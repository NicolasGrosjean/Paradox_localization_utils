import argparse
import os

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.read_localization_file import get_key, BadLocalizationException


def get_args():
    parser = argparse.ArgumentParser(description='Get the list of duplicates keys ')
    parser.add_argument('directory', type=str, help='Directory in which duplicate keys are searched')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    keys = set()
    for file in os.listdir(args.directory):
        if file.endswith('l_english.yml'):
            with open(os.path.join(args.directory, file), 'r', encoding='utf8') as f:
                lines = f.readlines()
            for line in lines:
                if 'l_english' in line or 'spellcheck_ignore' in line:
                    continue
                try:
                    key = get_key(line)
                    if key in keys:
                        print(f'{key} is duplicated. Found at least once in {file}')
                    keys.add(key)
                except BadLocalizationException:
                    pass
