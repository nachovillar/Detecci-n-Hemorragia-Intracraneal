# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:40:33 2022

@author: Villar
"""

import shutil
import os

data = '../../train_data/images/data_val'

file_destination_images_val = 'C:/Users/HP/Desktop/Tesis/train_data/images/val'
file_destination_labels_val = 'C:/Users/HP/Desktop/Tesis/train_data/labels/val'

for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
    for nombre_fichero in ficheros:
               
        nombre_archivo = nombre_fichero[0:-4]
        
        if 'txt' in nombre_fichero:
            
            shutil.move(nombre_directorio + '\\' + nombre_archivo + '.jpg', file_destination_images_val) 
            shutil.move(nombre_directorio + '\\' + nombre_archivo + '.txt', file_destination_labels_val)