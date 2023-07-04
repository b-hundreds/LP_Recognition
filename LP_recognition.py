import cv2
import numpy as np
from ultralytics import YOLO
from support_function import *

# Load model for detection and recognition task
model_detection = YOLO('./static/models/best.pt')
model_ocr = YOLO('./static/models/best_ocr1.pt')



def lp_recognition(path, filename):

  # read image from path
  img = cv2.imread(path)
  img = rotate_image(img, 20)   # Roate image for test

  results = model_detection.predict(img) 

  list_crop_image = []
  list_coor_box = []
  list_plate_number = []
  list_probs = []
  for result in results:
    boxes = result.boxes.cpu().numpy() 
    
    # Check if model can't any plate
    if len(boxes) == 0:
      h, w, _ = img.shape
      cv2.imwrite('./static/predict/{}'.format(filename), img)
      return ["ERROR"], [(0,0,0,0,0)]
    
    # Draw bounding box, get crop image and coordinates
    for box in boxes:
      r1 = box.xyxy[0].astype(int)
      crop_image = img[r1[1]:r1[3], r1[0]:r1[2]].copy()
      list_crop_image.append(crop_image)
      list_coor_box.append(r1)
      cv2.rectangle(img, r1[:2], r1[2:], (100, 200, 200), 2)
  for i in range(len(list_crop_image)):
    list_prob = []
    crop_image = list_crop_image[i]
    r1 = list_coor_box[i]

    results1 = model_ocr.predict(crop_image)

    names = model_ocr.names   # Get list of label 

    for result in results1:
      boxes = result.boxes.cpu().numpy()    
      probs = boxes.conf    # Get probility of boxes
      if len(probs) == 0:
        return ["ERROR"], [(0,0,0,0,0)]
      list_r2 = []
      list_cls = []      
      for box in boxes:
        name = box.cls
        r2 = box.xyxy[0].astype(int)
        cv2.rectangle(img, r1[:2] + r2[:2], r1[:2] + r2[2:], (100, 100, 200), 2)

        # Append to list of coordinates and label of boxes
        list_r2.append(r2)
        list_cls.append(names[int(name[-1])])

      r2_array = np.array(list_r2).astype(int)
      cls_array = np.array(list_cls).reshape(-1, 1)
      probs = np.array(probs).reshape(-1, 1)
      # Get matrix with [[x1, y1, z1, t1], [x2, y2, z2, t2], ...] where xi, yi, zi, ti: left, upper, right, lower coordinates
      r2_arr = np.concatenate((r2_array, cls_array, probs), axis=1)

      # Check if two or more boxes have high iou and delete boxes having lower probility
      list_index_labels = find_index(r2_arr)  
      delete_label = []
      for list_index_label in list_index_labels:
        for ele in list_index_label[1:]:
          delete_label.append(ele)
      r2_arr = np.delete(r2_arr, delete_label, axis=0)

      #r2_arr = r2_arr[r2_arr[:, 1].astype(int).argsort()]   # Sort matrix in creasing direction of upper coordinates 

      # Calculate distance of upper coordinates in a row  
      #check_arr = np.zeros((len(r2_arr), 1))
      #check_arr[:len(r2_arr)-1, 0] = r2_arr[1:, 1]
      #check_arr1 = abs(check_arr - r2_arr[:, 1].astype(int).reshape(-1, 1))

      #max_value, index_max = find_max_and_index(check_arr1)

      # Check if plate is 1 line or 2 lines
      ratio = (np.max(r2_arr[:, 3].astype(int)) - np.min(r2_arr[:, 1].astype(int))) / (np.max(r2_arr[:, 2].astype(int)) - np.min(r2_arr[:, 0].astype(int)))
      if ratio > 0.75 and ratio < 1.33:
        mean = np.mean(r2_arr[:, 1].astype(int))
        r2_arr = r2_arr[r2_arr[:, 0].astype(int).argsort()]

        num_top = ""
        num_bot = ""
        for i in range(len(r2_arr)):
          if int(r2_arr[i, 1]) < mean:
            num_top += r2_arr[i, 4]
            list_prob.append(r2_arr[i, 5])
          else:
            num_bot += r2_arr[i, 4]
            list_prob.append(r2_arr[i, 5])

        plate_number = num_top + '-' + num_bot
        cv2.putText(img, plate_number, (r1[0], r1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imwrite('./static/predict/{}'.format(filename), img)
        list_plate_number.append(plate_number)
        list_probs.append(list_prob)
      else:
        r2_arr = r2_arr[r2_arr[:, 0].astype(int).argsort()]
        plate_number = ''
        for i in range(len(r2_arr)):
          plate_number += r2_arr[i, 4]
          list_prob.append(r2_arr[i, 5])
        cv2.putText(img, plate_number, (r1[0], r1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imwrite('./static/predict/{}'.format(filename), img)
        list_plate_number.append(plate_number)
        list_probs.append(list_prob)
  return list_plate_number, list_probs
    