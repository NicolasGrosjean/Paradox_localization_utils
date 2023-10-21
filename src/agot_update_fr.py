from pathlib import Path
import shutil
import time
from download_paratranz import download_artifact, update_artifact
from extract_paratranz_translation import extract_paratranz_localisation_dir

paratranz_token = "ChangeMe"
paratranz_project_id = 6833
paratranz_dir = "ChangeMe"
tmp_loc_dir = "ChangeMe"
dest_dir = "ChangeMe"

if __name__ == "__main__":
    # Check tmp_loc_dir is set correctly
    present_french_files = False
    for file in Path(tmp_loc_dir).glob("*_french.yml"):
        present_french_files = True
        break
    if not present_french_files:
        print("ERROR: Call copy_on_other_languages AGOT before")
        exit()

    # download_paratranz
    update_artifact(paratranz_token, paratranz_project_id)
    waiting_time = 20
    print(f"Artifacts updated, wait {waiting_time} seconds before downloading")
    time.sleep(waiting_time)
    download_artifact(paratranz_token, paratranz_project_id, paratranz_dir, "D:\\Documents\\0tmp\\utf8")

    # extract paratanz
    extract_paratranz_localisation_dir(paratranz_dir, "french", tmp_loc_dir, True)

    # remove previous files
    shutil.rmtree(dest_dir, ignore_errors=True)

    # copy new files
    shutil.copytree(tmp_loc_dir, dest_dir)