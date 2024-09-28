import os
import random
import string


class DataDirNotFoundException(Exception):
    pass


def get_data_dir() -> str:
    if os.path.exists("data"):
        return "data"
    elif os.path.exists(os.path.join("tests", "data")):
        return os.path.join("tests", "data")
    else:
        raise DataDirNotFoundException()


def generate_random_str(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))
