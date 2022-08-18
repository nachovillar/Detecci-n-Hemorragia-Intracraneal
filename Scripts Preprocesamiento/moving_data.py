# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:36:19 2022

@author: Villar
"""

import shutil
import os

data = '../../data_training'

for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
    for nombre_fichero in ficheros:
        
        file_destination = 'C:/Users/HP/Desktop/Tesis/train_data/images'
        #print(nombre_directorio + '\\' + nombre_fichero)
        

        shutil.move(nombre_directorio + '\\' + nombre_fichero, file_destination)

