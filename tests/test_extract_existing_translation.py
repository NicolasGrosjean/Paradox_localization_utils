import os
import shutil
import sys
import unittest

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.extract_existing_translation import extract_existing_translation


class TestApplyDiff(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join('data', 'extract_existing_translation')
        for file in os.listdir(os.path.join(cls.data_dir, 'original')):
            shutil.copyfile(os.path.join(cls.data_dir, 'original', file), os.path.join(cls.data_dir, 'target', file))

    def test_extract_existing_ck2_translations(self):
        extract_existing_translation(os.path.join(self.data_dir, 'ck2'), os.path.join(self.data_dir, 'ck2'),
                                     os.path.join(self.data_dir, 'target'), os.path.join(self.data_dir, 'target'),
                                     'english', 'french', 1, 2)
        with open(os.path.abspath(os.path.join(self.data_dir, 'target', 'target_l_french.yml')), 'r',
                  encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), 'l_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  KEY0:0 "value0"')
        self.assertEqual(lines[2].replace('\n', ''), ' KEY1:0 "valeur1"')

    def test_extract_existing_hoi4_translations(self):
        extract_existing_translation(os.path.join(self.data_dir, 'hoi4'), os.path.join(self.data_dir, 'hoi4'),
                                     os.path.join(self.data_dir, 'target'), os.path.join(self.data_dir, 'target'),
                                     'english', 'french', 1, 2)
        with open(os.path.abspath(os.path.join(self.data_dir, 'target', 'target_l_french.yml')), 'r',
                  encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), 'l_french:')
        self.assertEqual(lines[1].replace('\n', ''), ' KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace('\n', ''), '  KEY1:2 "value1"')
