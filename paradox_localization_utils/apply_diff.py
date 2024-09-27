import argparse

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from paradox_localization_utils.read_localization_file import (
    file_to_keys_and_lines,
    get_key_value_and_version,
    BadLocalizationException,
    file_to_keys_and_values,
)


def get_args():
    parser = argparse.ArgumentParser(description="Apply diff in source to destination")
    parser.add_argument("old_source_file", type=str, help="Source file before modifications")
    parser.add_argument("new_source_file", type=str, help="Source file after modifications")
    parser.add_argument("dest_file", type=str, help="Destination file to override")
    parser.add_argument("-space_prefix", type=str, help="Prefix (generally spaces) before key to add in dest file")
    parser.add_argument("-keep_edited", action="store_true", help="Keep destination value if source has been edited")
    return parser.parse_args()


def apply_diff(old_source_file, new_source_file, dest_file, space_prefix="  ", keep_edited=False):
    dest_texts, dest_first_line = file_to_keys_and_lines(dest_file)
    dest_values, _ = file_to_keys_and_values(dest_file)
    old_source_texts, _ = file_to_keys_and_lines(old_source_file)
    old_source_values, _ = file_to_keys_and_values(old_source_file)

    with open(new_source_file, "r", encoding="utf8") as f:
        source_lines = f.readlines()

    with open(dest_file, "w", encoding="utf8") as f:
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
                    if key in old_source_texts and old_source_values[key]["value"] == value:
                        f.write(dest_texts[key])
                    elif keep_edited:
                        f.write(space_prefix + key + ':9 "' + dest_values[key]["value"] + '"\n')
                    else:
                        f.write(space_prefix + key + ':9 "' + value + '"\n')
                else:
                    f.write(space_prefix + key + ':9 "' + value + '"\n')


if __name__ == "__main__":
    args = get_args()
    space_prefix = args.space_prefix
    if space_prefix is None:
        space_prefix = " "
    apply_diff(args.old_source_file, args.new_source_file, args.dest_file, space_prefix, args.keep_edited)
