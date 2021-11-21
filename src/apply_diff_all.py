import argparse
import os

import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.read_localization_file import (
    file_to_keys_and_lines,
    get_key,
    get_key_value_and_version,
    BadLocalizationException,
    file_to_keys_and_values,
)


DELETED_LINES_FILE_NAME = "deleted_lines.txt"


def get_args():
    parser = argparse.ArgumentParser(description="Apply diff in source to destination for all files")
    parser.add_argument("old_source_dir", type=str, help="Directory with source Paradox files for previous version")
    parser.add_argument("source_dir", type=str, help="Directory with source Paradox files for new version")
    parser.add_argument(
        "-dest_dir",
        type=str,
        help="Directory with destination Paradox files (not used when EUIV, HoI4 or Stellaris game)",
    )
    parser.add_argument("-source_lang", type=str, help="Source language when EUIV, HoI4 or Stellaris game")
    parser.add_argument("-dest_lang", type=str, help="Destination language when EUIV, HoI4 or Stellaris game")
    return parser.parse_args()


def is_source_lang_line(line: str, language: str):
    lang_line = f"l_{language}:"
    return line.replace("\ufeff", "").replace("\n", "").replace(" ", "").replace("\t", "") == lang_line


def apply_diff_one_file(
    source_file_path,
    dest_file_path,
    old_source_values,
    dest_texts,
    dest_lang_line,
    source_lang,
    existing_translations,
    dest_lines_not_found,
):
    with open(source_file_path, "r", encoding="utf8") as f:
        source_lines = f.readlines()

    with open(dest_file_path, "w", encoding="utf8") as f:
        source_lang_line_seen = False
        first_line = True
        for source_line in source_lines:
            if not source_lang_line_seen:
                if not is_source_lang_line(source_line, source_lang):
                    # Copy source header
                    f.write(source_line)
                else:
                    # Add the language description
                    if first_line:
                        f.write(dest_lang_line)
                    else:
                        f.write(dest_lang_line[1:])
                    source_lang_line_seen = True
            else:
                try:
                    key, value, version, source_other = get_key_value_and_version(source_line)
                    print_version = version if version is not None else ""
                except BadLocalizationException:
                    f.write(source_line)
                    continue
                if key in dest_texts and (dest_texts[key] != "" or value == ""):
                    try:
                        _, dest_text, _, other = get_key_value_and_version(dest_texts[key])
                    except BadLocalizationException:
                        dest_text = ""
                    if key in old_source_values and old_source_values[key]["value"] != value:
                        # The source has changed
                        if dest_text != "":
                            # We keep destination text but update version
                            if len(other) == 0 or other[-1] != "\n":
                                other += "\n"
                            f.write(f' {key}:{print_version} "{dest_text}"{other}')
                            # Update the dest lines not found
                            if dest_texts[key] in dest_lines_not_found:
                                dest_lines_not_found.remove(dest_texts[key])
                        else:
                            # Error with destination text extracted, we use source text
                            f.write(source_line)
                    else:
                        # Keep previous translation
                        f.write(dest_texts[key])
                        # Update the dest lines not found
                        if dest_texts[key] in dest_lines_not_found:
                            dest_lines_not_found.remove(dest_texts[key])
                else:
                    if len(source_other) == 0 or source_other[-1] != "\n":
                        source_other += "\n"
                    if value in existing_translations:
                        # Add existing translation
                        f.write(f' {key}:{print_version} "{existing_translations[value]}"{source_other}')
                    else:
                        f.write(f' {key}:{print_version}Z "{value}"{source_other}')
            first_line = False


def apply_diff_all_eu_hoi_stellaris(old_dir, current_dir, source_lang, dest_lang):
    """
    Apply diff for all files for EUIV, HoI4 or Stellaris
    :param old_dir: Directory with source Paradox files for previous version
    :param current_dir: Directory with source and destination Paradox files for new version
    :param source_lang: Source language
    :param dest_lang: Destination language
    :return:
    """
    # Store old source texts
    old_source_values = dict()
    for root, _, files in os.walk(old_dir):
        for file in files:
            if file.endswith(source_lang + ".yml"):
                abs_path = os.path.abspath(os.path.join(root, file))
                file_old_source_texts, _ = file_to_keys_and_values(abs_path)
                old_source_values = {**old_source_values, **file_old_source_texts}
    # Store current dest texts and delete files
    rel_to_dest_abs_path = dict()
    dest_texts = dict()
    dest_values = dict()
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith(dest_lang + ".yml"):
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_to_dest_abs_path[abs_path[: abs_path.find("_l_")].replace(current_dir, "")] = abs_path
                file_dest_texts, _ = file_to_keys_and_lines(abs_path)
                file_dest_values, _ = file_to_keys_and_values(abs_path)
                os.remove(abs_path)
                dest_texts = {**dest_texts, **file_dest_texts}
                dest_values = {**dest_values, **file_dest_values}
    # Map current translation
    existing_translations = dict()
    for source_key in old_source_values.keys():
        if source_key in dest_values.keys() and old_source_values[source_key]["value"] != "":
            existing_translations[old_source_values[source_key]["value"]] = dest_values[source_key]["value"]
    # List all dest lines to export deleted ones
    dest_lines_not_found = {
        line for line in dest_texts.values() if not line.replace("\ufeff", "").startswith(f"l_{dest_lang}")
    }
    # Apply diff with current source texts
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith(source_lang + ".yml"):
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = abs_path[: abs_path.find("_l_")].replace(current_dir, "")
                if rel_path in rel_to_dest_abs_path:
                    dest_file_path = rel_to_dest_abs_path[rel_path]
                else:
                    dest_file_path = abs_path.replace(source_lang + ".yml", dest_lang + ".yml")
                apply_diff_one_file(
                    abs_path,
                    dest_file_path,
                    old_source_values,
                    dest_texts,
                    "\ufeffl_" + dest_lang + ":\n",
                    source_lang,
                    existing_translations,
                    dest_lines_not_found,
                )
    # Export dest lines not found if there are some ones
    if len(dest_lines_not_found) > 0:
        dest_lines_not_found_list = list(dest_lines_not_found)
        with open(f"{dest_lang}_{DELETED_LINES_FILE_NAME}", "w", encoding="utf8") as f:
            f.writelines(dest_lines_not_found_list)
        with open(f"{source_lang}_{DELETED_LINES_FILE_NAME}", "w", encoding="utf8") as f:
            for line in dest_lines_not_found_list:
                key = get_key(line)
                old_source_line = old_source_values[key]
                other = old_source_line["other"]
                if len(other) == 0 or other[-1] != "\n":
                    other += "\n"
                f.write(f' {key}:{old_source_line["version"]} "{old_source_line["value"]}"{other}')

if __name__ == "__main__":
    args = get_args()
    if (args.source_lang is None) and (args.dir_lang is None):
        print("Not yet implemented!")
    else:
        answer = input(f"Do want apply diff with {args.old_source_dir} as old source directory ? [y/N]")
        if answer.lower() == "y":
            apply_diff_all_eu_hoi_stellaris(args.old_source_dir, args.source_dir, args.source_lang, args.dest_lang)
