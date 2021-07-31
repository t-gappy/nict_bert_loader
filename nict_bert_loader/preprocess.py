import os
import subprocess
from logging import getLogger

logger = getLogger(__name__)


DOWNLOAD_URL = "https://alaginrc.nict.go.jp/nict-bert/"


def download_nict_bert(cache_dir, model_name):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

    zipfile_name = model_name + ".zip"
    url = DOWNLOAD_URL + zipfile_name
    outpath = os.path.join(cache_dir, zipfile_name)

    logger.info("Downloading zip file.")
    subprocess.run(["wget", "--no-check-certificate", "-O", outpath, url])

    logger.info("Extracting weight files.")
    subprocess.run(["unzip", "-d", cache_dir, outpath])