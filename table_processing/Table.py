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
from table_tools import get_bounding_boxes, calculate_intersection
pytesseract.pytesseract.tesseract_cmd = os.path.join('C:/Users',getpass.getuser(),'AppData/Local/Programs/Tesseract-OCR/tesseract.exe')


class Table:

    # Constructor for the table class. Accepts an image of the table.
    # Todo: accept another data structure as well for building a table without OCR
    def __init__(self, image = None):
        if image != None:
            self.image = image
            self.rowSorted = []
            self.colSorted = []
            self.sortBBox()
            self.extract_table_content()

    def sortBBox(self):
        self.model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")
        self.table_structure = get_bounding_boxes(self.image, self.model)[0][0]


        tmpBox = self.getBBox()
        tmpLabel = self.getLabels()
        for i in range(len(tmpBox)):
            if tmpLabel[i] == 2:
                self.rowSorted.append(tmpBox[i])

        self.rowSorted = sorted(self.rowSorted, key=lambda x: x[1])

        for i in range(len(tmpBox)):
            if tmpLabel[i] == 1:
                self.colSorted.append(tmpBox[i])


        self.colSorted = sorted(self.colSorted, key=lambda x: x[0])


    def extract_table_content(self):
        # OCR all box content
        tableData=[]
        for row in self.rowSorted:
            text_buffer = []

            for col in self.colSorted:   
                res = calculate_intersection(row, col)
                cropped_image = self.image.crop(res)
                text = pytesseract.image_to_string(cropped_image)
                text_buffer.append(text)
            tableData.append(text_buffer) 

        # Make a table structure - likely a dataframe
        self.table_data = pd.DataFrame.from_records(tableData, columns=tableData[0])
        self.table_data = self.table_data.drop(0)

    def plot_bounding_boxes(self):
        # colors for visualization
        COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
                  [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]
        
        plt.figure(figsize=(16,10))
        plt.imshow(self.image)
        ax = plt.gca()
        colors = COLORS * 100
        boxes = self.getBBox()
        labels = self.getLabels()
        scores = self.get_scores()
        for score, label, (xmin, ymin, xmax, ymax), c in zip(scores, labels, boxes, colors):
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                    fill=False, color=c, linewidth=3))
            text = f'{self.model.config.id2label[label]}: {score:0.2f}'
            ax.text(xmin, ymin, text, fontsize=15,
                    bbox=dict(facecolor='yellow', alpha=0.5))
        plt.axis('off')
        plt.show()

    def get_as_dataframe(self):
        return self.table_data
    
    def getBBox(self):
        return self.table_structure['boxes'].tolist()
    
    def getLabels(self):
        return self.table_structure['labels'].tolist()
    
    def get_scores(self):
        return self.table_structure['scores'].tolist()

    # Extract the table in xlsx format (add other tools for exporting the table in excel format)
    def to_excel(self):
        self.table_data.to_excel(str(self.table_structure['boxes'][0]))         
