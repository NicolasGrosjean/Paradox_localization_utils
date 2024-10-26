import argparse
from pathlib import Path
import shutil
import time
from download_paratranz import download_artifact, update_artifact
from extract_paratranz_translation import extract_paratranz_localisation_dir


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
    return parser.parse_args()


def update_files_from_paratranz(token: str, project_id: int, loc_dir: Path, language: str, steam_loc_dir: str | None):
    # Check tmp_loc_dir is set correctly
    present_french_files = False
    for _ in Path(loc_dir / language).glob(f"*_{language}.yml"):
        present_french_files = True
        break
    if not present_french_files:
        print("ERROR: Call copy_on_other_languages before")
        exit()

    # download_paratranz
    update_artifact(token, project_id)
    waiting_time = 20
    print(f"Artifacts updated, wait {waiting_time} seconds before downloading")
    time.sleep(waiting_time)
    raw_dir = loc_dir / ".." / "raw"
    utf8_dir = loc_dir / "utf8"
    download_artifact(token, project_id, raw_dir, utf8_dir)
    shutil.rmtree(utf8_dir, ignore_errors=True)

    # extract paratanz
    extract_paratranz_localisation_dir(str(raw_dir.resolve()), language, loc_dir / language, True)
    extract_paratranz_localisation_dir(str(raw_dir.resolve()), language, loc_dir, True)

    if steam_loc_dir:
        steam_loc_dir = Path(steam_loc_dir)
        # remove previous files
        shutil.rmtree(steam_loc_dir, ignore_errors=True)

        # copy new files
        shutil.copytree(loc_dir / language, steam_loc_dir / language)
        shutil.copytree(loc_dir / "replace", steam_loc_dir / "replace")
        for file in (steam_loc_dir / "replace").glob("*_english.yml"):
            file.unlink()


if __name__ == "__main__":
    args = get_args()
    update_files_from_paratranz(
        args.token, args.project_id, Path(args.loc_dir), args.language, args.steam_loc_dir
    )
