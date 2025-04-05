from pathlib import Path

import pytest
from paradox_localization_utils.keep_edited_lines_only import write_kept_lines


class TestWriteKeptLines:
    # TODO Test empty file

    @pytest.mark.parametrize(
        "input_original_values_by_key, input_text_content",
        [
            ({"l_english": ""}, "l_english:"),
            ({"\ufeffl_english": ""}, "l_english:"),
            ({"l_english": ""}, "\ufeffl_english:"),
            ({"\ufeffl_english": ""}, "\ufeffl_english:"),
        ],
        ids=[
            "Original no BOM, new text no BOM",
            "Original with BOM, new text no BOM",
            "Original no BOM, new text with BOM",
            "Original with BOM, new text with BOM",
        ],
    )
    def test_almost_empty_original(
        self, tmp_path: Path, input_original_values_by_key: dict[str, str], input_text_content: str
    ):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text(input_text_content, encoding="utf-8")

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_values_by_key)

        assert output_file_path.read_text(encoding="utf-8") == input_text_content

    def test_new_line(self, tmp_path: Path):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text('l_english:\nkey: "value"', encoding="utf-8")
        input_original_values_by_key = {"l_english": ""}

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_values_by_key)

        assert output_file_path.read_text(encoding="utf-8") == 'l_english:\nkey: "value"'

    def test_edited_line(self, tmp_path: Path):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text('l_english:\nkey: "value2"', encoding="utf-8")
        input_original_values_by_key = {"l_english": "l_english:", "key": "value1"}

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_values_by_key)

        assert output_file_path.read_text(encoding="utf-8") == 'l_english:\nkey: "value2"'

    def test_unedited_line(self, tmp_path: Path):
        input_source_file_path = tmp_path / "toto_l_english.yml"
        input_source_file_path.write_text('l_english:\nkey: "value"', encoding="utf-8")
        input_original_values_by_key = {"l_english": "l_english:", "key": "value"}

        output_file_path = tmp_path / "replace toto_l_english.yml"
        write_kept_lines(input_source_file_path, output_file_path, input_original_values_by_key)

        assert output_file_path.read_text(encoding="utf-8") == "l_english:\n"
