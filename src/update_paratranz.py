import argparse
from joblib import Parallel, delayed
import os
import requests
import time

from src.utils import compute_time, manage_request_error


def get_args():
    parser = argparse.ArgumentParser(description="Update files to translate on Paratranz")
    parser.add_argument("token", type=str, help="Paratranz API token")
    parser.add_argument("project_id", type=int, help="Id of the project on Paratranz")
    parser.add_argument(
        "loc_dir", type=str, help="Path of the localisation directory which will be browse recursively"
    )
    parser.add_argument("language", type=str, help="Source language to send only files with this suffix")
    parser.add_argument("-parallel_nb", type=int, help="Number of parallel tasks", default=-1)
    return parser.parse_args()


def create_or_update_files(project_id: int, token: str, loc_dir: str, language: str, parallel_nb: int):
    __assert_localisation_directory_format(loc_dir, language)
    start = time.time()
    try:
        current_files = get_project_files(project_id)
    except requests.HTTPError:
        print("WARNING: Fail to get the list of files from Paratranz")
        print("Files can be created but not updated")
        current_files = dict()
    print(f"Update_paratranz on {os.path.join(loc_dir, language)}")
    all_files = []
    for root, _, files in os.walk(os.path.join(loc_dir, language)):
        for file in files:
            all_files.append(os.path.join(root, file))
    files_with_errors = []
    Parallel(n_jobs=parallel_nb, backend="threading")(
        delayed(create_or_update_file)(
            token, project_id, loc_dir, language, file_path, current_files, files_with_errors
        )
        for file_path in all_files
    )
    if len(files_with_errors) > 0:
        print("-------------------------")
        print("ERROR: Non updated files:")
        for file in files_with_errors:
            print(file)
    print(f"Total time of the execution: {compute_time(start)}")

def __assert_localisation_directory_format(loc_dir: str, language: str):
    if not os.path.isdir(loc_dir):
        raise ValueError(f"Directory {loc_dir} does not exist")
    if not os.path.isdir(os.path.join(loc_dir, language)):
        raise ValueError(f"Directory {os.path.join(loc_dir, language)} does not exist")

def get_project_files(project_id: int) -> dict[str, int]:
    r = requests.get(f"https://paratranz.cn/api/projects/{project_id}/files")
    manage_request_error(r)
    return {file["name"]: file["id"] for file in r.json()}


def create_or_update_file(
    token: str,
    project_id: int,
    loc_dir: str,
    language: str,
    file_path: str,
    current_files: dict[str, int],
    files_with_errors: list,
    sleeping_before_retry: int = 2,
):
    file_relative_path = file_path.replace(f"{loc_dir}\\{language}\\", "")
    paratranz_path = os.path.dirname(file_relative_path)
    if file_path.endswith(f"{language}.yml"):
        try:
            if file_relative_path.replace("\\", "/") in current_files:
                print(f"Update file {file_relative_path}")
                __post_file_to_paratranz_with_retry(
                    token,
                    project_id,
                    file_path,
                    paratranz_path,
                    sleeping_before_retry,
                    current_files[file_relative_path.replace("\\", "/")],
                )
            else:
                print(f"Create file {file_relative_path}")
                __post_file_to_paratranz_with_retry(
                    token, project_id, file_path, paratranz_path, sleeping_before_retry
                )
        except requests.HTTPError:
            files_with_errors.append(file_relative_path)


def __post_file_to_paratranz_with_retry(
    token: str,
    project_id: int,
    filepath: str,
    paratranz_path: str,
    sleeping_before_retry: int,
    file_id: int | None = None,
):
    headers = {"Authorization": token}
    url = f"https://paratranz.cn/api/projects/{project_id}/files"
    if file_id is not None:
        url += f"/{file_id}"
    try:
        __post_file_to_paratranz(url, headers, filepath, paratranz_path)
    except requests.HTTPError:
        print(f"Fail to create/update {filepath}, retry in {sleeping_before_retry} seconds")
        time.sleep(sleeping_before_retry)
        __post_file_to_paratranz(url, headers, filepath, paratranz_path)


def __post_file_to_paratranz(url: str, headers: dict, filepath: str, paratranz_path: str):
    r = requests.post(
        url,
        headers=headers,
        data={"path": paratranz_path},
        files={"file": open(filepath, "rb")},
    )
    manage_request_error(r)


if __name__ == "__main__":
    print("Version of the software: 1.1 (27th September 2024)")
    args = get_args()
    create_or_update_files(args.project_id, args.token, args.loc_dir, args.language, args.parallel_nb)
