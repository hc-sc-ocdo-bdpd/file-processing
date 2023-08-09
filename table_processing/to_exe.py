# Import table classes, functions, and packages

import subprocess
import sys
    
from Table_Detector import Table_Detector
from table_metrics import test_tables
import pandas as pd
import numpy as np
# xlsxwriter not imported, but needs to be downloaded in environment
import logging
logging.basicConfig(filename='table_detection.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')


file_path = input('Please enter the path to the PDF to extract tables from: ')
file_path = file_path.replace('\"', '').replace('\\', '\\\\').split('.')[0]

try:
    detector = Table_Detector(file = file_path+'.pdf')
    detector.to_excel(filename = file_path+'.xlsx')

except Exception as e:  # could not detect table from pdf
    logging.error('Could not detect table ' + file_path + ' from pdf')
    logging.error(e)

# terminal command to run
# pyinstaller --onefile --hidden-import=pytorch --hidden-import=timm --collect-data timm --collect-data torch --copy-metadata torch --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata huggingface_hub --copy-metadata safetensors --copy-metadata pyyaml --copy-metadata transformers --hidden-import=transformers --collect-all timm --paths ./.venv/Lib/site-packages ./table_processing/to_exe.py   