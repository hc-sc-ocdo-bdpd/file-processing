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
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from table_tools import get_bounding_boxes, remove_duplicate_limits
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
        row_thresh, col_thresh = 4, 4
        self.row_limits = remove_duplicate_limits(self.row_limits, row_thresh)  # threshold is in pixels
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


    def get_cropped_rows(self):
        self.row_limits.sort()
        cropped_rows = []
        width, height = self.image.size
        x1 = 0
        x2 = width
        y2 = 0
        for limit in self.row_limits:
            y1 = y2
            y2 = limit
            cropped_rows.append(self.image.crop([x1,y1,x2,y2]))
        
        # Do the last row to the end of the image
        y1 = y2
        y2 = height
        cropped_rows.append(self.image.crop([x1,y1,x2,y2]))
        return cropped_rows
    
    ## TODO: refactor to eliminate code duplication between this method and get_cropped_rows()
    ## TODO: Need to consider that the left most and right most box seems to crop some of the cell
    def get_cropped_columns(self, image):
        self.column_limits.sort()
        x2 = 0
        cropped_columns = []
        width, height = image.size
        y1 = 0
        y2 = height
        for limit in self.column_limits:
            x1 = x2
            x2 = limit
            cropped_columns.append(image.crop([x1,y1,x2,y2]))
        
        # Do the last column to the end of the image
        x1 = x2
        x2 = width
        cropped_columns.append(image.crop([x1,y1,x2,y2]))
        return cropped_columns

    def plot_image(self, image):
        plt.figure()
        plt.imshow(image)
        plt.show()


    def extract_table_content(self):
        row_images = self.get_cropped_rows()
        rows = []
        for row in row_images:
            row_cell_text = []
            #row.show()
            if row.size[1] > 0:
                cells = self.get_cropped_columns(row)
                for cell in cells:
                    width, height = cell.size
                    if width > 0:
                        cell = cell.resize((int(width*2.5), int(height*2.5)))
                        #self.plot_image(cell)
                        row_cell_text.append(pytesseract.image_to_string(cell))
                        #print(row_cell_text[-1])
                rows.append(row_cell_text)
        if len(rows) < 1:  # if read table is only one row
            rows.append(['']*len(rows[0]))
        self.table_data = pd.DataFrame.from_records(rows[1:], columns=rows[0])


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


    def get_as_dataframe(self):
        return self.table_data
    
    def get_bounding_box_list(self):
        return self.table_structure['boxes'].tolist()
    
    def get_labels(self):
        return self.table_structure['labels'].tolist()
    
    def get_scores(self):
        return self.table_structure['scores'].tolist()

    # Extract the table in xlsx format (add other tools for exporting the table in excel format)
    def to_excel(self):
        self.table_data.to_excel(str(self.table_structure['boxes'][0]))         
