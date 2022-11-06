import argparse
import json
import os
import requests


def get_args():
    parser = argparse.ArgumentParser(description="Update files to translate on Paratranz")
    parser.add_argument("token", type=str, help="Paratranz API token")
    parser.add_argument("project_id", type=int, help="Id of the project on Paratranz")
    parser.add_argument(
        "loc_dir", type=str, help="Path of the localisation directory which will be browse recursively"
    )
    parser.add_argument("language", type=str, help="Source language to send only files with this suffix")
    return parser.parse_args()


def manage_request_error(r: requests.models.Response):
    if r.status_code != 200:
        try:
            error = json.loads(r._content.decode())
        except json.decoder.JSONDecodeError:
            print(r._content.decode())
            r.raise_for_status()
        if "message" in error:
            print(error["message"])
        elif "detail" in error:
            print(error["detail"])
        else:
            print(error)
        r.raise_for_status()


def get_project_files(project_id: int):
    r = requests.get(f"https://paratranz.cn/api/projects/{project_id}/files")
    manage_request_error(r)
    return {file["name"]: file["id"] for file in r.json()}


def create_or_update_file(token: str, project_id: int, filepath: str, file_id=None):
    headers = {"Authorization": token}
    url = f"https://paratranz.cn/api/projects/{project_id}/files"
    if file_id is not None:
        url += f"/{file_id}"
    r = requests.post(
        url,
        headers=headers,
        files={"file": open(filepath, "rb")},
    )
    manage_request_error(r)


if __name__ == "__main__":
    args = get_args()
    current_files = get_project_files(args.project_id)
    for root, _, files in os.walk(args.loc_dir):
        for file in files:
            if file.endswith(f"{args.language}.yml"):
                if file in current_files:
                    create_or_update_file(args.token, args.project_id, os.path.join(root, file), current_files[file])
                else:
                    create_or_update_file(args.token, args.project_id, os.path.join(root, file))
