from pathlib import Path
import re
import pytest
from pytest_mock import MockerFixture
import requests
import responses

from src.update_paratranz import create_or_update_file, create_or_update_files, get_project_files
from tests.utils import generate_random_str


@pytest.fixture(scope="module")
def project_id():
    yield 42


@pytest.fixture(scope="module")
def token():
    yield generate_random_str()


@pytest.fixture(scope="module")
def language():
    yield generate_random_str()


@pytest.fixture(scope="function")
def empty_file(language: str, tmp_path: Path):
    file_name = f"file_{language}.yml"
    file = tmp_path / language / file_name
    file.parent.mkdir(parents=True)
    file.touch()
    yield file


@pytest.fixture(scope="function")
def empty_file_with_subdir(language: str, tmp_path: Path):
    file_name = f"file_{language}.yml"
    file = tmp_path / language / "subdir" / file_name
    file.parent.mkdir(parents=True)
    file.touch()
    yield file


@responses.activate
def test_get_project_files(project_id: int):
    responses.get(
        f"https://paratranz.cn/api/projects/{project_id}/files",
        json=[{"id": "id1", "name": "name1"}, {"id": "id2", "name": "name2"}],
    )
    assert {"name1": "id1", "name2": "id2"} == get_project_files(project_id)


@responses.activate
def test_create_file(project_id: int, token: str, language: str, empty_file: Path, tmp_path: Path):
    current_files = dict()
    files_with_errors = []
    mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files")
    create_or_update_file(token, project_id, tmp_path, language, str(empty_file), current_files, files_with_errors)
    assert mock.call_count == 1
    assert empty_file.name in mock.calls[0].request.body.decode()
    assert files_with_errors == []


@responses.activate
def test_update_file(project_id: int, token: str, language: str, empty_file: Path, tmp_path: Path):
    file_id = 24
    current_files = {empty_file.name: file_id}
    files_with_errors = []
    mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files/{file_id}")
    create_or_update_file(token, project_id, tmp_path, language, str(empty_file), current_files, files_with_errors)
    assert mock.call_count == 1
    assert empty_file.name in mock.calls[0].request.body.decode()
    assert files_with_errors == []


@responses.activate
def test_create_file_error(project_id: int, token: str, language: str, empty_file: Path, tmp_path: Path):
    current_files = dict()
    files_with_errors = []
    mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files", status=500)
    create_or_update_file(token, project_id, tmp_path, language, str(empty_file), current_files, files_with_errors, 0)
    assert mock.call_count == 2  # Retry is done
    assert empty_file.name in mock.calls[0].request.body.decode()
    assert files_with_errors == [empty_file.name]


@responses.activate
def test_update_file_error(project_id: int, token: str, language: str, empty_file: Path, tmp_path: Path):
    file_id = 24
    current_files = {empty_file.name: file_id}
    files_with_errors = []
    mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files/{file_id}", status=500)
    create_or_update_file(token, project_id, tmp_path, language, str(empty_file), current_files, files_with_errors, 0)
    assert mock.call_count == 2  # Retry is done
    assert empty_file.name in mock.calls[0].request.body.decode()
    assert files_with_errors == [empty_file.name]


@responses.activate
def test_create_file_with_subdir(
    project_id: int, token: str, language: str, empty_file_with_subdir: Path, tmp_path: Path
):
    current_files = dict()
    files_with_errors = []
    mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files")
    create_or_update_file(
        token, project_id, tmp_path, language, str(empty_file_with_subdir), current_files, files_with_errors
    )
    assert mock.call_count == 1
    assert empty_file_with_subdir.parent.name in mock.calls[0].request.body.decode()
    assert files_with_errors == []


@responses.activate
def test_update_file_with_subdir(
    project_id: int, token: str, language: str, empty_file_with_subdir: Path, tmp_path: Path
):
    file_id = 24
    current_files = {f"{empty_file_with_subdir.parent.name}/{empty_file_with_subdir.name}": file_id}
    files_with_errors = []
    mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files/{file_id}")
    create_or_update_file(
        token, project_id, tmp_path, language, str(empty_file_with_subdir), current_files, files_with_errors
    )
    assert mock.call_count == 1
    assert empty_file_with_subdir.parent.name in mock.calls[0].request.body.decode()
    assert files_with_errors == []


first_call = True


