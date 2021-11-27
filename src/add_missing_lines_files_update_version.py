import argparse
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.read_localization_file import (
    get_key_value_and_version,
    BadLocalizationException,
    file_to_keys_and_values,
)


def get_args():
    parser = argparse.ArgumentParser(
        description="Add missing lines and files, and update version number. Other said, all is update excepted edited texts which are not edited."
    )
    parser.add_argument("old_dir", type=str, help="Directory with old Paradox files which will be partially updated")
    parser.add_argument("new_dir", type=str, help="Directory with new Paradox files which update the old directory")
    parser.add_argument("language", type=str, help="Language")
    return parser.parse_args()


def add_missing_lines_one_file(new_file_path: str, target_file_path: str, old_values_versions: dict):
    with open(new_file_path, "r", encoding="utf8") as f:
        new_file_lines = f.readlines()

    with open(target_file_path, "w", encoding="utf8") as f:
        for i in range(len(new_file_lines)):
            if i == 0:
                f.write(new_file_lines[0])
            else:
                try:
                    key, value, version, _, other = get_key_value_and_version(new_file_lines[i])
                    new_version = "" if version is None else str(version)
                except BadLocalizationException:
                    f.write(new_file_lines[i])
                    continue
                # Add new line or update version
                new_value = old_values_versions[key]["value"] if key in old_values_versions else value
                new_other = old_values_versions[key]["other"] if key in old_values_versions else other
                if len(new_other) == 0 or new_other[-1] != "\n":
                    new_other += "\n"
                f.write(
                    f' {key}:{new_version} "{new_value}"{new_other}'
                )


def add_missing_lines_files_update_version(old_dir: str, new_dir: str, language: str):
    rel_to_target_abs_path = dict()
    old_values_versions = dict()
    for root, _, files in os.walk(old_dir):
        for file in files:
            if file.endswith(language+".yml"):
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = abs_path.replace(os.path.abspath(old_dir), "")
                if rel_path[0] == "\\":
                    rel_path = rel_path[1:]
                rel_to_target_abs_path[rel_path] = abs_path
                file_old_values_versions, _ = file_to_keys_and_values(abs_path)
                os.remove(abs_path)
                old_values_versions = {**old_values_versions, **file_old_values_versions}
    for root, _, files in os.walk(new_dir):
        for file in files:
            if file.endswith(language+".yml"):
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = abs_path.replace(os.path.abspath(new_dir), "")
                if rel_path[0] == "\\":
                    rel_path = rel_path[1:]
                if rel_path in rel_to_target_abs_path:
                    add_missing_lines_one_file(
                        os.path.join(root, file), rel_to_target_abs_path[rel_path], old_values_versions
                    )
                else:
                    os.makedirs(os.path.dirname(os.path.join(old_dir, rel_path)), exist_ok=True)
                    shutil.copyfile(os.path.join(root, file), os.path.join(old_dir, rel_path))


if __name__ == "__main__":
    args = get_args()
    add_missing_lines_files_update_version(args.old_dir, args.new_dir, args.language)
