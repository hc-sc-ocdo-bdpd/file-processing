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

from Table import Table
from table_tools import get_bounding_boxes

class Table_Detector:

    # Requires EITHER an image of a page or a path to a pdf file.
    def __init__(self, file = None):
        self.page_data = None
        if file != None:
            self.page_data = self.get_tables_from_pdf(file)

    def get_page_data(self):
        return self.page_data

    # This will need to be refactored to use the new Table class
    def plot_table_results(self, pil_img, scores, labels, boxes, model):
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
        plt.show()


    def find_tables(self, image):
        model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
        return get_bounding_boxes(image, model)

    def get_tables_from_pdf(self, filename):
        doc = fitz.open(filename)
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
                table_data['box'] = tuple(table['boxes'].tolist()[0])
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
        return results

    # Todo: Implement this method    
    def to_excel(self, filename='all_excel.xlsx'):
        with pd.ExcelWriter(filename) as writer:
            for page_dict in self.page_data: #For each page
                for table_dict in page_dict['tables']:
                    table = table_dict['table_content']
                    page_num = page_dict['pageNum']
                    sheet_name =  'Page' + str(page_num) + ' ' + str(table.getBBox()[-1]).replace('[','').replace(']','') 
                    df = table.get_as_dataframe()
                    df.to_excel(writer, sheet_name=sheet_name, index=False) #Write it to a sheet in the output excel
                   




filename = "resources/multipletab.pdf"
table_detector = Table_Detector(file = filename)
table_data = table_detector.get_page_data()
table_detector.to_excel()

# Other todo 
# - Set up a benchmark test to assess performance

'''
for page_data in page_table_results:
    table_data_list = page_data['tables']

    (image, cropped_image, table_bounds, model) = result
    for table in table_bounds:
        plot_table_results(image, table['scores'], table['labels'], table['boxes'], model)
        score = table['scores'].tolist()
        label = table['labels'].tolist()
        (xmin, ymin, xmax, ymax) = table['boxes'].tolist()
'''
