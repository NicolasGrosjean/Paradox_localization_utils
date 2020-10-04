import argparse
import Levenshtein
import os

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.read_localization_file import file_to_keys_and_lines, get_key_value_and_version, BadLocalizationException, \
    file_to_keys_and_values


def get_args():
    parser = argparse.ArgumentParser(description='Add missing lines to translation files')
    parser.add_argument('old_source_dir', type=str, help='Directory with source Paradox files for previous version')
    parser.add_argument('source_dir', type=str, help='Directory with source Paradox files for new version')
    parser.add_argument('dest_dir', type=str, help='Directory with destination Paradox files')
    parser.add_argument('-source_lang', type=str, help='Source language when EUIV, HoI4 or Stellaris game')
    parser.add_argument('-dest_lang', type=str, help='Destination language when EUIV, HoI4 or Stellaris game')
    return parser.parse_args()


def apply_diff_one_file(source_file_path, dest_file_path, old_source_values, dest_texts, dest_first_line):
    with open(source_file_path, 'r', encoding='utf8') as f:
        source_lines = f.readlines()

    with open(dest_file_path, 'w', encoding='utf8') as f:
        for i in range(len(source_lines)):
            if i == 0:
                if len(source_lines) == 1:
                    # Manage empty source file
                    f.write(source_lines[i])
                else:
                    # Add the language description
                    f.write(dest_first_line)
            else:
                try:
                    key, value, version = get_key_value_and_version(source_lines[i])
                except BadLocalizationException:
                    f.write(source_lines[i])
                    continue
                if key in old_source_values and Levenshtein.distance(old_source_values[key]['value'], value) >= 10:
                    # The source has changed enough to replace destination by current source text
                    f.write(' ' + key + ':9 "' + value + '"\n')
                elif key in dest_texts and (dest_texts[key] != '' or value == ''):
                    try:
                        _, dest_text, _ = get_key_value_and_version(dest_texts[key])
                    except BadLocalizationException:
                        dest_text = ''
                    if key in old_source_values and Levenshtein.distance(old_source_values[key]['value'], value) > 0:
                        if dest_text != old_source_values[key]['value']:
                            # The source has little changed and has been translated, we keep translation but change version number
                            f.write(' ' + key + ':9 "' + dest_text + '"\n')
                        else:
                            # Add current source text because the previous destination was not translated
                            f.write(' ' + key + ':9 "' + value + '"\n')
                    else:
                        # Keep previous translation
                        f.write(dest_texts[key])
                else:
                    # Add current source text
                    f.write(' ' + key + ':9 "' + value + '"\n')


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
            if file.endswith(source_lang + '.yml'):
                abs_path = os.path.abspath(os.path.join(root, file))
                file_old_source_texts, _ = file_to_keys_and_values(abs_path)
                old_source_values = {**old_source_values, **file_old_source_texts}
    # Store current dest texts and delete files
    rel_to_dest_abs_path = dict()
    dest_texts = dict()
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith(dest_lang + '.yml'):
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_to_dest_abs_path[abs_path[:abs_path.find('_l_')].replace(current_dir, '')] = abs_path
                file_dest_texts, _ = file_to_keys_and_lines(abs_path)
                os.remove(abs_path)
                dest_texts = {**dest_texts, **file_dest_texts}
    # Apply diff with current source texts
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith(source_lang + '.yml'):
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = abs_path[:abs_path.find('_l_')].replace(current_dir, '')
                if rel_path in rel_to_dest_abs_path:
                    dest_file_path = rel_to_dest_abs_path[rel_path]
                else:
                    dest_file_path = abs_path.replace(source_lang + '.yml', dest_lang + '.yml')
                apply_diff_one_file(abs_path, dest_file_path, old_source_values, dest_texts, '\ufeffl_' + dest_lang + ':\n')


if __name__ == '__main__':
    args = get_args()
    if (args.source_lang is None) and (args.dir_lang is None):
        print('Not yet implemented!')
    else:
        answer = input(f'Do want apply diff with {args.old_source_dir} as old source directory ? [y/N]')
        if answer.lower() == 'y':
            apply_diff_all_eu_hoi_stellaris(args.old_source_dir, args.source_dir, args.source_lang, args.dest_lang)
