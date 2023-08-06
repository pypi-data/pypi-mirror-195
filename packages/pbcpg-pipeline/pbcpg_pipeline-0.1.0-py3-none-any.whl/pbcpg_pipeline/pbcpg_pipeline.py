#===============================================================================
# pbcpg_pipeline.py
#===============================================================================

"""Postprocess PacBio methylation calls"""




# Imports ======================================================================

import argparse
import os.path
import subprocess
from math import floor
from pbcpg_pipeline.env import MODEL_DIR
from pbcpg_pipeline.version import __version__
from pbcpg_pipeline.aligned_bam_to_cpg_scores import (setup_logging,
    log_args, get_regions_to_process, run_all_pileup_processing,
    write_output_bed, convert_bed_to_bigwig)




# Functions ====================================================================

def error_exit(msg):
    """Exit with an error

    Parameters
    ----------
    msg : str
        String describing the error
    """

    raise Exception(msg)

def validate_args_pre_alignment(args):
    """Validate arguments before the alignment step

    Parameters
    ----------
    args
        argparse.Namespace containing the arguments
    """

    def check_required_file(file, label):
        if not os.path.isfile(file):
            error_exit(f"Can't find {label} file '{file}'")

    check_required_file(args.bam, "input bam")
    check_required_file(args.fasta, "reference fasta")
    if not os.path.isdir(args.model_dir):
        error_exit("{} is not a valid directory path!".format(args.model_dir))


def validate_args_post_alignment(args):
    """Validate arguments after the alignment step

    Parameters
    ----------
    args
        argparse.Namespace containing the arguments
    """

    def is_bam_index_found(bam_file):
        bam_index_extensions = (".bai", ".csi")
        for ext in bam_index_extensions:
            bam_index_file=bam_file+ext
            if os.path.isfile(bam_index_file):
                return True
        return False

    if not is_bam_index_found(args.bam):
        error_exit(f"Can't find index for bam file '{args.bam}'")


def align_bam(ref: str, in_bam: str, out_bam: str, threads: int = 1,
              memory_mb: int = 768):
    """Run pbmm2 to align a BAM file to a FASTA reference

    Parameters
    ----------
    ref : str
        path to reference FASTA
    in_bam : str
        path to input BAM
    out_bam : str
        path to output BAM
    threads : int
        number of threads to use
    memory_mb : int
        megabytes of memory to use
    """
    subprocess.run(('pbmm2', 'align', '--preset', 'HIFI', '--sort',
                    '-j', f'{threads}', '--sort-memory', f'{memory_mb}M',
                    ref, in_bam, out_bam))


def parse_arguments():
    """
    Get arguments from command line with argparse.
    """
    parser = argparse.ArgumentParser(
        description=("Align a BAM file, then calculate CpG positions and "
            "scores. Outputs the aligned BAM plus raw and coverage-filtered "
            "results in bed and bigwig format, including haplotype-specific "
            "results (when available)."))
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
    io_args = parser.add_argument_group('io args')
    io_args.add_argument("bam", metavar="<input.bam>",
                        help="The unaligned BAM file.")
    io_args.add_argument("fasta", metavar="<ref.fasta>",
                        help="The reference fasta file.")
    io_args.add_argument("output_label", metavar="<label>",
                        help="Label for output files, which results in [label].bam/bed/bw.")
    score_args = parser.add_argument_group('score args')
    score_args.add_argument("-d", "--model_dir", metavar="</path/to/model/dir>",
                        default=MODEL_DIR,
                        help=f"Full path to the directory containing the model (*.pb files) to load. [default = {MODEL_DIR}]")
    score_args.add_argument("-m", "--modsites", choices=["denovo", "reference"],
                        default="denovo",
                        help="Only output CG sites with a modification probability > 0 "
                             "(denovo), or output all CG sites based on the "
                             "supplied reference fasta (reference). [default = %(default)s]")
    score_args.add_argument("-c", "--min_coverage", metavar="<int>", default=4,
                        type=int,
                        help="Minimum coverage required for filtered outputs. [default: %(default)d]")
    score_args.add_argument("-q", "--min_mapq", metavar="<int>", default=0,
                        type=int,
                        help="Ignore alignments with MAPQ < N. [default: %(default)d]")
    score_args.add_argument("-a", "--hap_tag", metavar="<TAG>", default="HP",
                        help="The SAM tag containing haplotype information. [default: %(default)s]")
    score_args.add_argument("-s", "--chunksize", metavar="<int>", default=500_000,
                        type=int,
                        help="Break reference regions into chunks "
                             "of this size for parallel processing. [default = %(default)d]")
    resource_args = parser.add_argument_group('resource args')
    resource_args.add_argument("-t", "--threads", metavar="<int>", default=1,
                        type=int,
                        help="Number of threads for parallel processing. [default = %(default)d]")
    resource_args.add_argument("--memory", metavar="<int>", default=4_000,
                        type=int,
                        help="Memory for alignment in megabytes. [default = %(default)d]")
    return parser.parse_args()


def main():
    args = parse_arguments()
    validate_args_pre_alignment(args)
    aligned_bam = f'{args.output_label}.pbmm2.bam'
    align_bam(args.fasta, args.bam, aligned_bam, threads=max(1, args.threads-1),
              memory_mb = max(floor(args.memory/args.threads), 1))
    args.bam = aligned_bam
    setup_logging(args.output_label)
    validate_args_post_alignment(args)
    log_args(args)
    print("\nChunking regions for multiprocessing.")
    regions_to_process = get_regions_to_process(args.bam, args.fasta, args.chunksize, args.modsites,
                                                "model", args.model_dir, args.min_mapq, args.hap_tag)
    print("Running multiprocessing on {:,} chunks.".format(len(regions_to_process)))
    bed_results = run_all_pileup_processing(regions_to_process, args.threads)
    print("Finished multiprocessing.\nWriting bed files.")
    bed_files = write_output_bed(args.output_label, args.modsites, args.min_coverage, bed_results)
    print("Writing bigwig files.")
    convert_bed_to_bigwig(bed_files, args.fasta, "model")
    print("Finished.\n")
