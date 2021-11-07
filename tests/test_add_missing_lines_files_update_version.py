import unittest

import os
import shutil

from src.add_missing_lines_files_update_version import add_missing_lines_files_update_version
from tests.utils import get_data_dir


class TestAddMissingLinesFilesUpdateVersion(unittest.TestCase):
    """
    Run add_missing_lines_files_update_version in setUpClass, the tests are only the assert

    Data directory setup:
    data/add_missing_lines_files_update_version/old: backup of old English files which are copied to data/add_missing_lines_files_update_version/target before tests
    data/add_missing_lines_files_update_version/new: new English files
    """

    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join(get_data_dir(), "add_missing_lines_files_update_version")
        for file in os.listdir(os.path.join(cls.data_dir, "old")):
            if file != "subdir":
                shutil.copyfile(os.path.join(cls.data_dir, "old", file), os.path.join(cls.data_dir, "target", file))
        for file in os.listdir(os.path.join(cls.data_dir, "old", "subdir")):
            shutil.copyfile(os.path.join(cls.data_dir, "old", "subdir", file), os.path.join(cls.data_dir, "target", "subdir", file))
        add_missing_lines_files_update_version(os.path.join(cls.data_dir, "target"), os.path.join(cls.data_dir, "new"))

    @classmethod
    def tearDownClass(cls):
        for file in os.listdir(os.path.join(cls.data_dir, "target")):
            if file.endswith(".yml"):
                os.remove(os.path.join(cls.data_dir, "target", file))
        for file in os.listdir(os.path.join(cls.data_dir, "target", "subdir")):
            if file.endswith(".yml"):
                os.remove(os.path.join(cls.data_dir, "target", "subdir", file))
        if os.path.exists(os.path.join(cls.data_dir, "target", "new_dir")):
            shutil.rmtree(os.path.join(cls.data_dir, "target", "new_dir"))

    def test_no_change(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "0_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(3, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY0:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY1:2 "value1"')

    def test_added_line(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "1_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(3, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY10:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY11:2 "value1"')

    def test_removed_line(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "2_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(3, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY20:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY21:2 "value1"')

    def test_updated_line(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "3_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(3, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY30:1 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY31:2 "value1"')

    def test_added_file(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "4_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(3, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY40:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY41:2 "value1"')

    def test_removed_file(self):
        self.assertFalse(os.path.exists(os.path.abspath(os.path.join(self.data_dir, "target", "5_l_english.yml"))))

    def test_moved_line(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "6_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(4, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY60:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY71:1 "moved line"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY62:2 "value2"')
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "7_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(3, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY70:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY72:2 "value1"')

    def test_all_actions_subdir(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "subdir", "0_l_english.yml")), "r", encoding="utf8"
        ) as f:
            lines = f.readlines()
        self.assertEqual(4, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' KEY80:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' KEY82:1 "value2"')
        self.assertEqual(lines[3].replace("\n", ""), ' KEY83:0 "value3"')

    def test_added_file_and_dir(self):
        with open(
            os.path.abspath(os.path.join(self.data_dir, "target", "new_dir", "new_file_l_english.yml")),
            "r",
            encoding="utf8",
        ) as f:
            lines = f.readlines()
        self.assertEqual(3, len(lines))
        self.assertEqual(lines[0].replace("\n", ""), "\ufeffl_english:")
        self.assertEqual(lines[1].replace("\n", ""), ' NEWKEY0:0 "value0"')
        self.assertEqual(lines[2].replace("\n", ""), ' NEWKEY1:2 "value1"')
