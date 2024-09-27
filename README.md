[![Build Status](https://github.com/NicolasGrosjean/Paradox_localization_utils/actions/workflows/flake8_test_coverage.yml/badge.svg)](https://github.com/NicolasGrosjean/Paradox_localization_utils/actions/workflows/flake8_test_coverage.yml)
[![Tests](badges/tests.svg)](https://github.com/NicolasGrosjean/Paradox_localization_utils/actions/workflows/flake8_test_coverage.yml)
[![Coverage](badges/coverage.svg)](https://github.com/NicolasGrosjean/Paradox_localization_utils/actions/workflows/flake8_test_coverage.yml)

# Paradox localization utils

> A set of tools to manipulate Paradox localization files particularly for translating

## Terms

- Source: It refers to the source language of your translation
- Destination (shorten dest): It refers to the destination language of your translation

Example : If I translate from English to French, the source directory refers to the directory of English localisation files.

## Installation

I recommend you to install a Python environment with poetry, conda, virtualenv or pipenv.

### Poetry

poetry install
```shell
```

#### Pre-commit (only need for contributing to the project)

<!-- [On Windows] Copy the file `coverage.bat` in the folder `.git/hooks/` and name it `pre-commit` (it is normal there is no `.bat`). -->

Install pre-commit

```shell
pre-commit install
```

### Conda

If you prefer conda to poetry, [download and install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Create a conda environment

```shell
conda create -n paradox_loc python=3.10
```

Activate the conda environment

```shell
activate paradox_loc
```

Install Levenshtein package (only needed for _apply_diff_all_)

```shell
conda install python-levenshtein
```

OR

```shell
pip install python-levenshtein
```

Install pandas package (only needed for _extract_existing_translation_)

```shell
pip install pandas
```

#### Pre-commit (only need for contributing to the project)

<!-- [On Windows] Copy the file `coverage.bat` in the folder `.git/hooks/` and name it `pre-commit` (it is normal there is no `.bat`). -->

Install pre-commit

```shell
pip install pre-commit
pre-commit install
```

## Usage

### Update source

> Update the localization files of your source languages.
> It also copy in the parent of the target directory an extract of the source localization and all files in target_dir.

```shell
python paradox_localization_utils/update_source.py <source_dir> <target_dir> <source_lang>
```

Example to update the English files of the HoI4 mod Kaiserreich

```shell
python paradox_localization_utils/update_source.py <...>\Steam\steamapps\workshop\content\394360\1521695605 <...>\GitHub\Traduction-FR-Kaiserreich\Traduction-FR-Kaiserreich english
```

### Update Paratranz

> Update files to translate on Paratranz

Get your Paratranz API token in the settings tab of your Paratranz profile.

Get the Paratranz project id by open the project and see the number in the url.

```shell
python paradox_localization_utils/update_paratranz.py <token> <project_id> <loc_dir> <language>
```

Example to update the RICE project (translation from English) on Paratranz

```shell
python paradox_localization_utils/update_paratranz.py <token> 2617 <...>\GitHub\RICE-for-CK3\RICE\localization english
```

To compile the code, run the following command

```shell
python compile_update_paratranz.py build
```

then put the dist/ directory in update_paratranz/

### Download from Paratranz

> Download translated files from Paratranz

Get your Paratranz API token in the settings tab of your Paratranz profile.

Get the Paratranz project id by open the project and see the number in the url.

```shell
python paradox_localization_utils/download_paratranz.py <token> <project_id> <raw_dir_path> <utf8_dir_path>
```

### Add missing lines

> Add in the destination files the lines which are missing from the source ones

#### For Imperator Rome and sooner

```shell
python paradox_localization_utils/add_missing_lines.py <source_dir> <dest_dir>
```

Example to add in French files missing lines from English files

```shell
python paradox_localization_utils/add_missing_lines.py "<...>\game\localization\english" "<...>\game\localization\french"
```

#### For EUIV, HoI4 or Stellaris

```shell
python paradox_localization_utils/add_missing_lines.py <localisation_dir> <localisation_dir> -source_lang <source_lang> -dest_lang <dest_lang>
```

Example to add in French files missing lines from English files

```shell
python paradox_localization_utils/add_missing_lines.py "<...>\localisation" "<...>\localisation" -source_lang english -dest_lang french
```

### Apply diff all

> Apply the differences between an old source version and a current source version to your current destination files.

#### For Imperator Rome and sooner, and new EUIV, HoI4 or Stellaris localisation format (a subdirectory for each language)

```shell
python paradox_localization_utils/apply_diff_all.py <old_localisation_dir> <current_localisation_dir>
```

- <old_localisation_dir> contains the localisation of the old source version
- <current_source_localisation_dir> contains the localisation of the new source version
- <current_dest_localisation_dir> contains the localisation of the old destination version

Example to apply in French files the modifications done in English

```shell
python paradox_localization_utils/apply_diff_all.py "<...>\V1\localisation\english" "<...>\V2\localisation\english" -dest_dir "<...>\V1\localisation\french"
```

#### For old EUIV, HoI4 or Stellaris localisation format (all files in the same directory)

```shell
python paradox_localization_utils/apply_diff_all.py <old_localisation_dir> <current_localisation_dir> -source_lang <source_lang> -dest_lang <dest_lang>
```

- <old_localisation_dir> contains the localisation of the old source version
- <current_localisation_dir> contains the localisation of both new source version and old destination version

Example to apply in French files the modifications done in English

```shell
python paradox_localization_utils/apply_diff_all.py "<...>\V1\localisation" "<...>\V2\localisation" -source_lang english -dest_lang french
```

#### Both format

The destination files are overriden so don't hesitate to have a backup before running this.

The new and edited lines contains `:9 "`.

If there is less than 10 modifications (according Levenshtein distance),
the destination text is kept.

All the lines to translate are exported in to*translate/file_to_translate*<source_lang>.yml.

We can also add the following parameter to the command line -keys_to_ignore <path_to_file_with_a_key_a_line>,
to simply copy-paste lines with these keys.
It is useful when you have keys like spellcheck_ignore in the source files.

### Extract existing translation

> Extract existing translation from another game or mod to apply to your translation

#### Limits

The target is EUIV or sooner whereas the source can be CK2/Vic2 or EUIV and sooner.

#### Usage

```shell
python paradox_localization_utils/extract_existing_translation.py <extract_source_dir> <extract_dest_dir> <target_source_dir> <target_dest_dir> <source_lang> <dest_lang> -source_col_ck2 <source_col_ck2> -dest_col_ck2 <dest_col_ck2>
```

Example to add in French CK3 files some texts from CK2 files.

```shell
python paradox_localization_utils/extract_existing_translation.py "<...>\CK2\localisation" "<...>\CK2\localisation" "<...>\CK3\localization\english" "<...>\CK3\localization\french" english french -source_col_ck2 1 -dest_col_ck2 2
```

Example to add in French HoI IV mod files some texts from Vanilla files.

```shell
python paradox_localization_utils/extract_existing_translation.py "<...>\Steam\steamapps\common\Hearts of Iron IV\localisation" "<...>\Steam\steamapps\common\Hearts of Iron IV\localisation" "<...>\mod\localisation" "<...>\mod\localisation" english french
```

### Extract Paratranz translation

> Extract translations from JSON files downloaded from [Paratranz](https://paratranz.cn) to apply to your translation.

#### Limits

This script only works for EUIV and sooner.

#### Usage

```shell
python paradox_localization_utils/extract_paratranz_translation.py <paratranz_dir> <localisation_dir> <language>
```

Example to extract french reviewed translations

```shell
python paradox_localization_utils/extract_paratranz_translation.py "<...>\paratranz" "<...>\localisation" french
```

By default it extracts only reviewed translation.
If you want to extract not reviewed translation, add `-extract_not_review` to the command.

Example to extract french translations (reviewed or not)

```shell
python paradox_localization_utils/extract_paratranz_translation.py "<...>\paratranz" "<...>\localisation" french -extract_not_review
```

### Copy localization in other languages

> Copy the localization of a language in other languages to allow to run your game/mod with this language with source texts instead of keys.

#### Limits

It works only for Imperator Rome and sooner.

#### Basic Usage [Windows only]

The usage is explicated in this [Steam guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2342385980).

#### Developer Usage

```shell
python paradox_localization_utils/copy_on_other_languages.py <localization_dir> <source_lang> <dest_lang1> <dest_lang2> ...
```

Example to add some languages to available only in English and French (the added languages will have English text).

```shell
python paradox_localization_utils/copy_on_other_languages.py "<...>\MyMod\localisation" english korean german russian simp_chinese spanish
```

To compile it (after running once `pip install cx_Freeze`), use the following command

```shell
cxfreeze -c paradox_localization_utils/copy_on_other_languages.py
```

### Get duplicates keys

> Get the list of duplicated keys in the localization to avoid localization erased by others.

#### Limits

The duplicated keys are searched in English localisation files only.

#### Usage

To get the full list of duplicated keys run the following command

```shell
python paradox_localization_utils/get_duplicates_key.py "<...>\MyMod\localisation"
```

To get only the list of duplicated keys which already cause a bug
(the value is not the same for each duplication), add _-only_different_value_ to the command.

### [DEPRECATED] Apply diff for EUIV and sooner

```shell
python paradox_localization_utils/apply_diff.py <old_source_file> <new_source_file> <dest_file>
```

The destination file is override so don't hesitate to have a backup before running this.
The new and edited lines contains `:9 "`

Optionnal parameters :

- `-space_prefix <value>` : Prefix (generally spaces) before key in files
- `-keep_edited` : Keep destination value in case of edition.
  The default behavior replace the destination value by the new source value.

Example to apply the English update from 0.11.1 to 0.11.2 to Russia file in French:

```shell
python paradox_localization_utils/apply_diff.py <...>\0.11.1\localisation\KR_Russia_l_english.yml <...>\0.11.2\localisation\KR_Russia_l_english.yml <...>\Translation_FR\localisation\KR_Russia_l_french.yml -space_prefix "  " -keep_edited
```

After running this, the new and edited lines need to be fixed by hand by seeking `:9 "`

## Tests

Run the tests with pytest

```shell
pytest
```

If some tests fails with error `ModuleNotFoundError: No module named 'paradox_localization_utils'`, run the following command in the root directory.

On Windows:

```shell
set PYTHONPATH=%CD%
```

On Linux

```shell
export PYTHONPATH=${PYTHONPATH}:${PWD}
```

## Run actions

Th upload badge to GitHub action should have access to your GitHub repository. Strongly recommend store it in secrets. [Create a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with the `repo` permission. [Create a secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named `ACCESS_TOKEN` in your repository and copy access token to the secret value.

## License

The project has an [MIT license](Licence.md).
