import logging
import os
from pathlib import Path
import shutil
import sys


def copy_on_other_languages(localisation_dir, source_lang, dest_langs):
    """
    Copy the localisation files from source_lang to to all dest_langs by adapting format.
    :param localisation_dir: Localisation directory where the files are
    :param source_lang:
    :param dest_langs:
    :return:
    """
    for dest_lang in dest_langs:
        source_loc_dir = os.path.join(localisation_dir, source_lang)
        dest_loc_dir = os.path.join(localisation_dir, dest_lang)

        # Delete destination directories and files if they exist
        shutil.rmtree(dest_loc_dir, ignore_errors=True)
        for file in Path(localisation_dir).rglob(f"*_{dest_lang}.yml"):
            file.unlink()

        # Copy source directory
        for file in Path(localisation_dir).rglob(f"*_{source_lang}.yml"):
            os.makedirs(os.path.dirname(str(file).replace(source_loc_dir, dest_loc_dir)), exist_ok=True)
            shutil.copy(
                file,
                str(file).replace(source_loc_dir, dest_loc_dir).replace(f"_{source_lang}.yml", f"_{dest_lang}.yml"),
            )

        # Edit copied files
        for file in Path(localisation_dir).rglob(f"*_{dest_lang}.yml"):
            with open(file, "r", encoding="utf-8") as f:
                try:
                    lines = f.readlines()
                except UnicodeDecodeError as e:
                    logging.error(f"Error when parsing {file}")
                    logging.exception(e)
                    continue
            with open(file, "w", encoding="utf-8") as f:
                # Copy all lines until the line with l_<lang>:
                i = 0
                while i < len(lines) and f"l_{source_lang}:" not in lines[i]:
                    f.write(lines[i])
                    i += 1

                if i == len(lines):
                    logging.warning(f"File {file} does not contain l_{dest_lang}:")
                    continue

                # Write the line with l_<lang>:
                if i == 0:
                    bom_or_not = "\ufeff"
                else:
                    bom_or_not = ""
                f.write(f"{bom_or_not}l_{dest_lang}:\n")

                # Write the rest of the lines:
                f.writelines(lines[i + 1 :])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    copy_on_other_languages(sys.argv[1], sys.argv[2], sys.argv[3:])
