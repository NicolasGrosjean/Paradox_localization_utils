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
```
python src/add_missing_lines.py <source_dir> <dest_dir>
```

Example to add in French files missing lines from English files
```
python src/add_missing_lines.py "<...>\game\localization\english" "<...>\game\localization\french"
```

## Tests

Go to the tests directory and run unittest
```
cd tests
python -m unittest discover
```

## License

The project has an [MIT license](Licence.md).
