'''
From: https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Table%20Transformer/Using_Table_Transformer_for_table_detection_and_table_structure_recognition.ipynb
Also from: https://huggingface.co/docs/transformers/model_doc/table-transformer
and lastly this: https://github.com/microsoft/table-transformer
'''

from transformers import TableTransformerForObjectDetection
from PIL import Image
import matplotlib.pyplot as plt
import fitz
import pandas as pd
import logging
import os
from pathlib import Path

from Table import Table
from table_tools import get_bounding_boxes

class Table_Detector:

    # Requires EITHER an image of a page or a path to a pdf file.
    def __init__(self, filename = None, filedata = None):
        self.page_data = None
        if filename != None:
            logging.info("Processing from filename: " + str(filename))
            self.page_data = self.get_tables_from_pdf(filename = filename)
        elif filedata != None:
            logging.info("Processing from file content.")
            self.page_data = self.get_tables_from_pdf(content = filedata)
        else:
            message = "Require filename or filedata parameters."
            logging.error(message)
            raise Exception(message)


    def get_page_data(self):
        return self.page_data

    # This will need to be refactored to use the new Table class
    def plot_table_results(self, pil_img, scores, labels, boxes, model, file_name):
        # colors for visualization
        COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
                [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

        plt.figure(figsize=(16,10))
        plt.imshow(pil_img)
        ax = plt.gca()
        colors = COLORS * 100
        for score, label, (xmin, ymin, xmax, ymax),c  in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                    fill=False, color=c, linewidth=3))
            text = f'{model.config.id2label[label]}: {score:0.2f}'
            ax.text(xmin, ymin, text, fontsize=15,
                    bbox=dict(facecolor='yellow', alpha=0.5))
        plt.axis('off')
        plt.savefig(file_name)
        plt.show()


    def find_tables(self, image):
        model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
        return get_bounding_boxes(image, model)
    

    def get_tables_from_pdf(self, filename = None, content = None):
        if filename != None:
            doc = fitz.open(filename)
        elif content != None:
            doc = fitz.open(None, content, "pdf")
        else:
            message = "Either a PDF filename or content must be provided."
            logging.error(message)
            raise Exception(message)
        
        if not doc.is_pdf:
            message = "Document is not a valid PDF."
            logging.error(message)
            doc.close()
            raise Exception(message)

        results = []
        # To get better resolution
        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        pageCount = 1
        for page in doc: # iterate over pdf pages
            
            pix = page.get_pixmap(matrix=mat)  # render page to an image
            page_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            (table_bounds, model) = self.find_tables(page_image) 
            tables = []
            for table in table_bounds:
                table_data = {}
                
                # Enlarge box since the default cuts it too close to the boundaries
                expanded_box = table['boxes'].tolist()[0]
                padding = [-10, -8, 12, 10]  # x1, y1, x2, y2
                for i in range(0, len(padding)):
                    expanded_box[i] += padding[i]  # add padding to assure all data is contained in the identified table box
                table_data['box'] = tuple(expanded_box)
                table_data['table_image'] = page_image.crop(table_data['box'])
                table_data['table_content'] = Table(image = table_data['table_image'])
                table_data['score'] = table['scores'][0]
                table_data['label'] = table['labels'][0]
                tables.append(table_data)
            page_data = {}
            page_data['image'] = page_image
            page_data['tables'] = tables
            page_data['model'] = model
            page_data['pageNum'] = pageCount
            results.append(page_data)
            pageCount +=1
        doc.close()
        return results


    # Function to export intermediate outputs such as full page image, full table image, and table bounding boxes
    def output_table_steps(self, folder_path):
        # Setup the output
        folder_path = Path(folder_path)
        if not os.path.exists(str(folder_path)):
            os.makedirs(str(folder_path))

        # Save the raw tables (post OCR, without cleaning)
        raw_excel_filename = str(Path(str(folder_path) + '/raw_excel.xlsx'))
        self.to_excel(filename=raw_excel_filename, raw = True)

        # Iterate through the pages in the file
        page_id = 0
        for page in self.page_data:
            page_id += 1

            # Save image of the page
            page['image'].save(str(folder_path) + '/page_'+str(page_id)+'.jpg')
            results = self.find_tables(page['image'])
            self.plot_table_results(page['image'], results[0][0]['scores'], results[0][0]['labels'], results[0][0]['boxes'], results[1], str(folder_path) + '/page_'+str(page_id)+'full'+'.jpg')
            
            # Iterate through the tables on the page (may be more than one)
            table_id = 0
            for table in page['tables']:
                table_id += 1

                # Save the image of the table with the bounding box
                table_id_string = 'table_' + str(page_id) + '-' + str(table_id)
                table['table_image'].save(str(folder_path) + "/" + table_id_string + '.jpg')
                
                # Save the bounding boxes for the table structure
                table['table_content'].plot_bounding_boxes(str(folder_path) + "/" + table_id_string + '_boxes')

                # Save the pre ocr table
                table['table_content'].save_pre_ocr_table(str(folder_path) + "/" + table_id_string + "_pre_ocr_cells/")
   

    def to_excel(self, filename='all_excel.xlsx', raw = False):
        if self.page_data == None:
            logging.warn("No page data to write to excel. No output file generated ")
            return

        logging.info("Writing table data to excel.")
        with pd.ExcelWriter(filename) as writer:
            for page_dict in self.page_data: #For each page
                counter = 1
                for table_dict in page_dict['tables']:
                    table = table_dict['table_content']
                    page_num = page_dict['pageNum']
                    sheet_name =  'Page' + str(page_num) + '_' + str(counter) 
                    if raw:
                        df = table.get_raw_dataframe()
                    else:
                        df = table.get_as_dataframe()
                    df.to_excel(writer, sheet_name=sheet_name, index=False) #Write it to a sheet in the output excel
                    counter += 1
        logging.info("Finished writing table data to excel.")
        return filename
