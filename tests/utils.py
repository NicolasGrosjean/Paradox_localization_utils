import os


class DataDirNotFoundException(Exception):
    pass


def get_data_dir():
    if os.path.exists("data"):
        return "data"
    elif os.path.exists(os.path.join("tests", "data")):
        return os.path.join("tests", "data")
    else:
        raise DataDirNotFoundException()
