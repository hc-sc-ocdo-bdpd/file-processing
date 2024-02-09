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

As system metadata extraction can entail OS-specific processes, Windows users can optionally install `pywin32` to extract file owner information (`pip install pywin32`).  

Optional developer dependencies are defined in the `pyproject.toml` config file. These cannot be installed directly from GitHub and will require manual `pip install <library>` for now, until the project can be published on `pypi`.

Once on `pypi`, the command to install the optional dependencies is:

```py
pip install file_procesing_tools[developer]
```

This installs both the library and each of the specified sets of dependencies. The `[developer]` dependencies are listed below and are oriented around build, documentation, and testing capabilities. 

```
wheel==0.40.0
pytest==7.4.0
pytest-order==1.2.0
sphinx==7.2.6
furo==2024.1.29
myst-parser==2.0.0
sphinx-inline-tabs==2023.4.21
pywin32
ipywidgets==8.1.1
build==1.0.3
```
