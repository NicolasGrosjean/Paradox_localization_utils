import argparse
import json
import os

from src.read_localization_file import get_key_value_and_version, BadLocalizationException


def get_args():
    parser = argparse.ArgumentParser(description='Extract translation Paratranz file')
    parser.add_argument('paratranz_dir', type=str, help='Directory with JSON Paratranz files')
    parser.add_argument('localisation_dir', type=str, help='Directory with Paradox files to edit')
    parser.add_argument('language', type=str, help='Language of the Paradox files to edit')
    return parser.parse_args()


def extract_paratranz_localisation(paratranz_file_path: str, localisation_file_path: str):
    with open(paratranz_file_path, 'r', encoding='utf8') as f:
        raw_paratranz_data = json.load(f)
    paratranz_data = dict()
    for line in raw_paratranz_data:
        if len(line['translation']) > 0:
            paratranz_data[line['key'].split(':')[0]] = line['translation']

    with open(localisation_file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    with open(localisation_file_path, 'w', encoding='utf8') as f:
        for i in range(len(lines)):
            if i == 0:
                # Keep the language definition line
                f.write(lines[0])
            else:
                try:
                    key, value, version = get_key_value_and_version(lines[i])
                    if key in paratranz_data:
                        f.write(' ' + key + ':' + str(version) + ' "' + paratranz_data[key] + '"\n')
                    else:
                        f.write(lines[i])
                except BadLocalizationException:
                    f.write(lines[i])
                    continue


if __name__ == '__main__':
    args = get_args()
    for file in os.listdir(args.paratranz_dir):
        if file.endswith('.json'):
            loc_file_name = file[:file.index('_l_')] + '_l_' + args.language + '.yml'
            extract_paratranz_localisation(os.path.join(args.paratranz_dir, file),
                                           os.path.join(args.localisation_dir, loc_file_name))
