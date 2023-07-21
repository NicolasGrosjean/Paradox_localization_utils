import logging
import os
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
        # Delete destination directories if they exist
        shutil.rmtree(os.path.join(localisation_dir, dest_lang), ignore_errors=True)

        # Copy source directory
        shutil.copytree(os.path.join(localisation_dir, source_lang), os.path.join(localisation_dir, dest_lang))

        # Edit copied files
        for root, _, files in os.walk(os.path.join(localisation_dir, dest_lang)):
            for file in files:
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    try:
                        lines = f.readlines()
                    except UnicodeDecodeError as e:
                        logging.error(f"Error when parsing {file}")
                        logging.exception(e)
                        continue
                with open(
                    os.path.join(root, file.replace(f"{source_lang}.yml", f"{dest_lang}.yml")), "w", encoding="utf-8"
                ) as f:
                    i = 0
                    while f"l_{source_lang}:" not in lines[i]:
                        f.write(lines[i])
                        i += 1
                    if i == 0:
                        bom_or_not = "\ufeff"
                    else:
                        bom_or_not = ""
                    f.write(f"{bom_or_not}l_{dest_lang}:\n")
                    f.writelines(lines[i + 1 :])
                os.remove(os.path.join(root, file))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    copy_on_other_languages(sys.argv[1], sys.argv[2], sys.argv[3:])
