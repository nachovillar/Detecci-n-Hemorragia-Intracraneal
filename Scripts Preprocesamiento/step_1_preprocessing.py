#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 20:15:04 2022

@author: joseignaciovillargallardo
"""
# Librerías plugin para lectura de los archivos dcm
#import gdcm
#import pylibjpeg
#import pylibjpeg-openjpeg

# Librería para crear directorios recursivamente
import mmcv

# Librería para trabajar las imágenes dicom
import pydicom

# Para el manejo y cálculo de matrices
import numpy as np

# procesamiento de archivos
import os

# Visualización
import matplotlib.pyplot as plt

# Dilatación morfológica en escala de grises de una imagen
from skimage import morphology

# Dar etiquetas de características a las matrices(imágenes)
from scipy import ndimage
from scipy.ndimage import binary_fill_holes

# Funciones de archivo utils.py
from utils import transform_to_hu, window_image

if __name__ == '__main__':

    data = '..\\Brain Hemorrhage Extended (BHX)'

    for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
        for nombre_fichero in ficheros:

            file_path = f'{nombre_directorio}\\{nombre_fichero}'
            print(f'Procesando el archivo: {file_path}')

            try:
                print(f'Leyendo archivo DICOM..')
                medical_image = pydicom.dcmread(file_path)
            except:
                print(f'No existe el archivo: {file_path}')
                exit(1)
            print('.OK!')

            patien_ID = medical_image.data_element('PatientID').value
            series_Number = medical_image.data_element('SeriesNumber').value
            instance_Number = medical_image.data_element('InstanceNumber').value

            print(f'Archivo: {patien_ID}-{series_Number}-{instance_Number}')

            print(f'\n\nTransformando el archivo a Unidades Hounsfield..')
            image = medical_image.pixel_array.astype(float)
            # Imprimir cabeceras del archivo
            hu_image = transform_to_hu(medical_image, image)
            print('.OK!')

            # Se hace un windowing para ver una escala de grises que permita ver el cerebro (40,80)
            print('\n\nRealizando Windowing para ver el cerebro..')
            brain_image = window_image(hu_image, 40, 80)
            print('.OK!')
            # morphology.dilation crea una segmentación de la imagen
            # Si un píxel está entre el origen y el borde de un cuadrado de tamaño
            # 5x5, el pixel pertenece a la misma clase.
            # En su lugar, podemos usar un círculo, utilizando: morphology.disk(2)
            # En este caso el pixel pertenece a la misma clase si es que esta está entre el origen
            # y el radio.
            print('\n\nAplicando Mask para eliminar ruido y elementos no deseados..')
            segmentation = morphology.dilation(brain_image, np.ones((5, 5)))
            labels, label_nb = ndimage.label(segmentation)
            label_count = np.bincount(labels.ravel().astype(int))
            #El tamaño de label_count es el número de clases/segmentaciones encontradas
            #No usamos la primera clase ya que es el fondo.
            label_count[0] = 0

            #Creamos una mask con la clase con más pixeles
            #En este caso debería ser el cerebro
            mask = labels == label_count.argmax()

            # Se mejora la mask del cerebro
            mask = morphology.dilation(mask, np.ones((5, 5)))
            mask = binary_fill_holes(mask)
            mask = morphology.dilation(mask, np.ones((3, 3)))

            # Dado que los píxeles de la máscara son ceros y unos
            # Podemos multiplicar la imagen original para mantener solo la región del cerebro
            masked_image = mask * brain_image
            print('.OK!')

            print(f'')
            route = f'../train_data/Patient-{patien_ID}/Series-{series_Number}'
            file = f'img-{series_Number}-{instance_Number}.png'
            print(f'Creando los directorios: {route}')
            mmcv.mkdir_or_exist(route)
            print('.Ok')
            print('Guardando Imagen en formato PNG para no perder información..')
            save_path = os.path.join(route, file)
            plt.imsave(save_path, masked_image, cmap='gray')
            print('.OK!')