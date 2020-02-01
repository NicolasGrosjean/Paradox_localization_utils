def file_to_keys_and_values(absolute_file_path):
    """
    Extract key and values from a Paradox localization file
    :param absolute_file_path: Absolute file path of a Paradox localization file
    :return: (Dict with localization keys as keys, first line of the file)
    """
    with open(absolute_file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    res = dict()
    for i in range(len(lines)):
        try:
            key, value, version = get_key_value_and_version(lines[i])
            res[key] = {'value': value, 'version': version}
        except BadLocalizationException as e:
            if str(e) == 'Missing double quote' and i > 0:
                print(f'Missing double quote in file {absolute_file_path} line {i} : {lines[i]}')
    return res, lines[0]


def get_key_value_and_version(line):
    """
    Extract the key and value of a string representing the line of a Paradox localization file
    :param line: string representing the line of a Paradox localization file
    :return: (localization key, value corresponding to the localization key, version of the value)
    """
    i = 0
    while i < len(line) and line[i] == ' ':
        i += 1
    if i < len(line) and line[i] == '#':
        raise BadLocalizationException('Comment line')
    split_line = line.split(':')
    if len(split_line) < 2:
        raise BadLocalizationException('No semicolon found')
    key = split_line[0]
    i = 0
    while key[i] == ' ':
        i += 1
    key = key[i:]
    text = split_line[1]
    version = None
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
            text += ':' + split_line[i]
    start = text.find('"') + 1
    end = text.rfind('"')
    if start > end:
        raise BadLocalizationException('Missing double quote')
    text = text[start:end]
    return key, text, version


class BadLocalizationException(Exception):
    pass
