"""This package defines a pipeline including both alignment by
`pbmm2 <https://github.com/PacificBiosciences/pbmm2>`_ and CpG
analysis by `pb-CpG-tools <https://github.com/PacificBiosciences/pb-CpG-tools>`_ , taking input unaligned PacBio BAM
data to output methylation calls.
"""

from pbcpg_pipeline.version import __version__
from pbcpg_pipeline.env import MODEL_DIR
from pbcpg_pipeline.align_bam import align_bam, align_bams
from pbcpg_pipeline.aligned_bam_to_cpg_scores import (get_regions_to_process,
    run_all_pileup_processing, write_output_bed, convert_bed_to_bigwig)