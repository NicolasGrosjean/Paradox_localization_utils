import unittest

import os
import shutil

from tests.utils import get_data_dir
from src.apply_diff_all import DELETED_LINES_FILE_NAME, apply_diff_all_eu_hoi_stellaris


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
        cls.data_dir = os.path.join(get_data_dir(), "apply_diff_all")
        for file in os.listdir(os.path.join(cls.data_dir, "dest")):
            shutil.copyfile(os.path.join(cls.data_dir, "dest", file), os.path.join(cls.data_dir, "new", file))
        apply_diff_all_eu_hoi_stellaris(
            os.path.join(cls.data_dir, "old"), os.path.join(cls.data_dir, "new"), "english", "french"
        )

    @classmethod
    def tearDownClass(cls):
        for file in os.listdir(os.path.join(cls.data_dir, "new")):
            if file.endswith("l_french.yml"):
                os.remove(os.path.join(cls.data_dir, "new", file))
        if os.path.exists(f"french_{DELETED_LINES_FILE_NAME}"):
            os.remove(f"french_{DELETED_LINES_FILE_NAME}")
        if os.path.exists(f"english_{DELETED_LINES_FILE_NAME}"):
            os.remove(f"english_{DELETED_LINES_FILE_NAME}")

    def test_apply_diff_same_sources(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "0_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:2 "valeur1"')

    def test_apply_diff_same_sources_unordered_dest(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "1_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY10:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY11:2 "valeur1"')

    def test_apply_diff_same_sources_with_comments(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "2_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), '  KEY20:0 "valeur0"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY21:2 "valeur1"')

    def test_apply_diff_new_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "3_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' KEY30:0Z "value of a new key"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY31:2 "valeur1"')

    def test_apply_diff_delete_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "4_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), " 	#1010 — 1031: Foreign Relations (Invite a foreign ruler to your court), by Mathilda Bjarnehed")
        self.assertEqual(lines[2].replace("\n", ""), '  KEY41:2 "valeur1"')
        with open(f"french_{DELETED_LINES_FILE_NAME}") as f:
            lines = f.readlines()
        self.assertEqual(1, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), '  KEY40:0 "valeur0"')
        with open(f"english_{DELETED_LINES_FILE_NAME}") as f:
            lines = f.readlines()
        self.assertEqual(1, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), ' KEY40:0 "value0"')

    def test_apply_diff_edited_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "5_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' KEY50:1 "valeur0" #ZX Comment to keep')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY51:2 "valeur1" #ZX Another comment to keep')

    def test_apply_diff_edited_line_keep_edited(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "6_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' KEY60:1 "valeur0"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY61:2 "valeur1"')

    def test_apply_diff_non_translated_file(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "7_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' KEY70:1 "value0"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY71:2 "value1"')

    def test_apply_diff_tab_in_key(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "8_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), ' game_rule_decisions:0 "Décisions de règles de jeu"')
        self.assertEqual(
            lines[2].replace("\n", ""), ' early_tagswitch_decision:0 "Jouer en tant que [From.GetNameDef]"'
        )

    def test_apply_diff_file_one_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "9_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
            self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")

    def test_apply_diff_comment_first(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "10_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeff######################################")
        self.assertEqual(lines[13].replace("\n", ""), "l_french:")
        self.assertEqual(lines[14].replace("\n", ""), '  dislikes_big_mt:0 "N\'aime pas le Big MT"')

    def test_apply_diff_new_line_but_existing_translation(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "11_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' New_translation:0Q "Déjà traduit"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  Existing_translation:2 "Déjà traduit"')

    def test_apply_diff_same_sources_but_spaces_in_lang_declaration(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "12_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY120:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY121:2 "valeur1"')

    def test_apply_diff_new_file(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "13_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' NEW_KEY0:0Z "Value of new file"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), ' NEW_KEY1:2Z "Value of new file 2"')

    def test_apply_diff_new_line(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "14_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' NEW_KEY_W_VERSION:Z "value of a new key without version"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY_W_VERSION: "clef sans version"')

    def test_apply_diff_new_line_with_comment(self):
        with open(os.path.abspath(os.path.join(self.data_dir, "new", "15_l_french.yml")), "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), ' KEY150:0Z "value of a new key" #comment to keep')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY151:2 "valeur1"')
