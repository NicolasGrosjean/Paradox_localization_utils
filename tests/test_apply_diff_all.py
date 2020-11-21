import unittest

import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.apply_diff_all import apply_diff_all_eu_hoi_stellaris


class TestApplyDiffAll(unittest.TestCase):
    """
    Run apply_diff_all in setUpClass, the tests are only the assert

    Data directory setup:
    data/apply_diff_all/dest : backup of old French files which are copied to data/apply_diff_all/new before tests
    data/apply_diff_all/old : old English files
    data/apply_diff_all/new : new English files and to update French files
    """
    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join('data', 'apply_diff_all')
        for file in os.listdir(os.path.join(cls.data_dir, 'dest')):
            shutil.copyfile(os.path.join(cls.data_dir, 'dest', file), os.path.join(cls.data_dir, 'new', file))
        apply_diff_all_eu_hoi_stellaris(os.path.join(cls.data_dir, 'old'), os.path.join(cls.data_dir, 'new'),
                                        'english', 'french')

    @classmethod
    def tearDownClass(cls):
        for file in os.listdir(os.path.join(cls.data_dir, 'new')):
            if file.endswith('l_french.yml'):
                os.remove(os.path.join(cls.data_dir, 'new', file))

    def test_apply_diff_same_sources(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '0_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace('\n', ''), '  KEY1:2 "valeur1"')

    def test_apply_diff_same_sources_unordered_dest(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '1_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  KEY10:0 "valeur0"')
        self.assertEqual(lines[2].replace('\n', ''), '  KEY11:2 "valeur1"')

    def test_apply_diff_same_sources_with_comments(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '2_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  # Ideas')
        self.assertEqual(lines[2].replace('\n', ''), '  KEY20:0 "valeur0"')
        self.assertEqual(lines[3].replace('\n', ''), '  ')
        self.assertEqual(lines[4].replace('\n', ''), '  # Events')
        self.assertEqual(lines[5].replace('\n', ''), '  KEY21:2 "valeur1"')

    def test_apply_diff_new_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '3_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  # Ideas')
        self.assertEqual(lines[2].replace('\n', ''), ' KEY30:9 "value0"')
        self.assertEqual(lines[3].replace('\n', ''), '  ')
        self.assertEqual(lines[4].replace('\n', ''), '  # Events')
        self.assertEqual(lines[5].replace('\n', ''), '  KEY31:2 "valeur1"')

    def test_apply_diff_delete_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '4_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  # Events')
        self.assertEqual(lines[2].replace('\n', ''), '  KEY41:2 "valeur1"')

    def test_apply_diff_edited_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '5_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  # Ideas')
        self.assertEqual(lines[2].replace('\n', ''), ' KEY50:9 "value01234567891011"')
        self.assertEqual(lines[3].replace('\n', ''), '  ')
        self.assertEqual(lines[4].replace('\n', ''), '  # Events')
        self.assertEqual(lines[5].replace('\n', ''), '  KEY51:2 "valeur1"')

    def test_apply_diff_edited_line_keep_edited(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '6_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  # Ideas')
        self.assertEqual(lines[2].replace('\n', ''), ' KEY60:9 "valeur0"')
        self.assertEqual(lines[3].replace('\n', ''), '  ')
        self.assertEqual(lines[4].replace('\n', ''), '  # Events')
        self.assertEqual(lines[5].replace('\n', ''), '  KEY61:2 "valeur1"')

    def test_apply_diff_non_translated_file(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '7_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), '  # Ideas')
        self.assertEqual(lines[2].replace('\n', ''), ' KEY70:9 "value14"')
        self.assertEqual(lines[3].replace('\n', ''), '  ')
        self.assertEqual(lines[4].replace('\n', ''), '  # Events')
        self.assertEqual(lines[5].replace('\n', ''), '  KEY71:2 "value1"')

    def test_apply_diff_tab_in_key(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '8_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[1].replace('\n', ''), ' game_rule_decisions:0 "Décisions de règles de jeu"')
        self.assertEqual(lines[2].replace('\n', ''), ' early_tagswitch_decision:0 "Jouer en tant que [From.GetNameDef]"')

    def test_apply_diff_bug_no_change(self):
        with open(os.path.abspath(os.path.join(self.data_dir, 'new', '9_l_french.yml')), 'r', encoding='utf8') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace('\n', ''), '\ufeffl_french:')
        self.assertEqual(lines[29].replace('\n', ''), ' twosun_missile:9 "Les Laboratoires de Missiles"')
