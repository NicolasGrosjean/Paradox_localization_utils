import argparse
import Levenshtein
import os

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.read_localization_file import (
    file_to_keys_and_lines,
    get_key_value_and_version,
    BadLocalizationException,
    file_to_keys_and_values,
)


def get_args():
    parser = argparse.ArgumentParser(description="Apply diff in source to destination for all files")
    parser.add_argument("old_source_dir", type=str, help="Directory with source Paradox files for previous version")
    parser.add_argument("source_dir", type=str, help="Directory with source Paradox files for new version")
    parser.add_argument("-dest_dir", type=str, help="Directory with destination Paradox files (not used when EUIV, HoI4 or Stellaris game)")
    parser.add_argument("-source_lang", type=str, help="Source language when EUIV, HoI4 or Stellaris game")
    parser.add_argument("-dest_lang", type=str, help="Destination language when EUIV, HoI4 or Stellaris game")
    return parser.parse_args()


def write_new_line_or_get_existing_translation(f, key, value, existing_translations):
    if value in existing_translations:
        f.write(" " + key + ':0 "' + existing_translations[value] + '"\n')
    else:
        f.write(" " + key + ':9 "' + value + '"\n')


def apply_diff_one_file(
    source_file_path,
    dest_file_path,
    old_source_values,
    dest_texts,
    dest_lang_line,
    source_lang_line,
    existing_translations,
):
    with open(source_file_path, "r", encoding="utf8") as f:
        source_lines = f.readlines()

    with open(dest_file_path, "w", encoding="utf8") as f:
        source_lang_line_seen = False
        first_line = True
        for source_line in source_lines:
            if not source_lang_line_seen:
                if source_line.replace("\ufeff", "").replace("\n", "") != source_lang_line.replace(
                    "\ufeff", ""
                ).replace("\n", ""):
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
                    key, value, version = get_key_value_and_version(source_line)
                except BadLocalizationException:
                    f.write(source_line)
                    continue
                if key in old_source_values and Levenshtein.distance(old_source_values[key]["value"], value) >= 10:
                    # The source has changed enough to replace destination by current source text
                    # OR translation if already translated elsewhere
                    write_new_line_or_get_existing_translation(f, key, value, existing_translations)
                elif key in dest_texts and (dest_texts[key] != "" or value == ""):
                    try:
                        _, dest_text, _ = get_key_value_and_version(dest_texts[key])
                    except BadLocalizationException:
                        dest_text = ""
                    if key in old_source_values and Levenshtein.distance(old_source_values[key]["value"], value) > 0:
                        if dest_text != old_source_values[key]["value"]:
                            # The source has little changed and has been translated,
                            # we keep translation but change version number
                            # OR translation if already translated elsewhere
                            write_new_line_or_get_existing_translation(f, key, dest_text, existing_translations)
                        else:
                            # Add current source text because the previous destination was not translated
                            # OR translation if already translated elsewhere
                            write_new_line_or_get_existing_translation(f, key, value, existing_translations)
                    else:
                        # Keep previous translation
                        f.write(dest_texts[key])
                else:
                    # Add current source text
                    # OR translation if already translated elsewhere
                    write_new_line_or_get_existing_translation(f, key, value, existing_translations)
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
                    "\ufeffl_" + source_lang + ":\n",
                    existing_translations,
                )


if __name__ == "__main__":
    args = get_args()
    if (args.source_lang is None) and (args.dir_lang is None):
        print("Not yet implemented!")
    else:
        answer = input(f"Do want apply diff with {args.old_source_dir} as old source directory ? [y/N]")
        if answer.lower() == "y":
            apply_diff_all_eu_hoi_stellaris(args.old_source_dir, args.source_dir, args.source_lang, args.dest_lang)
