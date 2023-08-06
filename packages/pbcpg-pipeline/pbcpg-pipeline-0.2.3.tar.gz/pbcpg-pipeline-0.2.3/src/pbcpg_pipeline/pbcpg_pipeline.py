#===============================================================================
# pbcpg_pipeline.py
#===============================================================================

"""Postprocess PacBio methylation calls"""




# Imports ======================================================================

import argparse
import os.path
from math import floor
from pbcpg_pipeline.env import MODEL_DIR, EXAMPLE_DATA_DIR
from pbcpg_pipeline.version import __version__
from pbcpg_pipeline.download import download_example
from pbcpg_pipeline.align_bam import align_bams
from pbcpg_pipeline.aligned_bam_to_cpg_scores import (setup_logging,
    log_args, get_regions_to_process, run_all_pileup_processing,
    write_output_bed, convert_bed_to_bigwig)
from pbcpg_pipeline.mean import calculate_mean, calculate_total_mean
from pbcpg_pipeline.gene_body_methylation import gene_body_methylation
from pbcpg_pipeline.promoter_methylation import promoter_methylation
from pbcpg_pipeline.plot import plot, COLOR_PALETTE
from pbcpg_pipeline.plot_genes import plot_genes
from pbcpg_pipeline.plot_repeats import plot_repeats
from pbcpg_pipeline.merge import merge_bedmethyl
from pbcpg_pipeline.intersect import intersect_bedmethyl
from pbcpg_pipeline.export_bedgraph import export_bedgraph




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
    for bam in args.bam:
        check_required_file(bam, "input bam")
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


def _download_example(args):
    download_example(dir=args.dir, n_samples=args.n_samples)


def _align(args):
    align_bams(args.fasta, args.bam, args.aligned_bam,
              threads=max(1, args.threads-1),
              memory_mb=max(floor(args.memory/args.threads), 1))


def process_aligned(args):
    setup_logging(args.output_label)
    validate_args_post_alignment(args)
    log_args(args)
    if args.verbose:
        print("\nChunking regions for multiprocessing.")
    regions_to_process = get_regions_to_process(args.bam, args.fasta,
        args.chunksize, args.modsites, "model", args.model_dir, args.min_mapq,
        args.hap_tag)
    if args.verbose:
        print("Running multiprocessing on {:,} chunks.".format(len(regions_to_process)))
    bed_results = run_all_pileup_processing(regions_to_process, args.threads)
    if args.verbose:
        print("Finished multiprocessing.\nWriting bed files.")
    bed_files = write_output_bed(args.output_label, args.modsites,
        args.min_coverage, bed_results)
    if args.verbose:
        print("Writing bigwig files.")
    convert_bed_to_bigwig(bed_files, args.fasta, "model")
    if args.verbose:
        print("Finished.\n")


def run_pbcpg_pipeline(args):
    validate_args_pre_alignment(args)
    aligned_bam = f'{args.output_label}.pbmm2.bam'
    align_bams(args.fasta, args.bam, aligned_bam,
              threads=max(1, args.threads-1),
              memory_mb = max(floor(args.memory/args.threads), 1))
    args.bam = aligned_bam
    process_aligned(args)


def _calculate_mean(args):
    if args.total:
        calculate_total_mean(args.bedmethyl, plot=args.plot,
                             groups=args.groups, title=args.title,
                             legend_title=args.legend_title, width=args.width,
                             color_palette=args.color_palette)
    else:
        calculate_mean(args.bedmethyl, plot=args.plot,
                       chromosomes=args.chromosomes, groups=args.groups,
                       title=args.title, legend_title=args.legend_title,
                       width=args.width, color_palette=args.color_palette)


def _promoter_methylation(args):
    promoter_methylation(args.features, args.bedmethyl,
        upstream_flank=args.upstream_flank,
        downstream_flank=args.downstream_flank, chromosomes=args.chromosomes,
        cytosines=args.cytosines, coverage=args.coverage,
        min_coverage=args.min_coverage, bins=args.bins, levels=args.levels,
        hist=args.hist, hist_log=args.hist_log, palette=args.palette)


