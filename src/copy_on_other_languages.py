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

        # Copy English directory
        shutil.copytree(os.path.join(localisation_dir, source_lang), os.path.join(localisation_dir, dest_lang))


        # Edit copied files
        for root, _, files in os.walk(os.path.join(localisation_dir, dest_lang)):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                with open(os.path.join(root, file.replace(f'{source_lang}.yml', f'{dest_lang}.yml')), 'w',
                          encoding='utf-8') as f:
                    f.write(f'\ufeffl_{dest_lang}:\n')
                    for i in range(1, len(lines)):
                        f.write(lines[i])
                os.remove(os.path.join(root, file))


if __name__ == '__main__':
    copy_on_other_languages(sys.argv[1], sys.argv[2], sys.argv[3:])
