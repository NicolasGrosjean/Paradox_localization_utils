import unittest

import os
import shutil

from src.apply_diff import apply_diff
from tests.utils import get_data_dir


class TestApplyDiff(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join(get_data_dir(), "apply_diff")
        for file in os.listdir(os.path.join(cls.data_dir, "dest")):
            shutil.copyfile(os.path.join(cls.data_dir, "dest", file), os.path.join(cls.data_dir, file))

    def test_apply_diff_same_sources(self):
        old_source = os.path.abspath(os.path.join(self.data_dir, "old_source_0.yml"))
        new_source = os.path.abspath(os.path.join(self.data_dir, "new_source_0.yml"))
        dest = os.path.abspath(os.path.join(self.data_dir, "dest_0.yml"))
        apply_diff(old_source, new_source, dest)
        with open(dest, "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:2 "valeur1"')

    def test_apply_diff_same_sources_unordered_dest(self):
        old_source = os.path.abspath(os.path.join(self.data_dir, "old_source_0.yml"))
        new_source = os.path.abspath(os.path.join(self.data_dir, "new_source_0.yml"))
        dest = os.path.abspath(os.path.join(self.data_dir, "dest_1.yml"))
        apply_diff(old_source, new_source, dest)
        with open(dest, "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), '  KEY0:0 "valeur0"')
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:2 "valeur1"')

    def test_apply_diff_same_sources_with_comments(self):
        old_source = os.path.abspath(os.path.join(self.data_dir, "old_source_2.yml"))
        new_source = os.path.abspath(os.path.join(self.data_dir, "new_source_2.yml"))
        dest = os.path.abspath(os.path.join(self.data_dir, "dest_2.yml"))
        apply_diff(old_source, new_source, dest)
        with open(dest, "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), '  KEY0:0 "valeur0"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY1:2 "valeur1"')

    def test_apply_diff_new_line(self):
        old_source = os.path.abspath(os.path.join(self.data_dir, "old_source_3.yml"))
        new_source = os.path.abspath(os.path.join(self.data_dir, "new_source_2.yml"))
        dest = os.path.abspath(os.path.join(self.data_dir, "dest_3.yml"))
        apply_diff(old_source, new_source, dest)
        with open(dest, "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), '  KEY0:9 "value0"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY1:2 "valeur1"')

    def test_apply_diff_delete_line(self):
        old_source = os.path.abspath(os.path.join(self.data_dir, "old_source_2.yml"))
        new_source = os.path.abspath(os.path.join(self.data_dir, "new_source_4.yml"))
        dest = os.path.abspath(os.path.join(self.data_dir, "dest_4.yml"))
        apply_diff(old_source, new_source, dest)
        with open(dest, "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Events")
        self.assertEqual(lines[2].replace("\n", ""), '  KEY1:2 "valeur1"')

    def test_apply_diff_edited_line(self):
        old_source = os.path.abspath(os.path.join(self.data_dir, "old_source_2.yml"))
        new_source = os.path.abspath(os.path.join(self.data_dir, "new_source_5.yml"))
        dest = os.path.abspath(os.path.join(self.data_dir, "dest_5.yml"))
        apply_diff(old_source, new_source, dest)
        with open(dest, "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), '  KEY0:9 "value42"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY1:2 "valeur1"')

    def test_apply_diff_edited_line_keep_edited(self):
        old_source = os.path.abspath(os.path.join(self.data_dir, "old_source_2.yml"))
        new_source = os.path.abspath(os.path.join(self.data_dir, "new_source_5.yml"))
        dest = os.path.abspath(os.path.join(self.data_dir, "dest_6.yml"))
        apply_diff(old_source, new_source, dest, keep_edited=True)
        with open(dest, "r", encoding="utf8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0].replace("\n", ""), "l_french:")
        self.assertEqual(lines[1].replace("\n", ""), "  # Ideas")
        self.assertEqual(lines[2].replace("\n", ""), '  KEY0:9 "valeur0"')
        self.assertEqual(lines[3].replace("\n", ""), "  ")
        self.assertEqual(lines[4].replace("\n", ""), "  # Events")
        self.assertEqual(lines[5].replace("\n", ""), '  KEY1:2 "valeur1"')
