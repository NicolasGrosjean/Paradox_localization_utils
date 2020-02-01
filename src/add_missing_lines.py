import argparse
import os

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.read_localization_file import file_to_keys_and_values, get_key_value_and_version, BadLocalizationException


def get_args():
    parser = argparse.ArgumentParser(description='Add missing lines to translation files')
    parser.add_argument('source_dir', type=str, help='Directory with source Paradox files')
    parser.add_argument('dest_dir', type=str, help='Directory with destination Paradox files')
    return parser.parse_args()


def add_missing_line(source_file_path, dest_file_path, old_lines_file_path):
    dest_texts, dest_first_line = file_to_keys_and_values(dest_file_path)

    with open(source_file_path, 'r', encoding='utf8') as f:
        source_lines = f.readlines()

    with open(dest_file_path, 'w', encoding='utf8') as f:
        for i in range(len(source_lines)):
            if i == 0:
                f.write(dest_first_line)
            else:
                try:
                    key, value, version = get_key_value_and_version(source_lines[i])
                except BadLocalizationException:
                    f.write(source_lines[i])
                    continue
                if key in dest_texts:
                    dest_version = '' if dest_texts[key]['version'] is None else str(dest_texts[key]['version'])
                    f.write(' ' + key + ':' + dest_version + ' "' + dest_texts[key]['value'] + '"\n')
                    del dest_texts[key]
                else:
                    dest_version = '' if version is None else str(version)
                    f.write(' ' + key + ':' + str(dest_version) + ' "' + value + '"\n')
    with open(old_lines_file_path, 'a', encoding='utf8') as f:
        for k, v in dest_texts.items():
            dest_version = '' if v['version'] is None else str(v['version'])
            f.write(' ' + k + ':' + dest_version + ' "' + v['value'] + '"\n')


if __name__ == '__main__':
    args = get_args()
    name_to_dest_path = dict()
    for root, _, files in os.walk(args.dest_dir):
        for file in files:
            name_to_dest_path[file[:file.find('_l_')]] = os.path.abspath(os.path.join(root, file))
    for root, _, files in os.walk(args.source_dir):
        for file in files:
            name = file[:file.find('_l_')]
            if name not in name_to_dest_path:
                print(f'File {name} doesn\'t exists for destination language')
            else:
                add_missing_line(os.path.abspath(os.path.join(root, file)), name_to_dest_path[name],
                                 os.path.abspath(os.path.join(args.dest_dir, '..', 'old_lines.yml')))
