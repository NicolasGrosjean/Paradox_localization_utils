import argparse
import os

import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from paradox_localization_utils.lib.read_localization_file import (
    file_to_keys_and_values,
    get_key_value_and_version,
    BadLocalizationException,
)


def get_args():
    parser = argparse.ArgumentParser(description="Keep edited lines only")
    parser.add_argument("source_dir", type=str, help="Directory with Paradox files to filter")
    parser.add_argument("original_dir", type=str, help="Directory with original Paradox files")
    parser.add_argument("target_dir", type=str, help="Directory where to write filtered lines")
    parser.add_argument("-language", type=str, help="Language to filter", default="english")
    parser.add_argument("-target_prefix", type=str, help="Prefix added to files in target_dir", default="replace ")
    return parser.parse_args()


def write_kept_lines(source_file_path: str, output_file_path: str, original_values_by_key: dict[str, str]):
    """Write in output_file_path the lines of source_file_path that are not in or are edited from original_values_by_key

    :param source_file_path: File to filter
    :param output_file_path: File where we write the filtered lines
    :param original_values_by_key: Dictionary with the original values by key
    """
    with open(source_file_path, "r", encoding="utf8") as f:
        lines = f.readlines()

    with open(output_file_path, "w", encoding="utf8") as f:
        language_found = False
        for line in lines:
            # Keep the language definition line
            if not language_found and line.replace("\ufeff", "").startswith("l_"):
                f.write(line)
                language_found = True
                continue
            try:
                key, value, _ = get_key_value_and_version(line)
                if key not in original_values_by_key or value != original_values_by_key[key]:
                    # It is a new or edited line, we keep it
                    f.write(line)
            except BadLocalizationException:
                pass


def keep_only_edited_lines(source_dir: str, original_dir: str, target_dir: str, language: str, target_prefix: str):
    # Store original file paths
    original_file_paths_by_file_name: dict[str, str] = dict()
    for root, _, files in os.walk(original_dir):
        for file in files:
            if file.endswith(language + ".yml"):
                original_file_paths_by_file_name[file] = os.path.join(root, file)

    # Analyze each file in source_dir to kepts only edited lines
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(language + ".yml"):
                print(f"Processing {file}...")
                # TODO Copy file when file is not in original_file_paths_by_file_name
                original_values_versions_by_key, _ = file_to_keys_and_values(original_file_paths_by_file_name[file])
                write_kept_lines(
                    os.path.join(root, file),
                    os.path.join(target_dir, target_prefix + file),
                    {key: original_values_versions_by_key[key]["value"] for key in original_values_versions_by_key},
                )


if __name__ == "__main__":
    args = get_args()
    keep_only_edited_lines(
        args.source_dir,
        args.original_dir,
        args.target_dir,
        args.language,
        args.target_prefix,
    )
