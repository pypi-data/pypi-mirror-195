import os
import os.path

MODEL_DIR = os.environ.get('PBCPG_MODEL_DIR',
    os.path.join(os.path.dirname(__file__), 'pileup_calling_model'))
EXAMPLE_DATA_URLS = (
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64011_190830_220126.hifi_reads.bam',
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64011_190901_095311.hifi_reads.bam',
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64012_190920_173625.hifi_reads.bam',
    'https://downloads.pacbcloud.com/public/dataset/HG002-CpG-methylation-202202/m64012_190921_234837.hifi_reads.bam',
)
HG38_FTP = 'ftp.ncbi.nlm.nih.gov'
HG38_GENOME_PATH = 'genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz'
HG38_ANNOT_PATH = 'genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.gff.gz'
EXAMPLE_DATA_DIR = os.environ.get('PBCPG_EXAMPLE_DATA_DIR', os.path.dirname(__file__))
