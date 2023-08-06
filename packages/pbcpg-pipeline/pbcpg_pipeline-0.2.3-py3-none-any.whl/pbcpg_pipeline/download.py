import urllib3
import shutil
import os
import os.path
import ftplib
import gzip
from pbcpg_pipeline.env import (EXAMPLE_DATA_URLS, EXAMPLE_DATA_DIR, HG38_FTP,
                                HG38_GENOME_PATH, HG38_ANNOT_PATH)

def download_example(dir: str = EXAMPLE_DATA_DIR, n_samples: int = 1):
    """Download an example datatset

    Parameters
    ----------
    dir : str
        Destination directory for example data
    n_samples : int
        Number of samples to download, max 4 [1]
    """

    if n_samples > 4:
        raise RuntimeError('n_samples parameter must be <= 4')
    hg38_genome_local_path = os.path.join(dir, os.path.basename(HG38_GENOME_PATH).replace('fna.gz', 'fa'))
    hg38_annot_local_path = os.path.join(dir, os.path.basename(HG38_ANNOT_PATH))
    if os.path.exists(hg38_genome_local_path):
        print(f'destination {hg38_genome_local_path} already exists')
    else:
        ftp = ftplib.FTP(HG38_FTP)
        ftp.login()
        with open(f'{hg38_genome_local_path}.gz', 'wb') as f:
            ftp.retrbinary(f'RETR {HG38_GENOME_PATH}', f.write)
    with gzip.open(f'{hg38_genome_local_path}.gz', 'rb') as f_in:
        with open(hg38_genome_local_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(f'{hg38_genome_local_path}.gz')
    if os.path.exists(hg38_annot_local_path):
        print(f'destination {hg38_annot_local_path} already exists')
    else:
        ftp = ftplib.FTP(HG38_FTP)
        ftp.login()
        with open(hg38_annot_local_path, 'wb') as f:
            ftp.retrbinary(f'RETR {HG38_ANNOT_PATH}', f.write)
    http = urllib3.PoolManager()
    for example_data_url in EXAMPLE_DATA_URLS[:n_samples]:
        file_path = os.path.join(dir, os.path.basename(example_data_url))
        if os.path.exists(file_path):
            print(f'destination {file_path} already exists')
            continue
        with http.request('GET', example_data_url, preload_content=False) as r, open(file_path, 'wb') as out_file:
            shutil.copyfileobj(r, out_file)
