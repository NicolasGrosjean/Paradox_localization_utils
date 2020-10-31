import os
import shutil
import sys
import unittest

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.copy_on_other_languages import copy_on_other_languages


class TestCopyOnOtherLanguages(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join('data', 'copy_on_other_languages')
        shutil.copytree(os.path.join(self.data_dir, 'backup'), os.path.join(self.data_dir, 'sandbox'))

    def tearDown(self):
        shutil.rmtree(os.path.join(self.data_dir, 'sandbox'))

    def test_copy_on_other_languages(self):
        copy_on_other_languages(os.path.join(self.data_dir, 'sandbox'), 'english', ['german', 'korean'])
        with open(os.path.abspath(os.path.join(self.data_dir, 'sandbox', 'french', 'text_l_french.yml')), 'r',
                  encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), 'l_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  KEY:0 "valeur0"')
        self.assertEqual(lines[2].replace('\n', ''), '  ANOTHERKEY:0 "valeur42"')
        for language in ['english', 'german', 'korean']:
            with open(os.path.abspath(os.path.join(self.data_dir, 'sandbox', language, f'text_l_{language}.yml')), 'r',
                      encoding='utf8') as f:
                lines = f.readlines()
            self.assertEqual(lines[0].replace('\n', ''), f'l_{language}:')
            self.assertEqual(lines[1].replace('\n', ''), '  KEY:0 "value0"')
            self.assertEqual(lines[2].replace('\n', ''), '  ANOTHERKEY:0 "value42"')
