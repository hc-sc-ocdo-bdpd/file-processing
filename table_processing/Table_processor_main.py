from Table_Detector import Table_Detector
import logging
logging.basicConfig(filename='table_detection.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')
logging.getLogger().addHandler(logging.StreamHandler())


def process_pdf(input_file_path, output_file_path = "output.xlsx"):
    logging.info("Processing path provided: " + input_file_path)
    input_file_path = input_file_path.replace('\"', '').replace('\\', '\\\\')
    output_file_path = output_file_path.replace('\"', '').replace('\\', '\\\\')
    logging.info("Processing file: " + input_file_path)

    try:
        detector = Table_Detector(file = input_file_path)
        logging.info("Saving output to: " + output_file_path)
        detector.to_excel(filename = output_file_path)
    except Exception as e:
        logging.error('An error occured: ' + e)
    
    return output_file_path


def console_main():
    logging.info("Table Processor started")
    input_file_path = input('Enter the path to the inout PDF file: ')
    output_file_path = input('Enter the path to the output xlsx file: ')
    output_file_path = process_pdf(input_file_path, output_file_path)
    logging.info("Table Processor finished. Results are in: " + output_file_path)


if __name__ == '__main__':
    console_main()
