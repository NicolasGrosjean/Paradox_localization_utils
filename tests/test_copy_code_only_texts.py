from pathlib import Path
import pytest
from paradox_localization_utils.copy_code_only_texts import copy_code_only_texts, extract_code_only_texts

SOURCE_LANG = "english"
DEST_LANG = "french"


@pytest.fixture
def source_file(tmp_path: Path):
    source_dir = tmp_path / SOURCE_LANG
    source_dir.mkdir()
    source_file = source_dir / f"text_l_{SOURCE_LANG}.yml"
    with open(source_file, "w", encoding="utf8") as f:
        f.write(
            f"""\ufeffl_{SOURCE_LANG}:
KEY0:0 "value0"
top_agenda_name:0 "[?top_agenda:agenda_idea.GetName]"
KEY1:2 "[abc] [def] [ghi]"
top_agenda_name2:0 "[?top_agenda:agenda_idea.GetName]"
KEY2:2 "[abc] [def] [ghi]"
KEY3:2 "[abc] def [ghi]"
"""
        )
    yield source_file


@pytest.fixture
def destination_file(tmp_path: Path):
    dest_dir = tmp_path / DEST_LANG
    dest_dir.mkdir()
    dest_file = dest_dir / f"text_l_{DEST_LANG}.yml"
    with open(dest_file, "w", encoding="utf8") as f:
        f.write(
            f"""\ufeffl_{DEST_LANG}:
KEY0:0 "valeur0"
top_agenda_name:0 "[?top_agenda:agenda_idea.GetTokenLocalizedKey]"
KEY1:2 "[abc] [dEf] [ghi]"
top_agenda_name2:0 "[?top_agenda:agenda_idea.GetName]"
KEY2:2 "[abc] [def] [ghi]"
KEY3:2 "[abc] dEf [ghi]"
"""
        )
    yield dest_file


class TestExtractCodeOnlyTexts:
    def test_extract_code_only_texts_when_ok(self, tmp_path: Path, source_file: Path):
        actual = extract_code_only_texts(tmp_path / SOURCE_LANG, SOURCE_LANG)
        assert actual == {
            "top_agenda_name": "[?top_agenda:agenda_idea.GetName]",
            "KEY1": "[abc] [def] [ghi]",
            "top_agenda_name2": "[?top_agenda:agenda_idea.GetName]",
            "KEY2": "[abc] [def] [ghi]",
        }

    def test_extract_code_only_texts_when_empty(self, tmp_path: Path):
        source_dir = tmp_path / SOURCE_LANG
        source_dir.mkdir()
        actual = extract_code_only_texts(source_dir, SOURCE_LANG)
        assert actual == {}


class TestCopyCodeOnlyTexts:
    def test_copy_code_only_texts_when_ok(self, tmp_path: Path, source_file: Path, destination_file: Path):
        copy_code_only_texts(tmp_path / SOURCE_LANG, tmp_path / DEST_LANG, SOURCE_LANG, DEST_LANG)
        with open(destination_file, "r", encoding="utf8") as f:
            actual = f.read()
        assert (
            actual
            == f"""\ufeffl_{DEST_LANG}:
KEY0:0 "valeur0"
 top_agenda_name:0 "[?top_agenda:agenda_idea.GetName]"
 KEY1:2 "[abc] [def] [ghi]"
top_agenda_name2:0 "[?top_agenda:agenda_idea.GetName]"
KEY2:2 "[abc] [def] [ghi]"
KEY3:2 "[abc] dEf [ghi]"
"""
        )
