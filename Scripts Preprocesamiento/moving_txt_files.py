# -*- coding: utf-8 -*-
"""
Created on Sun May 22 21:30:08 2022

@author: Villar
"""

import shutil
import os

data = '../Data/BHX'

for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
    for nombre_fichero in ficheros:
        
        file_destination = 'C:/Users/HP/Desktop/Tesis/train_data/images'
        #print(nombre_directorio + '\\' + nombre_fichero)
        
        if ".txt" in nombre_fichero:
            shutil.move(nombre_directorio + '\\' + nombre_fichero, file_destination)