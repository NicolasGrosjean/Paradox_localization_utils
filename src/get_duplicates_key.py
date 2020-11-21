import argparse
import os

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.read_localization_file import get_key_value_and_version, BadLocalizationException


def get_args():
    parser = argparse.ArgumentParser(description='Get the list of duplicates keys ')
    parser.add_argument('directory', type=str, help='Directory in which duplicate keys are searched')
    parser.add_argument('-only_different_value', action='store_true', help='Print only duplicates key with different value')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    keys_to_values = dict()
    for file in os.listdir(args.directory):
        if file.endswith('l_english.yml'):
            with open(os.path.join(args.directory, file), 'r', encoding='utf8') as f:
                lines = f.readlines()
            for line in lines:
                try:
                    key, value, _ = get_key_value_and_version(line)
                    if 'l_english' in key or 'spellcheck_ignore' in key:
                        continue
                    if key in keys_to_values and (not args.only_different_value or\
                                                  keys_to_values[key] != value):
                        print(f'{key} is duplicated. Found at least once in {file}')
                    keys_to_values[key] = value
                except BadLocalizationException:
                    pass
