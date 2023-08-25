
import PyInstaller.__main__

def build_application(console_app_py):
    PyInstaller.__main__.run([
        console_app_py,
        '--onefile',
        '--hidden-import=pytorch',
        '--hidden-import=timm',
        '--collect-data=timm',
        '--collect-data=torch',
        '--copy-metadata=torch',
        '--copy-metadata=tqdm',
        '--copy-metadata=regex',
        '--copy-metadata=requests',
        '--copy-metadata=packaging',
        '--copy-metadata=filelock',
        '--copy-metadata=numpy',
        '--copy-metadata=tokenizers',
        '--copy-metadata=huggingface_hub',
        '--copy-metadata=safetensors',
        '--copy-metadata=pyyaml',
        '--copy-metadata=transformers',
        '--hidden-import=transformers',
        '--collect-all=timm',
        '--collect-all=dash'
        '--paths=./.venv/Lib/site-packages'
    ])



if __name__ == '__main__':
    # build_application('./table_processing/Table_Processor_Main.py')
    build_application('./table_processing/GUI2.py')

    