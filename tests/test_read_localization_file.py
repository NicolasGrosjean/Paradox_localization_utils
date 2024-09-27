import unittest

import os
from paradox_localization_utils.read_localization_file import (
    get_key_value_and_version,
    BadLocalizationException,
    file_to_keys_and_values,
)
from tests.utils import get_data_dir


class TestReadLocalizationFile(unittest.TestCase):
    def test_get_key_and_value(self):
        self.assertEqual("key", get_key_value_and_version('key: "value"')[0])
        self.assertEqual("value", get_key_value_and_version('key: "value"')[1])
        self.assertIsNone(get_key_value_and_version('key: "value"')[2])
        self.assertEqual("key", get_key_value_and_version('key:0 "value"')[0])
        self.assertEqual("value", get_key_value_and_version('key:0 "value"')[1])
        self.assertEqual(0, get_key_value_and_version('key:0 "value"')[2])
        self.assertEqual("key", get_key_value_and_version(' key: "value"')[0])
        self.assertEqual("value", get_key_value_and_version(' key: "value"')[1])
        self.assertEqual("key", get_key_value_and_version('  key: "value"')[0])
        self.assertEqual("value", get_key_value_and_version('  key: "value"')[1])
        self.assertEqual("value #Tcool#!", get_key_value_and_version('key:0 "value #Tcool#!"')[1])
        self.assertEqual("value1:value2", get_key_value_and_version('key:0 "value1:value2"')[1])
        self.assertEqual("value1:value2", get_key_value_and_version('key:0 "value1:value2" #comment')[1])
        self.assertEqual("value1:value2", get_key_value_and_version('key:0 "value1:value2" #comment')[1])
        self.assertEqual("value1:value2", get_key_value_and_version('key:0 "value1:value2" #comment:a')[1])
        self.assertEqual("value1:value2 #!", get_key_value_and_version('key:0 "value1:value2 #!"')[1])
        self.assertEqual(42, get_key_value_and_version('key:42 "value"')[2])
        try:
            get_key_value_and_version("")
            self.fail()
        except BadLocalizationException as e:
            self.assertEqual("No semicolon found", str(e))
        try:
            get_key_value_and_version('key: "value')
            self.fail()
        except BadLocalizationException as e:
            self.assertEqual("Missing double quote", str(e))
        try:
            get_key_value_and_version("#")
            self.fail()
        except BadLocalizationException as e:
            self.assertEqual("Comment line", str(e))
        try:
            get_key_value_and_version("#Comment:a")
            self.fail()
        except BadLocalizationException as e:
            self.assertEqual("Comment line", str(e))

    def test_file_to_keys_and_values(self):
        absolute_file_path = os.path.abspath(os.path.join(get_data_dir(), "test.yml"))
        keys_and_values, first_line = file_to_keys_and_values(absolute_file_path)
        self.assertEqual(2, len(keys_and_values))
        self.assertEqual("value", keys_and_values["key"]["value"])
        self.assertEqual(0, keys_and_values["key"]["version"])
        self.assertEqual("value2", keys_and_values["key2"]["value"])
        self.assertEqual(0, keys_and_values["key2"]["version"])
        self.assertEqual("l_french:\n", first_line[1:])


if __name__ == "__main__":
    unittest.main()
