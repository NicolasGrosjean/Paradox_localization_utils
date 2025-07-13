import argparse
import os
from pathlib import Path
import shutil
import time
from download_paratranz import download_artifact, update_artifact
from extract_paratranz_translation import extract_paratranz_localisation_dir
from paradox_localization_utils.copy_code_only_texts import copy_code_only_texts


def get_args():
    parser = argparse.ArgumentParser(description="Update files to translate on Paratranz")
    parser.add_argument("token", type=str, help="Paratranz API token")
    parser.add_argument("project_id", type=int, help="Id of the project on Paratranz")
    parser.add_argument(
        "loc_dir", type=str, help="Path of the localisation directory where the translation will by written"
    )
    parser.add_argument("language", type=str, help="Destination language")
    parser.add_argument(
        "-steam_loc_dir",
        type=str,
        help="Path of the Steam localisation directory where the translation will by written",
    )
    parser.add_argument(
        "-clean_raw_files",
        action="store_true",
        help="Remove raw files after extraction",
    )
    parser.add_argument(
        "-no-check-dest-lang-dir",
        action="store_true",
        help="Do not stop if loc_dir/language directory doesn't contains file ",
    )
    return parser.parse_args()


def update_files_from_paratranz(
    token: str,
    project_id: int,
    loc_dir: Path,
    dest_language: str,
    steam_loc_dir: str | None,
    clean_raw_files: bool,
    no_check_dest_lang_dir: bool,
) -> None:
    """Update localisation files from Paratranz

    :param token: Paratranz token
    :param project_id: Project ID on Paratranz
    :param loc_dir: Path to the localisation directory where the translation will be written
    :param dest_language: Language to update
    :param steam_loc_dir: Localisation directory for Steam, if None, no files will be copied to Steam
    :param clean_raw_files: Delete raw files after extraction
    """

    # Check loc_dir is set correctly
    if not no_check_dest_lang_dir:
        present_dest_language_files = False
        for _ in Path(loc_dir / dest_language).glob(f"*_{dest_language}.yml"):
            present_dest_language_files = True
            break
        if not present_dest_language_files:
            print("ERROR: Call copy_on_other_languages before")
            exit()

    # download_paratranz
    update_artifact(token, project_id)
    waiting_time = 180
    print(f"Artifacts updated, wait {waiting_time} seconds before downloading")
    time.sleep(waiting_time)
    raw_dir = loc_dir / ".." / "raw"
    utf8_dir = loc_dir / "utf8"
    download_artifact(token, project_id, raw_dir, utf8_dir)
    shutil.rmtree(utf8_dir, ignore_errors=True)

    # extract paratanz
    extract_paratranz_localisation_dir(str(raw_dir.resolve()), dest_language, loc_dir / dest_language, True)
    extract_paratranz_localisation_dir(str(raw_dir.resolve()), dest_language, loc_dir, True)

    # copy code only texts
    copy_code_only_texts(loc_dir, loc_dir, "english", dest_language)

    if steam_loc_dir:
        steam_loc_dir = Path(steam_loc_dir)
        # remove previous files
        shutil.rmtree(steam_loc_dir, ignore_errors=True)

        # copy new files
        for file in loc_dir.rglob(f"*_{dest_language}.yml"):
            new_file = str(file).replace(str(loc_dir), str(steam_loc_dir))
            os.makedirs(os.path.dirname(new_file), exist_ok=True)
            shutil.copy(file, new_file)

    if clean_raw_files:
        shutil.rmtree(raw_dir, ignore_errors=True)


if __name__ == "__main__":
    args = get_args()
    update_files_from_paratranz(
        args.token,
        args.project_id,
        Path(args.loc_dir),
        args.language,
        args.steam_loc_dir,
        args.clean_raw_files,
        args.no_check_dest_lang_dir,
    )
