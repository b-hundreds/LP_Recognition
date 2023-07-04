import cv2
import numpy as np


def rotate_image(image, angle):
  height, width = image.shape[:2]
  rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
  rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
  return rotated_image

# Find list of index label with high IOU
def find_index(matrix):
  labels = matrix[:, -2]
  iou_threshold = 0.5
  list_selected_labels = []
  for i in range(len(matrix)):
    selected_labels = []
    bbox1 = matrix[i, :4].astype(int)  # Get coordinates of bouding box i
    flag = False

    for j in range(i + 1, len(matrix)):
      bbox2 = matrix[j, :4].astype(int)  # Lấy tọa độ của bounding box thứ j
      iou = calculate_iou(bbox1, bbox2)  # Calculate IOU between bouding box i and j

      if iou > iou_threshold:
        flag = True
        selected_labels.append(j)
    if flag == True:
      selected_labels.insert(0, i)       
      list_selected_labels.append(selected_labels)
  return list_selected_labels

# Calculate IOU of 2 bouding box 
def calculate_iou(bbox1, bbox2):
  x1_min, y1_min, x1_max, y1_max = bbox1
  x2_min, y2_min, x2_max, y2_max = bbox2

  area1 = (x1_max - x1_min) * (y1_max - y1_min)
  area2 = (x2_max - x2_min) * (y2_max - y2_min)

  x_min = max(x1_min, x2_min)
  y_min = max(y1_min, y2_min)
  x_max = min(x1_max, x2_max)
  y_max = min(y1_max, y2_max)

  intersection_area = max(0, x_max - x_min) * max(0, y_max - y_min)

  iou = intersection_area / (area1 + area2 - intersection_area)
  return iou
