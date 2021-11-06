import os
import shutil
import unittest

from src.extract_existing_translation import extract_existing_translation
from tests.utils import get_data_dir


class TestExtractExistingTranslation(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(get_data_dir(), "extract_existing_translation")
        if os.path.exists(os.path.join(self.data_dir, "target")):
            shutil.rmtree(os.path.join(self.data_dir, "target"))
            os.makedirs(os.path.join(self.data_dir, "target"))
        print(os.path.exists(os.path.join(self.data_dir, "target")))
        for file in os.listdir(os.path.join(self.data_dir, "original")):
            shutil.copyfile(os.path.join(self.data_dir, "original", file), os.path.join(self.data_dir, "target", file))

    def test_extract_existing_ck2_translations(self):
        extract_existing_translation(
            os.path.join(self.data_dir, "ck2"),
            os.path.join(self.data_dir, "ck2"),
            os.path.join(self.data_dir, "target"),
            os.path.join(self.data_dir, "target"),
            "english",
            "french",
            1,
            2,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "target_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY0:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY1:0 "valeur1"')

    def test_extract_existing_hoi4_translations(self):
        extract_existing_translation(
            os.path.join(self.data_dir, "hoi4"),
            os.path.join(self.data_dir, "hoi4"),
            os.path.join(self.data_dir, "target"),
            os.path.join(self.data_dir, "target"),
            "english",
            "french",
            1,
            2,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "target_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:2 "value1"')
