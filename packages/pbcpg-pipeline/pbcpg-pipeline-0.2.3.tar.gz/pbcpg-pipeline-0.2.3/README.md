# PBCPG pipeline

Analysis of CpG methylation calls from PacBio HiFi data. See also the [full documentation](https://salk-tm.gitlab.io/pbcpg-pipeline/index.html)

## Installation

### Conda

The recommended way to install `pbcpg-pipeline` is with a dedicated `conda` environment:

```
conda create -n pbcpg-pipeline -c bioconda -c conda-forge \
  python==3.9 tensorflow==2.7 numpy==1.20.0 biopython pandas \
  pysam tqdm pybigwig pbmm2 urllib3 bedtools pybedtools gff2bed \
  seaborn pyfaidx
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


### Check installation

Check that the correct version was installed with `pbcpg-pipeline --version`
