import argparse
import json
import os

import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from paradox_localization_utils.lib.write_localization_file import edit_file_with_dict


def get_args():
    parser = argparse.ArgumentParser(description="Extract translation Paratranz file")
    parser.add_argument("paratranz_dir", type=str, help="Directory with JSON Paratranz files")
    parser.add_argument("localisation_dir", type=str, help="Directory with Paradox files to edit")
    parser.add_argument("language", type=str, help="Language of the Paradox files to edit")
    parser.add_argument("-extract_not_review", action="store_true", help="Extract not reviewed translation")
    return parser.parse_args()


def extract_paratranz_localisation(paratranz_file_path: str, localisation_file_path: str, extract_not_review: bool):
    if not os.path.exists(localisation_file_path):
        print(f"ERROR : {localisation_file_path} does not exist")
        return
    with open(paratranz_file_path, "r", encoding="utf8") as f:
        raw_paratranz_data = json.load(f)
    paratranz_data: dict[str, str] = dict()
    for line in raw_paratranz_data:
        if len(line["translation"]) > 0 and (extract_not_review or line["stage"] == 5):
            paratranz_data[line["key"].split(":")[0]] = line["translation"]
    edit_file_with_dict(localisation_file_path, paratranz_data)


def extract_paratranz_localisation_dir(
    paratranz_dir: str, language: str, localisation_dir: str, extract_not_review: bool
):
    for root, _, files in os.walk(paratranz_dir):
        for file in files:
            if file.endswith(".json"):
                if "l_" not in file:
                    print(f"l_ not in {file}")
                    continue
                loc_file_name = file[: file.rindex("l_")] + "l_" + language + ".yml"
                abs_path = os.path.abspath(os.path.join(root, loc_file_name))
                rel_path = abs_path.replace(paratranz_dir, "")[1:]
                extract_paratranz_localisation(
                    os.path.join(root, file), os.path.join(localisation_dir, rel_path), extract_not_review
                )


if __name__ == "__main__":
    args = get_args()
    extract_not_review = args.extract_not_review
    if extract_not_review is None:
        extract_not_review = False
    extract_paratranz_localisation_dir(args.paratranz_dir, args.language, args.localisation_dir, extract_not_review)
