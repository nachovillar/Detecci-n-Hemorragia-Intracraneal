# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 16:31:57 2022

@author: Villar
"""

import cv2
import albumentations as A
import numpy as np
import pandas as pd
from PIL import Image
import os
from matplotlib import pyplot as plt
import matplotlib.patches as patches

# def visualize(image):
#     plt.figure(figsize=(10, 10))
#     plt.axis('off')
#     plt.imshow(image)
#     plt.show()

# def visualize_bbox(img, bbox, class_name, color=(255, 0, 0), thickness=5):
#     """Visualizes a single bounding box on the image"""
#     x_min, y_min, x_max, y_max = map(int, bbox)
#     cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, thickness)
#     return img

# def plot_examples(images, bboxes=None):
#     fig = plt.figure(figsize=(15, 15))
#     columns = 4
#     rows = 5

#     for i in range(1, len(images)):
#         if bboxes is not None:
#             img = visualize_bbox(images[i - 1], bboxes[i - 1], class_name="Hemorrhage")
#         else:
#             img = images[i-1]
#         fig.add_subplot(rows, columns, i)
#         plt.imshow(img)
#     plt.show()



images = '../train_data_3/images'
labels = '../train_data_3/labels'

environments = ['/train/', '/val/']
timer = 0
for nombre_directorio_imagen, dirs, ficheros_images in os.walk(images, topdown=True):
    for nombre_fichero_imagen in ficheros_images:
        
        fileName_images = str(nombre_directorio_imagen) + "/" + str(nombre_fichero_imagen)
        #print(fileName_images)
        id_image = nombre_fichero_imagen[0:-4]
        
        for environment in environments:
            if (("\\train/" in fileName_images) and (environment == "/train/")) or (("\\val/" in fileName_images) and (environment == "/val/")):
                
                id_label =  labels + environment + id_image + ".txt"  
                # print(id_label)                 
                label_file = pd.read_csv(id_label, sep=" ",header=None)
                arr = label_file.to_numpy()
                counter = 0
                
                for hemorrhage_type in arr[:, 0]:
                    if hemorrhage_type == 5 and counter <1:
                        timer += 1
                        print(timer)
                        print(id_image)
                        print("--------------------------------------------")
                        counter += 1
                        bboxes = []
                        hemorrhage_types = []
                        for ht in arr:
                
                            bb = ht[1:]
                            hem_type = ht[0]
                            bboxes.append(bb)
                            hemorrhage_types.append(hem_type)
                        
                        image = cv2.imread(fileName_images)
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                        # Pascal_voc (x_min, y_min, x_max, y_max), YOLO, COCO                        
                        transform = A.Compose(
                            [
                                A.Resize(width=1920, height=1080),
                                A.RandomCrop(width=1440, height=900),
                                A.Rotate(limit=40, p=0.9, border_mode=cv2.BORDER_CONSTANT),
                                A.HorizontalFlip(p=0.5),
                                A.VerticalFlip(p=0.1),
                                # A.RGBShift(r_shift_limit=25, g_shift_limit=25, b_shift_limit=25, p=0.9),
                                A.OneOf([
                                    A.Blur(blur_limit=3, p=0.5),
                                    A.ColorJitter(p=0.5),
                                ], p=1.0),
                            ], bbox_params=A.BboxParams(format="yolo", min_area=2048,
                                                        min_visibility=0.3, label_fields=[])
                        )                        
                        # print(bboxes[0])
                        images_list = [image]
                        saved_bboxes = [bboxes[0]]
                        # print(saved_bboxes)
                        counter_image = 1
                        
                        for i in range(5):
                            
                            transformed = transform(image=image, bboxes=bboxes)
                            transformed_image = transformed['image']
                            transformed_bboxes = transformed['bboxes']
                            cv2.imwrite(images + "/" + id_image + "(" + str(counter_image) + ").jpg", transformed_image)
                            
                            file = open(labels + "/" + id_image + "(" + str(counter_image) + ").txt", "w")
                            bboxes_counter = 0
                            
                            for i in transformed_bboxes:
                                
                                bbox_string = str(i).replace('(', "")     
                                bbox_string = bbox_string.replace(',', "") 
                                bbox_string = bbox_string.replace(')', "") 
                                if bboxes_counter > 0:
                                    file.writelines(str(int(hemorrhage_types[bboxes_counter])) + " " + bbox_string + os.linesep)
                                    bboxes_counter += 1
                                else:
                                
                                    bbox_string = str(i).replace('(', "")     
                                    bbox_string = bbox_string.replace(',', "") 
                                    bbox_string = bbox_string.replace(')', "")
                                    file.write(str(int(hemorrhage_types[bboxes_counter])) + " " + bbox_string + os.linesep)
                                    bboxes_counter += 1
                            
                            if len(transformed["bboxes"]) == 0:
                                continue
                        
                            images_list.append(transformed_image)
                            
                            saved_bboxes.append(transformed["bboxes"][0])
                            # print(saved_bboxes)
                            # print( len(images_list))
                            counter_image += 1
                        #plot_examples(images_list, saved_bboxes)
                        
            