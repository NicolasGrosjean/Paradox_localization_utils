import argparse
import os
from pathlib import Path
import pandas as pd

import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from paradox_localization_utils.lib.read_localization_file import (
    file_to_keys_and_values,
    get_key_value_and_version,
    BadLocalizationException,
)


def get_args():
    parser = argparse.ArgumentParser(description="Extract existing translation from other files")
    parser.add_argument("extract_source_dir", type=str, help="Directory with source Paradox files to extract")
    parser.add_argument("extract_dest_dir", type=str, help="Directory with source Paradox files to extract")
    parser.add_argument("target_source_dir", type=str, help="Directory with source Paradox files to translate")
    parser.add_argument("target_dest_dir", type=str, help="Directory with destination Paradox files to edit")
    parser.add_argument("source_lang", type=str, help="Source language when EUIV, HoI4 or Stellaris game")
    parser.add_argument("dest_lang", type=str, help="Destination language when EUIV, HoI4 or Stellaris game")
    parser.add_argument("-source_col_ck2", type=int, help="Source language column index for CK2 files")
    parser.add_argument("-dest_col_ck2", type=int, help="Destination language column index for CK2 files")
    return parser.parse_args()


def extract_translation_from_CK2_file(
    ck2_loc_file: str | Path, extracted_translation: dict[str, str], source_col_ck2: int, dest_col_ck2: int
):
    """
    Add {source_text: dest_text} to extracted_translation dict
    :param ck2_loc_file: Path of the CK2 localisation file
    :param extracted_translation:  Dictionary which will be completed
    :param source_col_ck2: Index of the source language column
    :param dest_col_ck2: Index of the destination language column
    :return: None
    """
    try:
        df = pd.read_csv(ck2_loc_file, sep=";", header=None, encoding="ISO-8859-1")
        for _, row in df.iterrows():
            extracted_translation[row[df.columns[source_col_ck2]]] = row[df.columns[dest_col_ck2]]
    except pd.errors.ParserError:
        with open(ck2_loc_file, "r", encoding="ISO-8859-1") as f:
            lines = f.readlines()
        for line in lines:
            split = line.split(";")
            extracted_translation[split[source_col_ck2]] = split[dest_col_ck2]


def extract_translation_from_yml_file(
    source_loc_file: str | Path, dest_loc_file: str | Path, extracted_translation: dict[str, str]
):
    """
    Add {source_text: dest_text} to extracted_translation dict
    :param source_loc_file: Path of YML source file
    :param dest_loc_file: Path of YML destination file
    :param extracted_translation: Dictionary which will be completed
    :return:
    """
    source_texts, _ = file_to_keys_and_values(source_loc_file)
    dest_texts, _ = file_to_keys_and_values(dest_loc_file)
    for source_key in source_texts.keys():
        if source_key in dest_texts.keys() and source_texts[source_key]["value"] != "":
            extracted_translation[source_texts[source_key]["value"]] = dest_texts[source_key]["value"]


def insert_text(file_path: str | Path, extracted_translation: dict[str, str], target_source_files: dict[str, str]):
    """
    Modify localisation yml file be inserting extracted translation (key -> source_text -> extracted_dest_text)
    :param file_path: File path of the file to edit
    :param extracted_translation: Extracted translation {source_text: dest_text}
    :param target_source_files: Target source {key: source_text}
    :return: None
    """
    with open(file_path, "r", encoding="utf8") as f:
        lines = f.readlines()

    with open(file_path, "w", encoding="utf8") as f:
        for i in range(len(lines)):
            if i == 0:
                # Keep the language definition line
                f.write(lines[0])
            else:
                try:
                    key, value, version = get_key_value_and_version(lines[i])
                    if key not in target_source_files:
                        raise Exception(
                            f"{key} not in the source file corresponding to {file_path}.\n"
                            + "Apply diff before this script"
                        )
                    target_source_text = target_source_files[key]["value"]
                    if target_source_text in extracted_translation:
                        f.write(" " + key + ': "' + extracted_translation[target_source_text] + '"\n')
                    else:
                        f.write(lines[i])
                except BadLocalizationException:
                    f.write(lines[i])
                    continue


def extract_existing_translation(
    extract_source_dir: str | Path,
    extract_dest_dir: str | Path,
    target_source_dir: str | Path,
    target_dest_dir: str | Path,
    source_lang: str,
    dest_lang: str,
    source_col_ck2: int,
    dest_col_ck2: int,
):
    # Store extracted translation {source_text: dest_text}
    extracted_translation = dict()
    for root, _, files in os.walk(extract_source_dir):
        for file in files:
            if file.endswith(".csv"):
                extract_translation_from_CK2_file(
                    os.path.join(root, file), extracted_translation, source_col_ck2, dest_col_ck2
                )
            elif file.endswith(source_lang + ".yml"):
                extract_translation_from_yml_file(
                    os.path.join(root, file),
                    os.path.join(
                        root.replace(extract_source_dir, extract_dest_dir), file.replace(source_lang, dest_lang)
                    ),
                    extracted_translation,
                )
            else:
                print(f"{file} not managed !")

    # Store target source text {key: source_text}
    target_source_files = dict()
    for root, _, files in os.walk(target_source_dir):
        for file in files:
            if file.endswith(source_lang + ".yml"):
                target_source_file, _ = file_to_keys_and_values(os.path.join(root, file))
                target_source_files = {**target_source_files, **target_source_file}

    # Insert text in destination target file
    for root, _, files in os.walk(target_dest_dir):
        for file in files:
            if file.endswith(dest_lang + ".yml"):
                insert_text(os.path.join(root, file), extracted_translation, target_source_files)


if __name__ == "__main__":
    args = get_args()
    extract_existing_translation(
        args.extract_source_dir,
        args.extract_dest_dir,
        args.target_source_dir,
        args.target_dest_dir,
        args.source_lang,
        args.dest_lang,
        args.source_col_ck2,
        args.dest_col_ck2,
    )
