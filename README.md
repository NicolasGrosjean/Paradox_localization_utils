# Paradox localization utils

## Installation

I recommend you to install a Python environment with conda, virtualenv or pipenv.

##### Conda
For example with conda, 
[download and install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Create a conda environment
```
conda create -n paradox_loc python=3.7.1
```

Activate the conda environment
```
activate paradox_loc
```

Install Levenshtein package (only needed for *apply_diff_all*)
```
conda install python-levenshtein==0.12.0
```
OR
```
pip install python-levenshtein==0.12.0
```

Install pandas package (only needed for *extract_existing_translation*)
```
pip install pandas
```

## Usage

### Update source

```
python src/update_source.py <source_dir> <target_dir> <source_lang>
```

Example to update the English files of the HoI4 mod Kaiserreich
```
python src/update_source.py <...>\Steam\steamapps\workshop\content\394360\1521695605 <...>\GitHub\Traduction-FR-Kaiserreich\Traduction-FR-Kaiserreich english
```

### Add missing lines

#### For Imperator Rome and sooner
```
python src/add_missing_lines.py <source_dir> <dest_dir>
```

Example to add in French files missing lines from English files
```
python src/add_missing_lines.py "<...>\game\localization\english" "<...>\game\localization\french"
```

#### For EUIV, HoI4 or Stellaris
```
python src/add_missing_lines.py <localisation_dir> <localisation_dir> -source_lang <source_lang> -dest_lang <dest_lang>
```

Example to add in French files missing lines from English files
```
python src/add_missing_lines.py "<...>\localisation" "<...>\localisation" -source_lang english -dest_lang french
```


### Apply diff all

#### For Imperator Rome and sooner
Not yet implemented

#### For EUIV, HoI4 or Stellaris
```
python src/apply_diff_all.py <old_localisation_dir> <current_localisation_dir> <current_localisation_dir> -source_lang <source_lang> -dest_lang <dest_lang>
```

Example to add in French files missing lines from English files
```
python src/apply_diff_all.py "<...>\V1\localisation" "<...>\V2\localisation" "<...>\V2\localisation" -source_lang english -dest_lang french
```

The destination file is override so don't hesitate to have a backup before running this.

The new and edited lines contains `:9 "`.

If there is less than 10 modifications (according Levenshtein distance),
the destination text is kept.

### Extract existing translation

#### Limits
The target is EUIV or sooner whereas the souce can be CK2/Vic2 or EUIV and sooner.

#### Usage
```
python src/extract_existing_translation.py <extract_source_dir> <extract_dest_dir> <target_source_dir> <target_dest_dir> <source_lang> <dest_lang> -source_col_ck2 <source_col_ck2> -dest_col_ck2 <dest_col_ck2>
```

Example to add in French CK3 files some texts from CK2 files.
```
python src/extract_existing_translation.py "<...>\CK2\localisation" "<...>\CK2\localisation" "<...>\CK3\localization\english" "<...>\CK3\localization\french" english french -source_col_ck2 1 -dest_col_ck2 2
```

Example to add in French HoI IV mod files some texts from Vanilla files.
```
python src/extract_existing_translation.py "<...>\Steam\steamapps\common\Hearts of Iron IV\localisation" "<...>\Steam\steamapps\common\Hearts of Iron IV\localisation" "<...>\mod\localisation" "<...>\mod\localisation" english french
```

### Copy localization in other languages

#### Limits
It works only for Imperator Rome and sooner.

#### Usage
 ```
python src/copy_on_other_languages.py <localization_dir> <source_lang> <dest_lang1> <dest_lang2> ... 
```

Example to add some languages to available only in English and French (the added languages will have English text). 
```
python src/copy_on_other_languages.py "<...>\MyMod\localisation" english korean german russian simp_chinese spanish
```
 
### [DEPRECATED] Apply diff for EUIV and sooner
```
python src/apply_diff.py <old_source_file> <new_source_file> <dest_file>
```

The destination file is override so don't hesitate to have a backup before running this.
The new and edited lines contains `:9 "`

Optionnal parameters :
* ```-space_prefix <value>``` : Prefix (generally spaces) before key in files
* ```-keep_edited``` : Keep destination value in case of edition.
The default behavior replace the destination value by the new source value.

Example to apply the English update from 0.11.1 to 0.11.2 to Russia file in French:
```
<...>\0.11.1\localisation\KR_Russia_l_english.yml <...>\0.11.2\localisation\KR_Russia_l_english.yml <...>\Translation_FR\localisation\KR_Russia_l_french.yml -space_prefix "  " -keep_edited
```
After running this, the new and edited lines need to be fixed by hand by seeking `:9 "`

## Tests

Go to the tests directory and run unittest
```
cd tests
python -m unittest discover
```

## License

The project has an [MIT license](Licence.md).
