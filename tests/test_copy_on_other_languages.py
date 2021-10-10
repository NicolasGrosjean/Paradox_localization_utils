import os
import shutil
import unittest

from src.copy_on_other_languages import copy_on_other_languages
from tests.utils import get_data_dir


class TestCopyOnOtherLanguages(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(get_data_dir(), "copy_on_other_languages")
        shutil.copytree(os.path.join(self.data_dir, "backup"), os.path.join(self.data_dir, "sandbox"))

    def tearDown(self):
        shutil.rmtree(os.path.join(self.data_dir, "sandbox"))

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
            with open(
                os.path.abspath(os.path.join(self.data_dir, "sandbox", language, f"text_l_{language}.yml")),
                "r",
                encoding="utf8",
            ) as f:
                lines = f.readlines()
            self.assertEqual(lines[0].replace("\n", ""), f"\ufeffl_{language}:")
            self.assertEqual(lines[1].replace("\n", ""), '  KEY:0 "value0"')
            self.assertEqual(lines[2].replace("\n", ""), '  ANOTHERKEY:0 "value42"')
