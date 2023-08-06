# PBCPG pipeline

Analysis of CpG methylation calls from PacBio HiFi data

## Installation

### Conda

```
conda create -n pbcpg-pipeline -c bioconda -c conda-forge python==3.9 tensorflow==2.7 numpy==1.20.0 biopython pandas pysam tqdm pybigwig pbmm2
conda activate pbcpg-pipeline
pip install pbcpg-pipeline
```

Alternatively, from the git repo:

```
git clone https://gitlab.com/salk-tm/pbcpg-pipeline.git
cd pbcpg-pipeline
conda env create -f conda_env_cpg_pipeline.yaml
conda activate pbcpg-pipeline
pip install .
```
