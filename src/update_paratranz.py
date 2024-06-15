import argparse
from joblib import Parallel, delayed
import os
import requests
import time

from utils import compute_time, manage_request_error


def get_args():
    parser = argparse.ArgumentParser(description="Update files to translate on Paratranz")
    parser.add_argument("token", type=str, help="Paratranz API token")
    parser.add_argument("project_id", type=int, help="Id of the project on Paratranz")
    parser.add_argument(
        "loc_dir", type=str, help="Path of the localisation directory which will be browse recursively"
    )
    parser.add_argument("language", type=str, help="Source language to send only files with this suffix")
    parser.add_argument("-parallel_nb", type=int, help="Number of parallel tasks",default=-1)
    return parser.parse_args()


def get_project_files(project_id: int):
    r = requests.get(f"https://paratranz.cn/api/projects/{project_id}/files")
    manage_request_error(r)
    return {file["name"]: file["id"] for file in r.json()}


def create_or_update_file(token: str, project_id: int, loc_dir: str, language: str, file_path: str, current_files: list):
    file_relative_path = file_path.replace(f"{loc_dir}\\{language}\\", "")
    if file_path.endswith(f"{language}.yml"):
        if file_relative_path.replace("\\", "/") in current_files:
            print(f"Update file {file_relative_path}")
            __create_or_update_file(
                token,
                project_id,
                file_path,
                file_relative_path,
                current_files[file_relative_path.replace("\\", "/")],
            )
        else:
            print(f"Create file {file_relative_path}")
            __create_or_update_file(token, project_id, file_path, file_relative_path)


def __create_or_update_file(token: str, project_id: int, filepath: str, file_relative_path: str, file_id=None):
    headers = {"Authorization": token}
    url = f"https://paratranz.cn/api/projects/{project_id}/files"
    if file_id is not None:
        url += f"/{file_id}"
    try:
        r = requests.post(
            url,
            headers=headers,
            data={"path": os.path.dirname(file_relative_path)},
            files={"file": open(filepath, "rb")},
        )
        manage_request_error(r)
    except:
        print(f"Fail to create/update {filepath}, retry in 2 seconds")
        time.sleep(2)
        r = requests.post(
            url,
            headers=headers,
            data={"path": os.path.dirname(file_relative_path)},
            files={"file": open(filepath, "rb")},
        )
        manage_request_error(r)


if __name__ == "__main__":
    args = get_args()
    start = time.time()
    current_files = get_project_files(args.project_id)
    print("Version of the software : 4th June 2024")
    print(f"Update_paratranz on {os.path.join(args.loc_dir, args.language)}")
    all_files = []
    for root, _, files in os.walk(os.path.join(args.loc_dir, args.language)):
        for file in files:
            all_files.append(os.path.join(root, file))
    Parallel(n_jobs=args.parallel_nb, backend="threading")(
        delayed(create_or_update_file)(args.token, args.project_id, args.loc_dir, args.language, file_path, current_files)
        for file_path in all_files)
    print(f"Total time of the execution: {compute_time(start)}")
