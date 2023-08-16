# table_exe.spec

# Path to the main Python script you want to convert to an executable
# Replace 'your_script.py' with the actual name of your Python script
# You can also use an absolute path here
entry_point = ['GUI.py']

# The name of the generated executable file (without the .exe extension on Windows)
# Replace 'output_executable' with the desired name of your executable
exe_name = 'table_processing_gui'

# Additional data files or directories that should be included with the executable
# Replace 'path/to/your/data' with the actual path to your data files or directories
datas = []#[('path/to/your/data', '.')]

# Additional files or directories to be added to the generated executable's environment
# Replace 'path/to/your/env/files' with the actual path to your environment files or directories
binaries = []#[('path/to/your/env/files', '.')]

# List of hidden imports that PyInstaller might not be able to detect automatically
# Replace 'module_name' with the name of the module you want to include as a hidden import
hiddenimports = []#['module_name']

# Specify any additional PyInstaller options you want to use
# For example, you can set the windowed mode (no console window) using: console=False
# Or you can add icon files using: icon='path/to/icon.ico'
# Check PyInstaller documentation for more available options: https://pyinstaller.readthedocs.io/en/stable/spec-files.html
a = Analysis(
    entry_point,
    pathex=['../table_processing/'],  # Replace with the path to your script's directory
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    #cipher=block_cipher,
    noarchive=False
)

# The BEXE builder is used to create the executable
# You can customize builder options here if needed
# For example, you can specify the compression level using: 'compressed=True'
# Check PyInstaller documentation for more available builder options: https://pyinstaller.readthedocs.io/en/stable/spec-files.html
pyz = PYZ(a.pure, a.zipped_data, compress=False, 
         # Add your custom builder options here
         )

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    upx_silent=False,
    runtime_tmpdir=None,
    console=True  # Set this to False if you don't want a console window to appear
)

# Collate the generated files into a 'dist' folder
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, a.binaries, name=exe_name)

# End of .spec file
