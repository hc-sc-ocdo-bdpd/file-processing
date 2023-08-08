# Import table classes, functions, and packages

import subprocess
import sys
    
from Table_Detector import Table_Detector
from table_metrics import test_tables
import pandas as pd
import numpy as np
# xlsxwriter not imported, but needs to be downloaded in environment
import logging
logging.basicConfig(filename='benchmarking_log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.WARNING, format='[%(asctime)s][%(levelname)s] %(message)s\n')

# Initialize table dict
tables = {}
failed_tables = []

file_path = input('Please enter the path to the PDF to extract tables from: ')

file_path = file_path.replace('\"', '').replace('\\', '\\\\').split('.')[0]

# Loop for n # of tables
for i in range(0,1):
    try:
        detc_table = Table_Detector(file_path+'.pdf')
        table = detc_table.get_page_data()[0]['tables'][0]['table_content']
        boxes_image = table.plot_bounding_boxes(file_name = file_path+'_boxes')
        detc_table.to_excel(file_path+'.xlsx')
        read_table = pd.read_excel(file_path+'.xlsx')
        # Store true and read tables
    except IndexError:  # could not detect table from pdf
        read_table = pd.DataFrame()
        failed_tables.append(file_path)
        logging.error('Could not detect table ' + file_path + ' from pdf')

# terminal command to run
# currently resulting in import error for timm once user enters path to PDF file
# pyinstaller --onefile --hidden-import=pytorch --hidden-import=timm --collect-data timm --collect-data torch --copy-metadata torch --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata huggingface_hub --copy-metadata safetensors --copy-metadata pyyaml --copy-metadata transformers --hidden-import=transformers --collect-all timm --paths ./.venv/Lib/site-packages ./table_processing/to_exe.py   