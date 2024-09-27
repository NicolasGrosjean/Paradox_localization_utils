import os
import shutil
import unittest

from paradox_localization_utils.extract_paratranz_translation import (
    extract_paratranz_localisation,
    extract_paratranz_localisation_dir,
)
from tests.utils import get_data_dir


class TestExtractParatranzTranslation(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(get_data_dir(), "extract_paratranz_translation")
        self.localisation_dir = os.path.join(self.data_dir, "target")
        if os.path.exists(self.localisation_dir):
            shutil.rmtree(self.localisation_dir)
            os.makedirs(self.localisation_dir)

    def test_extract_basic_paratranz_translation(self):
        shutil.copyfile(
            os.path.join(self.data_dir, "original", "text_l_french.yml"),
            os.path.join(self.data_dir, "target", "new_text_l_french.yml"),
        )
        extract_paratranz_localisation(
            os.path.join(self.data_dir, "new_text_l_french.yml.json"),
            os.path.join(self.localisation_dir, "new_text_l_french.yml"),
            False,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "new_text_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY2:0 "valeur2"')

    def test_extract_paratranz_translation_with_key_issue(self):
        shutil.copyfile(
            os.path.join(self.data_dir, "original", "text_l_french.yml"),
            os.path.join(self.data_dir, "target", "new_text2_l_french.yml"),
        )
        extract_paratranz_localisation(
            os.path.join(self.data_dir, "new_text2_l_french.yml.json"),
            os.path.join(self.localisation_dir, "new_text2_l_french.yml"),
            False,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "new_text2_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY2:0 "valeur2"')

    def test_extract_paratranz_translation_with_non_translation(self):
        shutil.copyfile(
            os.path.join(self.data_dir, "original", "text_l_french.yml"),
            os.path.join(self.data_dir, "target", "new_text3_l_french.yml"),
        )
        extract_paratranz_localisation(
            os.path.join(self.data_dir, "new_text3_l_french.yml.json"),
            os.path.join(self.localisation_dir, "new_text3_l_french.yml"),
            False,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "new_text3_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY2:0 "valeur2"')

    def test_extract_paratranz_translation_with_translation_not_reviewed(self):
        shutil.copyfile(
            os.path.join(self.data_dir, "original", "text_l_french.yml"),
            os.path.join(self.data_dir, "target", "new_text4_l_french.yml"),
        )
        extract_paratranz_localisation(
            os.path.join(self.data_dir, "new_text4_l_french.yml.json"),
            os.path.join(self.localisation_dir, "new_text4_l_french.yml"),
            True,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "new_text4_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY2:0 "valeur2"')

    def test_extract_paratranz_translation_with_translation_not_reviewed2(self):
        shutil.copyfile(
            os.path.join(self.data_dir, "original", "text_l_french.yml"),
            os.path.join(self.data_dir, "target", "new_text4_l_french.yml"),
        )
        extract_paratranz_localisation(
            os.path.join(self.data_dir, "new_text4_l_french.yml.json"),
            os.path.join(self.localisation_dir, "new_text4_l_french.yml"),
            False,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "new_text4_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY0:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY2:0 "valeur2"')

    def test_extract_paratranz_translation_with_l(self):
        shutil.copyfile(
            os.path.join(self.data_dir, "original", "text_l_french.yml"),
            os.path.join(self.data_dir, "target", "new_l_text5_l_french.yml"),
        )
        extract_paratranz_localisation_dir(
            os.path.abspath(os.path.join(self.data_dir, "paratranz_dir2")),
            "french",
            self.localisation_dir,
            False,
        )
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "new_l_text5_l_french.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY2:0 "valeur2"')
