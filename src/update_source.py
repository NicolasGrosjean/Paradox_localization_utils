import argparse
import os
import shutil
from time import strftime, gmtime


def get_args():
    parser = argparse.ArgumentParser(description='Update the mod source files')
    parser.add_argument('source_dir', type=str, help='Directory of the mod where it has been updated')
    parser.add_argument('target_dir', type=str, help='Directory of the mod where the source will be updated')
    parser.add_argument('source_lang', type=str, help='Source language')
    return parser.parse_args()


def list_file_to_copy(target_mod_dir):
    res = []
    for root, _, files in os.walk(target_mod_dir):
        for file in files:
            res.append(os.path.join(root, file))
    return res


def get_localisation_dir(mod_dir, source_lang):
    hoi4_loc_dir = os.path.join(mod_dir, 'localisation')
    ck3_loc_dir = os.path.join(mod_dir, 'localization', source_lang)
    if os.path.exists(hoi4_loc_dir):
        return hoi4_loc_dir
    elif os.path.exists(ck3_loc_dir):
        return ck3_loc_dir
    else:
        raise Exception('Localisation directory not found')


def main(args):
    # Compute unzip mod directory
    copied_mod_dir = os.path.join(os.path.join(args.target_dir, '..', strftime("%Y_%m_%d_%H_%M_%S", gmtime())))
    os.makedirs(copied_mod_dir)

    # Copy localisation directory
    loc_dir = get_localisation_dir(args.source_dir, args.source_lang)
    if os.path.basename(loc_dir) == 'localisation':
        shutil.copytree(loc_dir, os.path.join(copied_mod_dir, 'localisation'))
    elif os.path.basename(loc_dir) == args.source_lang:
        shutil.copytree(loc_dir, os.path.join(copied_mod_dir, 'localization', args.source_lang))
    else:
        raise Exception('Invalid source localisation directory')

    # Copy update of mod file in the new directory
    for file in list_file_to_copy(args.target_dir):
        dest = file.replace(args.target_dir, copied_mod_dir)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(file, dest)

    # Remove old source files
    i = 0
    for root, _, files in os.walk(get_localisation_dir(args.target_dir, args.source_lang)):
        for file in files:
            if file.endswith('l_' + args.source_lang + '.yml'):
                i += 1
                os.remove(os.path.join(root, file))
    print('{0} old files removed'.format(i))

    # Copy new source files
    i = 0
    source_loc_dir = get_localisation_dir(copied_mod_dir, args.source_lang)
    target_loc_dir = get_localisation_dir(args.target_dir, args.source_lang)
    for root, _, files in os.walk(source_loc_dir):
        for file in files:
            if file.endswith('l_' + args.source_lang + '.yml'):
                i += 1
                source = os.path.join(root, file)
                dest = source.replace(source_loc_dir, target_loc_dir)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(source, dest)
    print('{0} new files copied'.format(i))


if __name__ == '__main__':
    main(get_args())
