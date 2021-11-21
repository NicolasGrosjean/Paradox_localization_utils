import unittest

import os
from src.read_localization_file import get_key_value_and_version, BadLocalizationException, file_to_keys_and_values
from tests.utils import get_data_dir


class TestReadLocalizationFile(unittest.TestCase):
    def test_get_key_and_value(self):
        key_and_value = get_key_value_and_version('key: "value"')
        self.assertEqual("key", key_and_value[0])
        self.assertEqual("value", key_and_value[1])
        self.assertIsNone(key_and_value[2])
        self.assertEqual("", key_and_value[3])
        key_version_and_value = get_key_value_and_version('key:1 "value"')
        self.assertEqual("key", key_version_and_value[0])
        self.assertEqual("value", key_version_and_value[1])
        self.assertEqual(1, key_version_and_value[2])
        self.assertEqual("", key_version_and_value[3])
        space_key_value = get_key_value_and_version(' key: "value"')
        self.assertEqual("key", space_key_value[0])
        self.assertEqual("value", space_key_value[1])
        self.assertEqual("key", space_key_value[0])
        self.assertEqual("value", space_key_value[1])
        self.assertEqual("", space_key_value[3])
        value_with_color = get_key_value_and_version('key:0 "value #Tcool#!"')
        self.assertEqual("key", value_with_color[0])
        self.assertEqual("value #Tcool#!", value_with_color[1])
        self.assertEqual(0, value_with_color[2])
        self.assertEqual("", value_with_color[3])
        value_with_two_points = get_key_value_and_version('key:0 "value1:value2"')
        self.assertEqual("key", value_with_two_points[0])
        self.assertEqual("value1:value2", value_with_two_points[1])
        self.assertEqual(0, value_with_two_points[2])
        self.assertEqual("", value_with_two_points[3])
        value_comment = get_key_value_and_version('key:0 "value1:value2" #comment')
        self.assertEqual("key", value_comment[0])
        self.assertEqual("value1:value2", value_comment[1])
        self.assertEqual(0, value_comment[2])
        self.assertEqual(" #comment", value_comment[3])
        value_comment_with_two_points = get_key_value_and_version('key:0 "value1:value2" #comment:a')
        self.assertEqual("key", value_comment_with_two_points[0])
        self.assertEqual("value1:value2", value_comment_with_two_points[1])
        self.assertEqual(0, value_comment_with_two_points[2])
        self.assertEqual(" #comment:a", value_comment_with_two_points[3])
        value_with_hashtag = get_key_value_and_version('key:0 "value1:value2 #!"')
        self.assertEqual("key", value_with_hashtag[0])
        self.assertEqual("value1:value2 #!", value_with_hashtag[1])
        self.assertEqual(0, value_with_hashtag[2])
        self.assertEqual("", value_with_hashtag[3])
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
