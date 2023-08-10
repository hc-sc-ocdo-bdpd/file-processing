from Table_Detector import Table_Detector
import logging
from pathlib import Path

logging.basicConfig(filename='table_detection.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')
logging.getLogger().addHandler(logging.StreamHandler())
default_output = "output.xlsx"

def validate_input_filename(filename):
    filename = Path(filename)
    if filename.suffix != ".pdf":
        logging.error("Input_file_path suffix is not pdf. It was: " + filename.suffix)
        raise Exception("Invalid input file type, input must be a pdf file.")
    return filename


def validate_output_filename(filename):
    filename = Path(filename)
    if filename.suffix != ".xlsx":
        logging.error("Output_file_path suffix is not xlsx. It was: " + str(filename.suffix))
        filename = Path(default_output)
        logging.error("Output file changed to: " + str(filename))
    return filename


def process_content(content, output_file_path = default_output):
    logging.error("Not yet implemented")
    
    detector = Table_Detector(filedata = content)
    detector.to_excel(str(output_file_path))
    return str(output_file_path)


def process_pdf(input_file_path, output_file_path = default_output):
    logging.info("Processing path provided: " + str(input_file_path))
    input_file_path = validate_input_filename(input_file_path)
    output_file_path = validate_output_filename(output_file_path)
    logging.info("Processing file: " + str(input_file_path))

    try:
        detector = Table_Detector(filename = str(input_file_path))
        logging.info("Saving output to: " + str(output_file_path))
        detector.to_excel(filename = str(output_file_path))
    except Exception as e:
        logging.error('An error occured: ' + str(e))
    
    return str(output_file_path)


def console_main():
    logging.info("Table Processor started")
    input_file_path = input('Enter the path to the input PDF file: ')
    output_file_path = input('Enter the path to the output xlsx file: ')
    output_file_path = process_pdf(input_file_path, output_file_path)
    logging.info("Table Processor finished. Results are in: " + output_file_path)


if __name__ == '__main__':
    console_main()
