import argparse
from pathlib import Path
import re

from paradox_localization_utils.lib.read_localization_file import file_to_keys_and_values
from paradox_localization_utils.lib.write_localization_file import edit_file_with_dict

CODE_ONLY_REGEX = re.compile(r"(\[[^\]]+\]\s*)+")


def get_args():
    parser = argparse.ArgumentParser(description="Copy texts which are only code from source to destination")
    parser.add_argument("source_dir", type=str, help="Directory with source Paradox files")
    parser.add_argument("dest_dir", type=str, help="Directory with destination/target Paradox files")
    parser.add_argument("-source_lang", type=str, help="Source language")
    parser.add_argument("-dest_lang", type=str, help="Destination/target language")
    return parser.parse_args()


def extract_code_only_texts(source_dir: Path, source_lang: str) -> dict[str, str]:
    res: dict[str, str] = dict()
    for file_path in source_dir.rglob(f"*l_{source_lang}.yml"):
        keys_and_values_versions, _ = file_to_keys_and_values(file_path)
        for key, value_and_version in keys_and_values_versions.items():
            if re.fullmatch(CODE_ONLY_REGEX, value_and_version["value"]):
                res[key] = value_and_version["value"]
    return res


def copy_code_only_texts(source_dir: Path, dest_dir: Path, source_lang: str, dest_lang: str):
    code_only_sources = extract_code_only_texts(source_dir, source_lang)
    for file_path in dest_dir.rglob(f"*l_{dest_lang}.yml"):
        edit_file_with_dict(file_path, code_only_sources)


if __name__ == "__main__":
    args = get_args()
    copy_code_only_texts(Path(args.source_dir), Path(args.dest_dir), args.source_lang, args.dest_lang)
