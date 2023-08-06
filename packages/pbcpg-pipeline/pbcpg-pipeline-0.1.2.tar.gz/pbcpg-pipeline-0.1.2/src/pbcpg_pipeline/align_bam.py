import subprocess

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
