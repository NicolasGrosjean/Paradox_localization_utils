from pathlib import Path
from paradox_localization_utils.keep_edited_lines_only import write_kept_lines


class TestWriteKeptLines:
    def test_almost_empty_original(self, tmp_path: Path):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text("l_english:")
        input_original_lines_by_key = {"l_english": "l_english:"}

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_lines_by_key)

        assert output_file_path.read_text() == "l_english:"

    def test_new_line(self, tmp_path: Path):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text("l_english:\nkey: value")
        input_original_lines_by_key = {"l_english": "l_english:"}

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_lines_by_key)

        assert output_file_path.read_text() == "l_english:\nkey: value"

    def test_edited_line(self, tmp_path: Path):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text("l_english:\nkey: value2")
        input_original_lines_by_key = {"l_english": "l_english:", "key": "key: value1"}

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_lines_by_key)

        assert output_file_path.read_text() == "l_english:\nkey: value2"

    def test_unedited_line(self, tmp_path: Path):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text("l_english:\nkey: value")
        input_original_lines_by_key = {"l_english": "l_english:", "key": "key: value"}

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_lines_by_key)

        assert output_file_path.read_text() == "l_english:\n"
