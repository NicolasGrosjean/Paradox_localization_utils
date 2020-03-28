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

## Usage

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


### Apply diff for EUIV and sooner
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