def test_retry(project_id: int, token: str, language: str, empty_file: Path, tmp_path: Path, mocker: MockerFixture):

    def raise_error_first_call(url: str, headers: dict, filepath: str, paratranz_path: str):
        global first_call
        if first_call:
            first_call = False
            raise requests.HTTPError()

    mocker.patch("src.update_paratranz.__post_file_to_paratranz", new=raise_error_first_call)
    current_files = dict()
    files_with_errors = []
    create_or_update_file(token, project_id, tmp_path, language, str(empty_file), current_files, files_with_errors)
    assert files_with_errors == []


@responses.activate
def test_create_or_update_files(project_id: int, token: str, language: str, tmp_path: Path):
    file_name1 = f"file1_{language}.yml"
    file1 = tmp_path / language / file_name1
    file_name2 = f"file2_{language}.yml"
    file2 = tmp_path / language / file_name2
    file_name3 = f"file3_{language}.yml"
    subdir = "subdir"
    file3 = tmp_path / language / subdir / file_name3
    file_name4 = f"file4_{language}.yml"
    file4 = tmp_path / language / subdir / file_name4
    file_name5 = "file5.yml"
    file5 = tmp_path / "other_language" / file_name5
    file_name6 = "file5.yml"
    file6 = tmp_path / language / file_name6
    for file in [file1, file2, file3, file4, file5, file6]:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()
    file_id = 24
    responses.get(
        f"https://paratranz.cn/api/projects/{project_id}/files",
        json=[{"id": file_id, "name": f"{subdir}/{file_name4}"}],
    )
    create_mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files")
    update_mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files/{file_id}")
    create_or_update_files(project_id, token, tmp_path, language, 1)
    assert create_mock.call_count == 3
    expected_calls = [file_name1, file_name2, file_name3]
    for i in range(create_mock.call_count):
        assert expected_calls[i] in create_mock.calls[i].request.body.decode()
    assert subdir in create_mock.calls[-1].request.body.decode()
    assert update_mock.call_count == 1
    assert file_name4 in update_mock.calls[0].request.body.decode()
    assert subdir in update_mock.calls[0].request.body.decode()


@responses.activate
def test_create_or_update_files_get_paratranz_files_error(
    project_id: int, token: str, language: str, empty_file: Path, tmp_path: Path, capsys
):
    responses.get(f"https://paratranz.cn/api/projects/{project_id}/files", status=500)
    create_mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files")
    create_or_update_files(project_id, token, tmp_path, language, 1)
    assert create_mock.call_count == 1
    assert empty_file.name in create_mock.calls[0].request.body.decode()
    captured = capsys.readouterr()
    logs = captured.out.split("\n")
    assert "WARNING: Fail to get the list of files from Paratranz" in logs
    assert "Files can be created but not updated" in logs


@responses.activate
def test_create_or_update_files_create_error(
    project_id: int, token: str, language: str, empty_file: Path, tmp_path: Path, capsys
):
    responses.get(f"https://paratranz.cn/api/projects/{project_id}/files", json=[])
    mock = responses.post(f"https://paratranz.cn/api/projects/{project_id}/files", status=500)
    create_or_update_files(project_id, token, tmp_path, language, 1)
    assert mock.call_count == 2  # Retry
    for i in range(mock.call_count):
        assert empty_file.name in mock.calls[i].request.body.decode()
    captured = capsys.readouterr()
    logs = captured.out.split("\n")
    assert "ERROR: Non updated files:" in logs
    for i in range(len(logs)):
        if logs[i] == "ERROR: Non updated files:":
            break
    assert empty_file.name in logs[i:]


def test_create_or_update_files_non_existing_dir(project_id: int, token: str, language: str):
    responses.get(f"https://paratranz.cn/api/projects/{project_id}/files", json=[])
    responses.post(f"https://paratranz.cn/api/projects/{project_id}/files")
    loc_dir = generate_random_str()
    with pytest.raises(ValueError, match=f"Directory {loc_dir} does not exist"):
        create_or_update_files(project_id, token, loc_dir, language, 1)


def test_create_or_update_files_non_existing_language_dir(project_id: int, token: str, language: str, tmp_path: Path):
    responses.get(f"https://paratranz.cn/api/projects/{project_id}/files", json=[])
    responses.post(f"https://paratranz.cn/api/projects/{project_id}/files")
    with pytest.raises(ValueError, match=re.escape(f"Directory {tmp_path/language} does not exist")):
        create_or_update_files(project_id, token, tmp_path, language, 1)
