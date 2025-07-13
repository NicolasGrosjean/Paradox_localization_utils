import argparse
import os
import shutil
import time
import zipfile
import requests

from lib.utils import manage_request_error


def get_args():
    parser = argparse.ArgumentParser(description="Download files from Paratranz")
    parser.add_argument("token", type=str, help="Paratranz API token")
    parser.add_argument("project_id", type=int, help="Id of the project on Paratranz")
    parser.add_argument(
        "raw_dir_path", type=str, help="Path where the downloaded raw directory artifact will be saved"
    )
    parser.add_argument(
        "utf8_dir_path", type=str, help="Path where the downloaded utf8 directory artifact will be saved"
    )
    return parser.parse_args()


def update_artifact(token: str, project_id: int):
    """Update the artifacts of a Paratranz project

    :param token: Paratranz API token
    :param project_id: Id of the project on Paratranz
    """
    headers = {"Authorization": token}
    url = f"https://paratranz.cn/api/projects/{project_id}/artifacts"
    r = requests.post(url, headers=headers)
    manage_request_error(r)


def download_artifact(token: str, project_id: int, raw_dir_path: str, utf8_dir_path: str):
    """Download the artifacts of a Paratranz project

    :param token: Paratranz API token
    :param project_id: Id of the project on Paratranz
    :param raw_dir_path: Where raw files where will be stored
    :param utf8_dir_path: Where utf8 files where will be stored
    """
    headers = {"Authorization": token}
    url = f"https://paratranz.cn/api/projects/{project_id}/artifacts/download"
    r = requests.get(url, headers=headers)
    manage_request_error(r)
    download_url = r.url
    print(f"Download artefact from {download_url}")
    output_zip_file = "tmp.zip"
    with open(output_zip_file, "wb") as f:
        r = requests.get(download_url, timeout=60)
        manage_request_error(r)
        f.write(r.content)
    print("Extract the artifact")
    try:
        zip_ref = zipfile.ZipFile(output_zip_file, "r")
        try:
            zip_ref.extractall(".")
        finally:
            zip_ref.close()
    finally:
        os.remove(output_zip_file)
    print("Move raw files")
    move_files("raw", raw_dir_path)
    print("Move utf8 files")
    move_files("utf8", utf8_dir_path)


def move_files(source_dir: str, dest_dir: str):
    """Delete dest_dir if it exists and replace it by source_dir

    :param source_dir: Directory to move
    :param dest_dir: Destination directory
    """
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.move(source_dir, dest_dir)


if __name__ == "__main__":
    args = get_args()
    update_artifact(args.token, args.project_id)
    waiting_time = 20
    print(f"Artifacts updated, wait {waiting_time} seconds before downloading")
    time.sleep(waiting_time)
    download_artifact(args.token, args.project_id, args.raw_dir_path, args.utf8_dir_path)
