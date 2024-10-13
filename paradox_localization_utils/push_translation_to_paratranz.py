import argparse
from joblib import Parallel, delayed
import os
import requests
import time

from paradox_localization_utils.update_paratranz import get_project_files
from paradox_localization_utils.utils import compute_time, manage_request_error


def get_args():
    parser = argparse.ArgumentParser(description="Push translation files on Paratranz")
    parser.add_argument("token", type=str, help="Paratranz API token")
    parser.add_argument("project_id", type=int, help="Id of the project on Paratranz")
    parser.add_argument(
        "loc_dir", type=str, help="Path of the localisation directory which will be browse recursively"
    )
    parser.add_argument("source_language", type=str, help="Source language which suffix the files")
    parser.add_argument("translation_language", type=str, help="Source language to send only files with this suffix")
    parser.add_argument("-parallel_nb", type=int, help="Number of parallel tasks", default=-1)
    return parser.parse_args()


def push_all_translations(
    project_id: int, token: str, loc_dir: str, source_language: str, translation_language: str, parallel_nb: int
) -> dict[str, int]:
    __assert_localisation_directory_format(loc_dir, source_language)
    start = time.time()
    try:
        current_files = get_project_files(project_id)
    except requests.HTTPError:
        print("ERROR: Fail to get the list of files from Paratranz")
        return
    print(f"Update_paratranz on {loc_dir}")
    all_files = []
    for root, _, files in os.walk(loc_dir):
        for file in files:
            if file.endswith(f"{source_language}.yml"):
                all_files.append(os.path.join(root, file))
    files_with_errors = []
    Parallel(n_jobs=parallel_nb, backend="threading")(
        delayed(push_a_translation)(
            token,
            project_id,
            loc_dir,
            source_language,
            translation_language,
            file_path,
            current_files,
            files_with_errors,
        )
        for file_path in all_files
    )
    if len(files_with_errors) > 0:
        print("-------------------------")
        print("ERROR: Non updated files:")
        for file in files_with_errors:
            print(file)
    print(f"Total time of the execution: {compute_time(start)}")
    return current_files


def __assert_localisation_directory_format(loc_dir: str, language: str):
    if not os.path.isdir(loc_dir):
        raise ValueError(f"Directory {loc_dir} does not exist")
    if not os.path.isdir(os.path.join(loc_dir, language)):
        raise ValueError(f"Directory {os.path.join(loc_dir, language)} does not exist")


def push_a_translation(
    token: str,
    project_id: int,
    loc_dir: str,
    source_language: str,
    translation_language: str,
    file_path: str,
    current_files: dict[str, int],
    files_with_errors: list,
    sleeping_before_retry: int = 2,
):
    file_relative_path = (
        file_path.replace(f"{loc_dir}\\", "")
        .replace(f"{loc_dir}/", "")
        .replace(f"{source_language}\\", "")
        .replace(f"{source_language}/", "")
        .replace(f"replace\\{source_language}\\", "replace\\")
        .replace(f"replace/{source_language}/", "replace/")
    )
    if file_path.endswith(f"{source_language}.yml"):
        try:
            if file_relative_path.replace("\\", "/") in current_files:
                print(f"Push translation of file {file_relative_path}")
                __push_translation_to_paratranz_with_retry(
                    token,
                    project_id,
                    file_path.replace(source_language, translation_language),
                    sleeping_before_retry,
                    current_files.pop(file_relative_path.replace("\\", "/")),
                )
            else:
                files_with_errors.append(file_relative_path)
        except requests.HTTPError:
            files_with_errors.append(file_relative_path)


def __push_translation_to_paratranz_with_retry(
    token: str,
    project_id: int,
    filepath: str,
    sleeping_before_retry: int,
    file_id: int,
):
    headers = {"Authorization": token}
    url = f"https://paratranz.cn/api/projects/{project_id}/files/{file_id}/translation"
    try:
        __push_translation_to_paratranz(url, headers, filepath)
    except requests.HTTPError:
        print(f"Fail to create/update {filepath}, retry in {sleeping_before_retry} seconds")
        time.sleep(sleeping_before_retry)
        __push_translation_to_paratranz(url, headers, filepath)


def __push_translation_to_paratranz(url: str, headers: dict, filepath: str):
    r = requests.post(
        url,
        headers=headers,
        data={},
        files={"file": open(filepath, "rb")},
    )
    manage_request_error(r)


if __name__ == "__main__":
    print("Version of the software: 1.0 (13th October 2024)")
    args = get_args()
    push_all_translations(
        args.project_id, args.token, args.loc_dir, args.source_language, args.translation_language, args.parallel_nb
    )
