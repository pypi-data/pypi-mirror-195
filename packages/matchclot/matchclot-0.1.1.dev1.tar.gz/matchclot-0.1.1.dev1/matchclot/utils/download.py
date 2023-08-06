import zipfile
from pathlib import Path
from urllib.request import urlopen, Request
from tqdm.auto import tqdm


def download(url: str, path: str):
    """Download a file from url
    Args:
        url: URL from which the data can be downloaded
        path: path to the file where the data will be saved
    """
    path = Path(path)
    # create the path if it does not exist
    path.parent.mkdir(parents=True, exist_ok=True)
    # download the file
    blocksize = 1024 * 8
    blocknum = 0

    try:
        with urlopen(Request(url, headers={"User-agent": "dataset-user"})) as rsp:
            total = rsp.info().get("content-length", None)
            file_path = path
            with tqdm(
                unit="B",
                unit_scale=True,
                miniters=1,
                unit_divisor=1024,
                total=total if total is None else int(total),
            ) as t, file_path.open("wb") as f:
                block = rsp.read(blocksize)
                while block:
                    f.write(block)
                    blocknum += 1
                    t.update(len(block))
                    block = rsp.read(blocksize)
    except (KeyboardInterrupt, Exception):
        # Make sure file doesn’t exist half-downloaded
        if file_path.is_file():
            file_path.unlink()
        raise


def unzip(file_path: str, dest_path: str):
    """Unzip a file
    Args:
        file_path: path to the file to unzip
        dest_path: path to the directory where the contents will be unzipped
    """
    dest_path = Path(dest_path)
    # create the path if it does not exist
    dest_path.mkdir(parents=True, exist_ok=True)
    # unzip the file
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(dest_path)
