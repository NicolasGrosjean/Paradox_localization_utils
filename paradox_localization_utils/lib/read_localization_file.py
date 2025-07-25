from pathlib import Path


def file_to_keys_and_values(absolute_file_path: str | Path) -> tuple[dict[str, dict[str, str | int | None]], str]:
    """
    Extract key and values from a Paradox localization file
    :param absolute_file_path: Absolute file path of a Paradox localization file
    :return: (Dict with localization keys as keys, first line of the file)
    """
    with open(absolute_file_path, "r", encoding="utf8") as f:
        lines = f.readlines()
    if len(lines) == 0:
        return dict(), ""
    res: dict[str, dict[str, str]] = dict()
    for i in range(len(lines)):
        try:
            key, value, version = get_key_value_and_version(lines[i])
            res[key] = {"value": value, "version": version}
        except BadLocalizationException as e:
            if str(e) == "Missing double quote" and i > 0:
                print(f"Missing double quote in file {absolute_file_path} line {i} : {lines[i]}")
    return res, lines[0]


def file_to_keys_and_lines(absolute_file_path: str | Path) -> tuple[dict[str, str], str]:
    """
    Extract key and lines from a Paradox localization file
    :param absolute_file_path: Absolute file path of a Paradox localization file
    :return: (Dict with localization keys as keys and lines as values, first line of the file)
    """
    with open(absolute_file_path, "r", encoding="utf8") as f:
        lines = f.readlines()
    res: dict[str, str] = dict()
    for i in range(1, len(lines)):
        try:
            key = get_key(lines[i])
            res[key] = lines[i]
        except BadLocalizationException as e:
            if str(e) == "Missing double quote" and i > 0:
                print(f"Missing double quote in file {absolute_file_path} line {i} : {lines[i]}")
    return res, lines[0]


def get_key_value_and_version(line: str) -> tuple[str, str, int | None]:
    """
    Extract the key, the value and the version of a string representing the line of a Paradox localization file
    :param line: string representing the line of a Paradox localization file
    :return: (localization key, value corresponding to the localization key, version of the value)
    """
    i = 0
    while i < len(line) and (line[i] == " " or line[i] == "\t"):
        i += 1
    if i < len(line) and line[i] == "#":
        raise BadLocalizationException("Comment line")
    split_line = line.split(":")
    if len(split_line) < 2:
        raise BadLocalizationException("No semicolon found")
    key = split_line[0][i:]
    text = split_line[1]
    version = None
    if len(text) > 0:
        i = 0
        while text[i].isdigit():
            if version is None:
                version = int(text[i])
            else:
                version = 10 * version + int(text[i])
            i += 1
        text = text[i:]
    if len(split_line) > 2:
        for i in range(2, len(split_line)):
            text += ":" + split_line[i]
    start = text.find('"') + 1
    end = text.rfind('"')
    if start > end:
        raise BadLocalizationException("Missing double quote")
    text = text[start:end]
    return key, text, version


def get_key(line: str) -> str:
    """
    Extract the key of a string representing the line of a Paradox localization file
    :param line: string representing the line of a Paradox localization file
    :return: (localization key, value corresponding to the localization key, version of the value)
    """
    i = 0
    while i < len(line) and (line[i] == " " or line[i] == "\t" or line[i] == "\ufeff"):
        i += 1
    if i < len(line) and line[i] == "#":
        raise BadLocalizationException("Comment line")
    split_line = line.split(":")
    if len(split_line) < 2:
        raise BadLocalizationException("No semicolon found")
    key = split_line[0]
    i = 0
    while key[i] == " " or key[i] == "\t":
        i += 1
    return key[i:]


class BadLocalizationException(Exception):
    pass