def _gene_body_methylation(args):
    gene_body_methylation(args.features, args.bedmethyl,
        upstream_flank=args.upstream_flank,
        downstream_flank=args.downstream_flank, chromosomes=args.chromosomes,
        cytosines=args.cytosines, coverage=args.coverage,
        min_coverage=args.min_coverage, bins=args.bins, levels=args.levels,
        hist=args.hist, hist_log=args.hist_log, palette=args.palette)

def _plot(args):
    plot(args.bedmethyl, args.output, reference=args.reference,
         chromosomes=args.chromosomes, groups=args.groups, title=args.title,
         legend=args.legend, legend_title=args.legend_title,
         bin_size=args.bin_size, width=args.width,
         color_palette=args.color_palette, alpha=args.alpha,
         x_label=args.x_label)


def _plot_genes(args):
    plot_genes(args.features, args.bedmethyl, args.output, groups=args.groups,
               flank=args.flank, smooth=args.smooth, title=args.title,
               confidence_interval=args.confidence_interval,
               gene_bins=args.gene_bins, gene_levels=args.gene_levels,
               legend=args.legend, legend_title=args.legend_title,
               palette=args.palette, width=args.width, alpha=args.alpha)


def _plot_repeats(args):
    plot_repeats(args.features, args.bedmethyl, args.output, type=args.type,
                 groups=args.groups, flank=args.flank, smooth=args.smooth,
                 title=args.title, confidence_interval=args.confidence_interval,
                 legend=args.legend, legend_title=args.legend_title,
                 palette=args.palette, width=args.width, alpha=args.alpha)

def _merge(args):
    merge_bedmethyl(args.bedmethyl, chromosomes=args.chromosomes)


def _intersect(args):
    intersect_bedmethyl(args.bedmethyl, chromosomes=args.chromosomes)


