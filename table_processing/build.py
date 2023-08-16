
import subprocess
from pathlib import Path

def build_exe_from_spec(spec_path):
    try:
        subprocess.run(["pyinstaller", "--noconfirm", spec_path])
    except Exception as e:
        print("Error building executable:", e)

# Specify the path to your .spec file
spec_file_path = Path("./table_processing/table_exe.spec").absolute()

# Call the function to build the executable
build_exe_from_spec(spec_file_path)


'''
import PyInstaller.__main__
import logging
import os
import shutil
from pathlib import Path

logging.basicConfig(filename='build_log.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')
logging.getLogger().addHandler(logging.StreamHandler())


def delete_directory(directory_path):
    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
            logging.info(f"Deleted directory: {directory_path}")
        except Exception as e:
            logging.error(f"Error deleting directory: {e}")
    else:
        logging.info(f"Directory does not exist: {directory_path}")


def build_application(spec_path, spec_file):
    logging.info("Building application: " + str(spec_path) + ".")
    PyInstaller.__main__.run(['--specpath ' + str(spec_path) + ' ' + str(spec_file)])

    '''
''''
    PyInstaller.__main__.run([
        console_app_py,
        '--noconfirm',
        '--onefile',
        #'--windowed',
        #'--hidden-import=pytorch',
        #'--hidden-import=timm',
        #'--collect-data timm',
        #'--collect-data torch',
        '--copy-metadata torch',
        '--copy-metadata tqdm',
        '--copy-metadata regex',
        '--copy-metadata requests',
        '--copy-metadata packaging',
        '--copy-metadata filelock',
        '--copy-metadata numpy',
        '--copy-metadata tokenizers',
        '--copy-metadata huggingface_hub',
        '--copy-metadata safetensors',
        '--copy-metadata pyyaml',
        '--copy-metadata transformers',
        #'--hidden-import=transformers'
        #'--collect-all timm',
        #'--paths ./.venv/Lib/'
    ])
    '''
    #logging.info("Application build complete: " + str(console_app_py))


'''
if __name__ == '__main__':
    logging.info("Build Tool Starting...")
    logging.info("Cleaning up previous build files.")
    delete_directory("build")
    delete_directory("dist")
    spec_path = (str(Path('./resources/build_files').absolute()))
    spec_file = "table_exe.spec"
    build_application(spec_path, spec_file)
    #build_application('./table_processing/GUI.py')
    #build_application('./table_processing/demo.py')
    logging.info("... Build Tool Finished.")
    '''