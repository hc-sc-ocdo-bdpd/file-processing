import logging

from Document import Document

# Init for logging
logging.basicConfig(level = logging.INFO)
#logging.basicConfig(level = logging.DEBUG)

if __name__ == '__main__':
    doc = Document('resources/SampleReport.pdf')
    logging.info('Document text: \n ' + doc.text)
    doc = Document('resources/SampleReportScreenShot.pdf')
    logging.info('Document OCR data: \n ' + doc.ocrText)
