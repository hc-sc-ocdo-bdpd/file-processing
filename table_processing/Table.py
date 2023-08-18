'''
From: https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Table%20Transformer/Using_Table_Transformer_for_table_detection_and_table_structure_recognition.ipynb
Also from: https://huggingface.co/docs/transformers/model_doc/table-transformer
and lastly this: https://github.com/microsoft/table-transformer
'''

from transformers import TableTransformerForObjectDetection
from PIL import Image
import pytesseract
import os
import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from table_tools import get_bounding_boxes, remove_duplicate_limits, clean_cell_text
pytesseract.pytesseract.tesseract_cmd = os.path.join('C:/Users',getpass.getuser(),'AppData/Local/Programs/Tesseract-OCR/tesseract.exe')


class Table:

    # Constructor for the table class. Accepts an image of the table.
    # Todo: accept another data structure as well for building a table without OCR
    def __init__(self, image = None):
        if image != None:
            self.image = image
            self._load_model()
            self._find_bounding_boxes()
            self._calculate_row_column_limits()
            self.extract_table_content()


    def _load_model(self):
        self.model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")


    def _find_bounding_boxes(self):
        self.table_structure, self.model = get_bounding_boxes(self.image, self.model)
        self.table_structure = self.table_structure[0]  #[0] as the boxes are returns a list of table structures of length 1

    def _calculate_raw_row_column_limits(self):
        # Use boundaries of bounding boxes to set row and column limits
        self.row_limits = []
        self.column_limits = []
        for box in self.get_bounding_box_list():
            x1,y1,x2,y2 = box
            self.row_limits.append(y1)
            self.row_limits.append(y2)
            self.column_limits.append(x1)
            self.column_limits.append(x2)
        self.row_limits.sort()
        self.column_limits.sort()
        

    def _calculate_row_column_limits(self):
        self._calculate_raw_row_column_limits()
        row_thresh, col_thresh = 8, 16   # threshold is in pixels
        self.row_limits = remove_duplicate_limits(self.row_limits, row_thresh)  
        self.column_limits = remove_duplicate_limits(self.column_limits, col_thresh)

        # Remove left-most and right most column limits to handle clipping issue (temporary fix) and replace them with the image limits
        self.column_limits.sort()
        self.column_limits.pop(0)
        self.column_limits.pop()

        # Add image boundaries to the row and column limits
        width, height = self.image.size
        self.row_limits.append(0)
        self.row_limits.append(height)
        self.column_limits.append(0)
        self.column_limits.append(width)     
        
        self.row_limits = remove_duplicate_limits(self.row_limits, row_thresh)
        self.column_limits = remove_duplicate_limits(self.column_limits, col_thresh)  


    def plot_image(self, image):
        plt.figure()
        plt.imshow(image)
        plt.show()
        plt.close()


    # Transform the table into a list of lists representation
    # Consists of images of the individual cells in the table  
    # Generates self.table_pre_ocr  
    def generate_table_pre_ocr(self):
        row_images = get_cropped_rows(self.image, self.row_limits)
        self.table_pre_ocr = []
        for row in row_images:
            row_pre_ocr = []
            if row.size[1] > 0:
                cells = get_cropped_columns(row, self.column_limits)
                for cell in cells:
                    width, height = cell.size
                    if width > 0:
                        row_pre_ocr.append(cell)
            self.table_pre_ocr.append(row_pre_ocr)

    # Generates a datafram representation of the table contents using OCR
    # No post OCR cleanup
    # Generates self.raw_table_data
    def generate_raw_table_text(self):
        self.generate_table_pre_ocr()
        raw_rows = []
        for row in self.table_pre_ocr:
            raw_cells = []
            for cell in row:
                width, height = cell.size
                if width > 0:
                    cell = cell.resize((int(width*2.5), int(height*2.5)))
                    ocr_text = pytesseract.image_to_string(cell)
                    raw_cells.append(ocr_text)
            raw_rows.append(raw_cells)
        self.raw_table_data = pd.DataFrame.from_records(raw_rows[1:], columns=raw_rows[0])



    def extract_table_content(self):
        self.generate_raw_table_text()
        self.table_data = self.raw_table_data.applymap(clean_cell_text)

    
    def plot_bounding_boxes(self, file_name):
        # colors for visualization
        COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
                  [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]
        
        plt.figure(figsize=(16,10))
        plt.imshow(self.image)
        ax = plt.gca()
        colors = COLORS * 100
        boxes = self.get_bounding_box_list()
        labels = self.get_labels()
        scores = self.get_scores()
        for score, label, (xmin, ymin, xmax, ymax), c in zip(scores, labels, boxes, colors):
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                    fill=False, color=c, linewidth=3))
            text = f'{self.model.config.id2label[label]}: {score:0.2f}'
            ax.text(xmin, ymin, text, fontsize=15,
                    bbox=dict(facecolor='yellow', alpha=0.5))
        plt.axis('off')
        plt.savefig(file_name + ".jpg")
        plt.close()


    # Return the raw ocr table content
    def get_raw_dataframe(self):
        return self.raw_table_data
    

    # Save intermediate steps steps
    def save_pre_ocr_table(self, file_path):
        if not os.path.exists(str(file_path)):
            os.makedirs(str(file_path))
        row_id = 0
        for row in self.table_pre_ocr:
            column_id = 0
            for cell in row:
                file_name = file_path + "/row_" + str(row_id) + "_column_" + str(column_id) + ".jpg"
                cell.save(file_name)
                column_id += 1
            row_id += 1


    def get_as_dataframe(self):
        return self.table_data
    
    def get_bounding_box_list(self):
        return self.table_structure['boxes'].tolist()
    
    def get_labels(self):
        return self.table_structure['labels'].tolist()
    
    def get_scores(self):
        return self.table_structure['scores'].tolist()   


def get_cropped_rows(image, row_limits):
    row_limits.sort()
    cropped_rows = []
    width, height = image.size
    x1 = 0
    x2 = width
    y2 = 0
    for limit in row_limits:
        y1 = y2
        y2 = limit
        cropped_rows.append(image.crop([x1,y1,x2,y2]))

    return cropped_rows

## TODO: refactor to eliminate code duplication between this method and get_cropped_rows()
def get_cropped_columns(image, column_limits):
    column_limits.sort()
    x2 = 0
    cropped_columns = []
    width, height = image.size
    y1 = 0
    y2 = height
    for limit in column_limits:
        x1 = x2
        x2 = limit
        cropped_columns.append(image.crop([x1,y1,x2,y2]))
        
    return cropped_columns