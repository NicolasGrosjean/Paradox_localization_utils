import os
import shutil
import sys
import unittest

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.extract_paratranz_translation import extract_paratranz_localisation


class TestExtractParatranzTranslation(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join('data', 'extract_paratranz_translation')
        self.localisation_dir = os.path.join(self.data_dir, 'target')
        shutil.rmtree(self.localisation_dir)
        os.makedirs(self.localisation_dir)

    def test_extract_basic_paratranz_translation(self):
        shutil.copyfile(os.path.join(self.data_dir, 'original', 'text_l_french.yml'),
                        os.path.join(self.data_dir, 'target', 'new_text_l_french.yml'))
        extract_paratranz_localisation(os.path.join(self.data_dir, 'new_text_l_french.yml.json'),
                                       os.path.join(self.localisation_dir, 'new_text_l_french.yml'))
        with open(os.path.abspath(os.path.join(self.data_dir, 'target', 'new_text_l_french.yml')), 'r',
                  encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), 'l_french:')
        self.assertEqual(lines[1].replace('\n', ''), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace('\n', ''), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace('\n', ''), ' KEY2:0 "valeur2"')

    def test_extract_paratranz_translation_with_key_issue(self):
        shutil.copyfile(os.path.join(self.data_dir, 'original', 'text_l_french.yml'),
                        os.path.join(self.data_dir, 'target', 'new_text2_l_french.yml'))
        extract_paratranz_localisation(os.path.join(self.data_dir, 'new_text2_l_french.yml.json'),
                                       os.path.join(self.localisation_dir, 'new_text2_l_french.yml'))
        with open(os.path.abspath(os.path.join(self.data_dir, 'target', 'new_text2_l_french.yml')), 'r',
                  encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), 'l_french:')
        self.assertEqual(lines[1].replace('\n', ''), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace('\n', ''), '  KEY1:0 "value1"')
        self.assertEqual(lines[3].replace('\n', ''), ' KEY2:0 "valeur2"')
