
import PyInstaller.__main__
import logging
logging.basicConfig(filename='build_log.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')
logging.getLogger().addHandler(logging.StreamHandler())

def build_application(console_app_py):
    logging.info("Building application: " + str(console_app_py) + ".")
    logging.info("Cleaning up previous build files for the console application.")
    PyInstaller.__main__.run(['--clean', console_app_py])
    logging.info("Building console application: " + str(console_app_py) + ".")
    PyInstaller.__main__.run([
        console_app_py,
        '--onefile',
        '--windowed',
        '--hidden-import=pytorch',
        '--hidden-import=timm',
        '--collect-data timm',
        '--collect-data torch',
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
        '--hidden-import=transformers'
        '--collect-all timm',
        '--paths ./.venv/Lib/site-packages'
    ])
    logging.info("Console application build complete: " + str(console_app_py))



if __name__ == '__main__':
    build_application('./table_processing/Table_Processor_Main.py')
    build_application('./table_processing/GUI.py')
    