<br>

# Installation

<br>

## Quickstart

The library can be installed directly from GitHub. This should take approximately 2-4 minutes.

```js
pip install git+https://github.com/hc-sc-ocdo-bdpd/file-processing-tools.git
```

An alternative option is downloading the `dist/*.whl` file from GitHub and installing this via `pip install <path/to/whl/file>`.

It is not yet possible to directly install the library through `pypi` as the project is in pre-release.

<br>

## Additional Dependencies

This project uses Tesseract for OCR and ffmpeg for transcription. Note that these are not hard requirements as OCR and transcription are configurable by the `use_ocr` and `use_transcription` parameters.

**Tesseract**: This must be installed at: `C:/Users/USERNAME/AppData/Local/Programs/Tesseract-OCR/tesseract.exe` (Windows) or `/usr/bin/tesseract` (Linux). See [here for more details](https://github.com/UB-Mannheim/tesseract/wiki). 

**ffmpeg**: This can be installed through PowerShell:
1. Install scoop: `iwr -useb get.scoop.sh | iex`
2. Install ffmpeg: `scoop install ffmpeg`
3. It may be necessary to restart the IDE and computer after these installs have been completed

<br>

## Optional Dependencies

Optional dependencies are defined in the `pyproject.toml` config file. These include sets of dependencies for `windows`, `testing`, `build`, and `documentation`. These cannot be installed directly from GitHub and will require manual `pip install <library>` for now, until the project can be published on `pypi`.

Once on `pypi`, the command to install optional dependencies is:

```py
pip install file_procesing_tools[<optional_set_1>, ...]
```

This installs both the library and each of the specified sets of dependencies. Namely, the 4 optional dependency sets are:

```toml
windows = ['pywin32']
build = ['wheel==0.40.0']
documentation = [
    'sphinx==7.2.6',
    'furo==2024.1.29',
    'myst-parser==2.0.0',
    'sphinx-inline-tabs==2023.4.21',
]
testing = [
    'pytest==7.4.0',
    'pytest-order==1.2.0',
    'openpyxl>=3.1.2',
    'python-Levenshtein==0.21.1',
    'scikit-learn==1.3.0',
]
```
