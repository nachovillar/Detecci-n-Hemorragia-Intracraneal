# -*- coding: utf-8 -*-
"""
Created on Mon May 23 11:55:30 2022

@author: Villar
"""

import shutil
import os

NINETY_PERCENT =14381

data = '../../train_data/images'

file_destination_images_train = 'C:/Users/HP/Desktop/Tesis/train_data/images/train'
file_destination_labels_train = 'C:/Users/HP/Desktop/Tesis/train_data/labels/train'

file_destination_images_val = 'C:/Users/HP/Desktop/Tesis/train_data/images/val'
file_destination_labels_val = 'C:/Users/HP/Desktop/Tesis/train_data/labels/val'

dead_counter = 0
          
for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
    for nombre_fichero in ficheros:
        
        if dead_counter == NINETY_PERCENT:
            break
        
        nombre_archivo = nombre_fichero[0:-4]
        counter = 0
    
        for nombre_directorio_2, dirs_2, ficheros_2 in os.walk(data, topdown=True):
            for nombre_fichero_2 in ficheros_2:
                
                nombre_archivo_2 = nombre_fichero_2[0:-4]
                
                if nombre_archivo == nombre_archivo_2:
                    counter +=1
                
                if counter > 1:
                    
                    shutil.move(nombre_directorio + '\\' + nombre_archivo + '.jpg', file_destination_images_train) 
                    shutil.move(nombre_directorio + '\\' + nombre_archivo + '.txt', file_destination_labels_train)
                    
                    counter = 0
                    dead_counter += 1
                    print(dead_counter)


for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
    for nombre_fichero in ficheros:
               
        nombre_archivo = nombre_fichero[0:-4]
        counter = 0
        
        for nombre_directorio_2, dirs_2, ficheros_2 in os.walk(data, topdown=True):
            for nombre_fichero_2 in ficheros_2:
                
                nombre_archivo_2 = nombre_fichero_2[0:-4]
                
                if nombre_archivo == nombre_archivo_2:
                    counter +=1
                    
                if counter > 1:
                    
                    shutil.move(nombre_directorio + '\\' + nombre_archivo + '.jpg', file_destination_images_val) 
                    shutil.move(nombre_directorio + '\\' + nombre_archivo + '.txt', file_destination_labels_val)
                    
                    counter = 0

        
        

                    
                
                
                    