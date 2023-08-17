from Table_Detector import Table_Detector
import logging
from pathlib import Path

'''
Main program for the console version of the table extraction tool.
'''


logging.basicConfig(filename='table_detection.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')
logging.getLogger().addHandler(logging.StreamHandler())
default_output = "output.xlsx"


# Validate the input filename, regect names that are not pdf files. 
def validate_input_filename(filename):
    filename = Path(filename)
    if filename.suffix != ".pdf":
        logging.error("Input_file_path suffix is not pdf. It was: " + filename.suffix)
        raise Exception("Invalid input file type, input must be a pdf file.")
    return filename


# Validates the output filename. If it is no good, it reports the path of a new filename that will be used
def validate_output_filename(filename):
    filename = Path(filename)
    if filename.suffix != ".xlsx":
        logging.error("Output_file_path suffix is not xlsx. It was: " + str(filename.suffix))
        filename = Path(default_output)
        logging.error("Output file changed to: " + str(filename))
    return filename


# Process the content of the input file.
# Returns the path to the output file
# This is the main method to call if you have file content instead of a file path
# (Notably used by the GUI)
def process_content(content, output_file_path = default_output):
    logging.info("Processing file content.")
    output_file_path = validate_output_filename(output_file_path)
    
    try:
        detector = Table_Detector(filedata = content)
        logging.info("Saving output to: " + str(output_file_path))
        detector.to_excel(str(output_file_path))
    except Exception as e:
        logging.error('process_content - An error occured: ' + str(e))
    
    logging.info("Processing complete")
    return str(output_file_path)


# Process the input file from path
# Returns the path to the output file
# This is the main method to call if you have a path to an input file
# (Notably used by the console application)
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
    
    logging.info("Processing complete")
    return str(output_file_path)


# Main console application
def console_main():
    logging.info("Table Processor started")
    input_file_path = input('Enter the path to the input PDF file: ')
    output_file_path = input('Enter the path to the output xlsx file: ')
    output_file_path = process_pdf(input_file_path, output_file_path)
    logging.info("Table Processor finished. Results are in: " + output_file_path)


if __name__ == '__main__':
    console_main()
