

from transformers import DetrImageProcessor
import torch
import os
import pandas as pd

def get_bounding_boxes(image, model):
#    width, height = image.size
#    image.resize((int(width*0.5), int(height*0.5)))
    feature_extractor = DetrImageProcessor()
    encoding = feature_extractor(image, return_tensors="pt")
#    encoding.keys()
    with torch.no_grad():
        outputs = model(**encoding)
    width, height = image.size
    bounding_boxes = feature_extractor.post_process_object_detection(outputs, threshold=0.7, target_sizes=[(height, width)])
    return bounding_boxes, model

def calculate_intersection(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    if x2 < x1 or y2 < y1:
        return None
    else:
        return [x1, y1, x2, y2]
    

def remove_duplicate_limits(limit_list, threshold):
    unique = []
    for limit in limit_list:
        if not True in [within_threshold(limit, x, threshold) for x in unique]:
            unique.append(limit)
    unique.sort()
    return unique


def within_threshold(a, b, threshold):
    return abs(b - a) < abs(threshold)


def _calculate_raw_row_column_limits(bbox_list):
    # Use boundaries of bounding boxes to set row and column limits
    row_limits = []
    column_limits = []
    for box in bbox_list:
        x1,y1,x2,y2 = box
        row_limits.append(y1)
        row_limits.append(y2)
        column_limits.append(x1)
        column_limits.append(x2)
    row_limits.sort()
    column_limits.sort()

    return(column_limits,row_limits)
    

def _calculate_row_column_limits(image_dim, bbox_list):
    column_limits, row_limits =_calculate_raw_row_column_limits(bbox_list)
    row_thresh, col_thresh = 8, 16
    row_limits = remove_duplicate_limits(row_limits, row_thresh)
    column_limits = remove_duplicate_limits(column_limits, col_thresh)

    # Remove left-most and right most column limits to handle clipping issue (temporary fix) and replace them with the image limits
    column_limits.sort()
    column_limits.pop(0)
    column_limits.pop()

    # Add image boundaries to the row and column limits
    width, height = image_dim
    row_limits.append(0)
    row_limits.append(height)
    column_limits.append(0)
    column_limits.append(width)      
    
    # Make sure that adding the new limits didn't add dubplicates
    row_limits = remove_duplicate_limits(row_limits, row_thresh)
    column_limits = remove_duplicate_limits(column_limits, col_thresh)

    return(column_limits, row_limits)  


# Map function for cleaning the text in a dataframe
def clean_cell_text(raw_text):
    processed_text = raw_text
    if processed_text != '':

        # verify if separator character at start (ignoring whitespaces) of string
        if processed_text[len(processed_text) - len(processed_text.lstrip())] == '|':
            processed_text = processed_text[len(processed_text) - len(processed_text.lstrip()) + 1:]             
                
            # verify if separator character at end (ignoring whitespaces) of string
            if processed_text[-(len(processed_text) - len(processed_text.rstrip()) + 1)] == '|':
                processed_text = processed_text[:-(len(processed_text) - len(processed_text.rstrip()) + 1)]

    # remove all leading and trailing whitespaces
    processed_text = processed_text.strip()
    raw_text.replace(processed_text)
