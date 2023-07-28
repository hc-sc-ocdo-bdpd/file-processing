

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
