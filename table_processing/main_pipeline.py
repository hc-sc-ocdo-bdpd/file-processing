from Table_Detector import Table_Detector
import os
import logging

logging.basicConfig(filename='table_detection_log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')
filepath = './resources/'
filename = ''
def main():
    fileInput = input('Enter name of file:  ')
    global filename
    global filepath
    filepath = filepath + fileInput
    filename = fileInput
    read_pdf(filepath)

    
def read_pdf(filepath):
    output_path = './output/'
    output_path = output_path + filename
    if not os.path.exists(output_path):
        os.makedirs('./output/' + filename)

    try:
        detc_table = Table_Detector(filepath+'.pdf')
        detc_table.to_excel(output_path+'/alltables.xlsx')

    except Exception as e:  # could not detect table from pdf
        logging.error('Could not detect table ' + filepath + ' from pdf')
        logging.error(e)

main()