def _export_bedgraph(args):
    export_bedgraph(args.bedmethyl, chromosomes=args.chromosomes,
                    coverage=args.coverage)


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
    subparsers = parser.add_subparsers()
    
    parser_download = subparsers.add_parser('download-example', help='download an example dataset')
    parser_download.set_defaults(func=_download_example)
    parser_download.add_argument(
        '-d', '--dir', metavar='<dir/>', default=EXAMPLE_DATA_DIR,
        help='destination directory for example data')
    parser_download.add_argument(
        '-n', '--n-samples', metavar='<int>', type=int, default=1,
        help='number of samples to download, max 4 [1]')

    parser_run = subparsers.add_parser('run', help='run full pipeline')
    parser_run.set_defaults(func=run_pbcpg_pipeline)
    io_args = parser_run.add_argument_group('io args')
    io_args.add_argument("bam", metavar="<unaligned.bam>", nargs='+',
                        help="Unaligned BAM file.")
    io_args.add_argument("fasta", metavar="<ref.fasta>",
                        help="The reference fasta file.")
    io_args.add_argument("output_label", metavar="<label>",
                        help="Label for output files, which results in [label].bam/bed/bw.")
    io_args.add_argument("--verbose", action="store_true",
                        help="verbose output")
    score_args = parser_run.add_argument_group('score args')
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
    resource_args = parser_run.add_argument_group('resource args')
    resource_args.add_argument("-t", "--threads", metavar="<int>", default=1,
                        type=int,
                        help="Number of threads for parallel processing. [default = %(default)d]")
    resource_args.add_argument("--memory", metavar="<int>", default=4_000,
                        type=int,
                        help="Memory for read alignment and sorting in megabytes. [default = %(default)d]")

    parser_align = subparsers.add_parser('align', help='align BAM to reference')
    parser_align.set_defaults(func=_align)
    io_args = parser_align.add_argument_group('io args')
    io_args.add_argument("bam", metavar="<unaligned.bam>", nargs='+',
        help="Unaligned BAM file to read.")
    io_args.add_argument("fasta", metavar="<ref.fasta>",
        help="The reference fasta file.")
    io_args.add_argument("aligned_bam", metavar="<aligned.bam>",
        help="Aligned bam file to write.")
    resource_args = parser_align.add_argument_group('resource args')
    resource_args.add_argument("-t", "--threads", metavar="<int>", type=int,
        default=1,
        help="Number of threads for parallel processing. [default = %(default)d]")
    resource_args.add_argument("--memory", metavar="<int>", type=int,
        default=4_000,
        help="Memory for read alignment and sorting in megabytes. [default = %(default)d]")

    parser_process = subparsers.add_parser('process', help='process aligned reads')
    parser_process.set_defaults(func=process_aligned)
    io_args = parser_process.add_argument_group('io args')
    io_args.add_argument("bam", metavar="<aligned.bam>",
                        help="Aligned BAM file.")
    io_args.add_argument("fasta", metavar="<ref.fasta>",
                        help="The reference fasta file.")
    io_args.add_argument("output_label", metavar="<label>",
                        help="Label for output files, which results in [label].bam/bed/bw.")
    io_args.add_argument("--verbose", action="store_true",
                        help="verbose output")
    score_args = parser_process.add_argument_group('score args')
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
    resource_args = parser_process.add_argument_group('resource args')
    resource_args.add_argument("-t", "--threads", metavar="<int>", default=1,
                        type=int,
                        help="Number of threads for parallel processing. [default = %(default)d]")
    
    parser_mean = subparsers.add_parser('mean',
        help='calculate average methylation across chromosomes or in total')
    parser_mean.set_defaults(func=_calculate_mean)
    parser_mean.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_mean.add_argument('--plot', metavar='<output.{pdf,png,svg}>',
        help='path to output plot')
    domain_group = parser_mean.add_mutually_exclusive_group()
    domain_group.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to include')
    domain_group.add_argument('--total', action='store_true',
        help='calculate total genomic mean')
    parser_mean.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files [0]')
    parser_mean.add_argument('--title', metavar='<"Plot title">',
        default='Methylation', help='set the title for the plot')
    parser_mean.add_argument('--legend-title', metavar='<Title>',
        default='Group', help='title of legend')
    parser_mean.add_argument('--width', metavar='<float>', type=float,
        default=8, help='set width of figure in inches')
    parser_mean.add_argument('--color-palette', metavar='<#color>', nargs='+',
        default=COLOR_PALETTE, help='color palette to use')

    parser_promoter = subparsers.add_parser('promoter',
        help='quantify promoter methylation')
    parser_promoter.set_defaults(func=_promoter_methylation)
    parser_promoter.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_promoter.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        help='bedMethyl file containing methylation data')
    parser_promoter.add_argument('--upstream-flank', metavar='<int>', type=int,
        default=2000, help='length of upstream flank in bp [2000]')
    parser_promoter.add_argument('--downstream-flank', metavar='<int>',
        type=int, default=0, help='length of upstream flank in bp [0]')
    parser_promoter.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to include')
    parser_promoter.add_argument('--cytosines', action='store_true',
        help='output a column with number of cytosines in each promoter')
    parser_promoter.add_argument('--coverage', action='store_true',
        help='output a column of coverage for each promoter')
    parser_promoter.add_argument('--min-coverage', metavar='<int>',
        type=int, default=1, help='minimum coverage to include promoter [1]')
    parser_promoter.add_argument('--bins', action='store_true',
        help='output a column binning promoters by discrete methylation level')
    parser_promoter.add_argument('--levels', metavar='<Level>',
        nargs='+', default=['Min', 'Low', 'Mid', 'High', 'Max'],
        help='discrete methylation levels')
    parser_promoter.add_argument('--hist', metavar='<file.{pdf,png,svg}>',
        help='generate histogram of methylation levels')
    parser_promoter.add_argument('--hist-log', action='store_true',
        help='use a log scale for  histogram')
    parser_promoter.add_argument('--palette', metavar='<palette>',
        default='mako_r', help='name of seaborn color palette [mako_r]')

    parser_gene_body = subparsers.add_parser('gene-body',
        help='quantify gene body methylation')
    parser_gene_body.set_defaults(func=_gene_body_methylation)
    parser_gene_body.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_gene_body.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        help='bedMethyl file containing methylation data')
    parser_gene_body.add_argument('--upstream-flank', metavar='<int>', type=int,
        default=0, help='length of upstream flank in bp [0]')
    parser_gene_body.add_argument('--downstream-flank', metavar='<int>',
        type=int, default=0, help='length of upstream flank in bp [0]')
    parser_gene_body.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to include')
    parser_gene_body.add_argument('--cytosines', action='store_true',
        help='output a column with number of cytosines in each gene')
    parser_gene_body.add_argument('--coverage', action='store_true',
        help='output a column of coverage for each gene')
    parser_gene_body.add_argument('--min-coverage', metavar='<int>',
        type=int, default=1, help='minimum coverage to include gene [1]')
    parser_gene_body.add_argument('--bins', action='store_true',
        help='output  a column binning genes by discrete methylation level')
    parser_gene_body.add_argument('--levels', metavar='<Level>',
        nargs='+', default=['Min', 'Low', 'Mid', 'High', 'Max'],
        help='discrete methylation levels')
    parser_gene_body.add_argument('--hist', metavar='<file.{pdf,png,svg}>',
        help='generate histogram of methylation levels')
    parser_gene_body.add_argument('--hist-log', action='store_true',
        help='use a log scale for  histogram')
    parser_gene_body.add_argument('--palette', metavar='<palette>',
        default='mako_r', help='name of seaborn color palette [mako_r]')
    
    parser_plot = subparsers.add_parser('plot',
        help='plot methylation across chromosomes')
    parser_plot.set_defaults(func=_plot)
    parser_plot.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_plot.add_argument('output', metavar='<output.{pdf,png,svg}>',
        help='path to output file')
    parser_plot.add_argument('--reference', metavar='<reference.fa>',
        help='reference genome')
    parser_plot.add_argument('--chromosomes', metavar='<X>', nargs='+',
        help='chromosomes to plot')
    parser_plot.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files [0]')
    parser_plot.add_argument('--title', metavar='<"Plot title">',
        default='Methylation', help='set the title for the plot')
    parser_plot.add_argument('--x-label', metavar='<"Label">',
        help='set x-axis label for the plot')
    parser_plot.add_argument('--legend', action='store_true',
        help='include a legend with the plot')
    parser_plot.add_argument('--legend-title', metavar='<"Title">',
        default='Group', help='title of legend')
    parser_plot.add_argument('--bin-size', metavar='<int>', type=int, default=0,
        choices=(-2,-1,0,1,2),
        help=('Set bin size. The input <int> is converted to the bin size by '
              'the formula: 10^(<int>+6) bp. The default value is 0, i.e. '
              '1-megabase bins. [0]'))
    parser_plot.add_argument('--width', metavar='<float>', type=float,
        default=8, help='set width of figure in inches [8.0]')
    parser_plot.add_argument('--color-palette', metavar='<#color>', nargs='+',
        default=COLOR_PALETTE, help='color palette to use')
    parser_plot.add_argument('--alpha', metavar='<float>', type=float,
        default=0.5, help='transparency value for lines [0.5]')
    
    parser_plot_genes = subparsers.add_parser('plot-genes',
        help='plot methylation profiles over genomic features')
    parser_plot_genes.set_defaults(func=_plot_genes)
    parser_plot_genes.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_plot_genes.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_plot_genes.add_argument('output', metavar='<output.{pdf,png,svg}>',
        help='path to output file')
    parser_plot_genes.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files [0]')
    parser_plot_genes.add_argument('--flank', metavar='<int>', type=int,
        default=2000, help='size of flanking regions in bp [1000]')
    parser_plot_genes.add_argument('--smooth', action='store_true',
        help='draw a smoother plot')
    parser_plot_genes.add_argument('--confidence-interval', metavar='<int>',
        type=int, help='draw a confidence interval')
    parser_plot_genes.add_argument('--title', metavar='<"Plot title">',
        default='Methylation',
        help='set the title for the plot')
    parser_plot_genes.add_argument('--gene-bins', metavar='<gene_bins.json>',
        help='gene bins')
    parser_plot_genes.add_argument('--gene-levels', metavar='<Level>',
        nargs='+', default=['Min', 'Low', 'Mid', 'High', 'Max'],
        help='gene expression levels')
    parser_plot_genes.add_argument('--legend', action='store_true',
        help='include a legend with the plot')
    parser_plot_genes.add_argument('--legend-title', metavar='<Title>',
        default='Group', help='title of legend')
    parser_plot_genes.add_argument('--width', metavar='<float>', type=float,
        default=4, help='set width of figure in inches')
    parser_plot_genes.add_argument('--palette', metavar='<palette>',
        default='deep', help='name of seaborn color palette [deep]')
    parser_plot_genes.add_argument('--alpha', metavar='<float>', type=float,
        default=1, help='transparency value for lines [1.0]')
    
    parser_plot_repeats = subparsers.add_parser('plot-repeats',
        help='plot methylation profiles over genomic features')
    parser_plot_repeats.set_defaults(func=_plot_repeats)
    parser_plot_repeats.add_argument('features', metavar='<features.gff3>',
        help='gff3 file of genomic features')
    parser_plot_repeats.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_plot_repeats.add_argument('output', metavar='<output.{pdf,png,svg}>',
        help='path to output file')
    parser_plot_repeats.add_argument('--type', metavar='<"feature_type">',
        help='generate plot for a specific type of repeat')
    parser_plot_repeats.add_argument('--groups', metavar='<"Group">', nargs='+',
        help='list of groups for provided bedmethyl files [0]')
    parser_plot_repeats.add_argument('--flank', metavar='<int>', type=int,
        default=500, help='size of flanking regions in bp [500]')
    parser_plot_repeats.add_argument('--smooth', action='store_true',
        help='draw a smoother plot')
    parser_plot_repeats.add_argument('--confidence-interval', metavar='<int>',
        type=int, help='draw a confidence interval')
    parser_plot_repeats.add_argument('--title', metavar='<"Plot title">',
        default='Methylation',
        help='set the title for the plot')
    parser_plot_repeats.add_argument('--legend', action='store_true',
        help='include a legend with the plot')
    parser_plot_repeats.add_argument('--legend-title', metavar='<Title>',
        default='Group', help='title of legend')
    parser_plot_repeats.add_argument('--width', metavar='<float>', type=float,
        default=4, help='set width of figure in inches')
    parser_plot_repeats.add_argument('--palette', metavar='<palette>',
        default='deep', help='name of seaborn color palette [deep]')
    parser_plot_repeats.add_argument('--alpha', metavar='<float>', type=float,
        default=1, help='transparency value for lines [1.0]')
    
    parser_intersect = subparsers.add_parser('intersect',
        help='intersect two or more bedmethyl files')
    parser_intersect.set_defaults(func=_intersect)
    parser_intersect.add_argument('bedmethyl', metavar='<bedmethyl.bed>',
        nargs='+', help='bedMethyl file containing methylation data')
    parser_intersect.add_argument('output_prefix', metavar='<output-prefix>',
        help='prefix for output files')
    parser_intersect.add_argument('--chromosomes', metavar='<X>',
        nargs='+', help='chromosomes to include')

    return parser.parse_args()


def main():
    args = parse_arguments()
    args.func(args)
