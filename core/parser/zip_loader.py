import shutil
import zipfile
from pathlib import Path


def extract_zip(zip_path: str, output_dir: str):

    output = Path(output_dir)

    if output.exists():
        shutil.rmtree(output)

    output.mkdir(parents=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output)

    return output