# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:40:33 2022

@author: Villar
"""

import shutil
import os

if __name__ == '__main__':
    bounding_boxes = '../Bounding_Boxes'
    images = '../train_data_fusion_Gonzalo'

    file_destination_images = '../train_data'

    for nombre_directorio, dirs, ficheros in os.walk(bounding_boxes, topdown=True):
        for nombre_fichero in ficheros:

            nombre_archivo = nombre_fichero[0:-4]

            for nombre_directorio_images, dirs_images, ficheros_images in os.walk(images, topdown=True):
                for nombre_fichero_image in ficheros_images:

                    nombre_archivo_image = nombre_fichero_image[0:-4]

                    if nombre_archivo == nombre_archivo_image:
                        shutil.move(f'{nombre_directorio_images}\\{nombre_archivo_image}.png', file_destination_images)
