import os
import shutil
import unittest

from paradox_localization_utils.copy_on_other_languages import copy_on_other_languages
from tests.utils import get_data_dir


class TestCopyOnOtherLanguages(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(get_data_dir(), "copy_on_other_languages")
        shutil.copytree(os.path.join(self.data_dir, "backup"), os.path.join(self.data_dir, "sandbox"))

    def tearDown(self):
        shutil.rmtree(os.path.join(self.data_dir, "sandbox"))

    def assert_file_content(self, file_path: str, language: str, suffix: str):
        with open(
            os.path.abspath(file_path),
            "r",
            encoding="utf8",
        ) as f:
            lines = f.readlines()
        i = 0
        if suffix == "2":
            self.assertEqual(lines[0].replace("\n", ""), "\ufeff# Comment in the first line")
            self.assertEqual(lines[1].replace("\n", ""), "")
            self.assertEqual(lines[2].replace("\n", ""), f"l_{language}:")
            i = 2
        else:
            self.assertEqual(lines[0].replace("\n", ""), f"\ufeffl_{language}:")
        self.assertEqual(lines[i + 1].replace("\n", ""), '  KEY:0 "value0"')
        self.assertEqual(lines[i + 2].replace("\n", ""), '  ANOTHERKEY:0 "value42"')

    def test_copy_on_other_languages(self):
        copy_on_other_languages(os.path.join(self.data_dir, "sandbox"), "english", ["german", "korean"])
        with open(
            os.path.abspath(os.path.join(self.data_dir, "sandbox", "french", "text_l_french.yml")),
            "r",
            encoding="utf8",
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  ANOTHERKEY:0 "valeur42"')
        for language in ["english", "german", "korean"]:
            for suffix in ["", "2"]:
                self.assert_file_content(
                    os.path.join(self.data_dir, "sandbox", language, f"text{suffix}_l_{language}.yml"),
                    language,
                    suffix,
                )
            self.assert_file_content(
                os.path.join(self.data_dir, "sandbox", f"text_in_root_l_{language}.yml"), language, ""
            )
