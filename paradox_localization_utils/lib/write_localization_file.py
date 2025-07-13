from pathlib import Path

from paradox_localization_utils.lib.read_localization_file import BadLocalizationException, get_key_value_and_version


def edit_file_with_dict(localisation_file_path: str | Path, data_to_update: dict[str, str]):
    """Edit a file by replacing lines with keys and values from the provided dictionary.

    :param localisation_file_path: Path of the localization file to edit.
    :param data_to_update: Dict {key: new_text} where key is the localization key and new_text is the new value to set.
    """
    with open(localisation_file_path, "r", encoding="utf8") as f:
        lines = f.readlines()

    with open(localisation_file_path, "w", encoding="utf8") as f:
        for i in range(len(lines)):
            if i == 0:
                # Keep the language definition line
                f.write(lines[0])
            else:
                try:
                    key, value, version = get_key_value_and_version(lines[i])
                    if version is None:
                        version = ""
                    if key in data_to_update and data_to_update[key] != value:
                        f.write(" " + key + ":" + str(version) + ' "' + data_to_update[key] + '"\n')
                    else:
                        f.write(lines[i])
                except BadLocalizationException:
                    f.write(lines[i])
                    continue
