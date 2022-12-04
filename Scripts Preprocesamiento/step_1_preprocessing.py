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
from utils import transform_to_hu, window_image, crop_image

# Funciones para fusionar las imágenes con distintas Unidades Hounsfield
from utils import get_nonzero
from utils import genRGB

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
            # brain_image la utilizamos solo para crear la máscara
            brain_image = window_image(hu_image, 40, 80, True)
            # Subdura y soft_tissue son utilizadas para fusionarse y dar como resultado una imagen RGB de NxNx3
            subdural_image = window_image(hu_image, 80, 200, False)
            soft_tissue_image = window_image(hu_image, 300, 420, False)
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

            #Creamos una mask con la clase con más pixeles (cerebro)
            mask = labels == label_count.argmax()

            # Se mejoran las mask
            mask = morphology.dilation(mask, np.ones((5, 5)))
            mask = binary_fill_holes(mask)
            mask = morphology.dilation(mask, np.ones((3, 3)))

            # Utilizamos la máscara para el cerebro en las distintas imágenes con rangos de HU distintos
            # Así dejamos en las imágenes limpias, solo con la cabeza del paciente en la imagen
            brain_image_2 = window_image(hu_image, 40, 80, False)
            masked_image_brain = mask * brain_image_2
            masked_image_subdural = mask * subdural_image
            masked_image_soft_tissue = mask * soft_tissue_image
            print('.OK!')
            print(f'')

            print(f'Fusionando imágenes...')
            imRGB = genRGB(masked_image_brain, masked_image_subdural, masked_image_soft_tissue)
            print('.OK!')

            print('Cortando imagen...')
            try:
                print('Start of crop'.center(40, '*'))
                print(f'Archivo: {nombre_directorio}\\{nombre_fichero}')
                print(f'Imagen: {patien_ID}-{series_Number}-{instance_Number}.png')
                croped_image = crop_image(imRGB)
                print('end of crop'.center(42, '*'))
            except:
                print(f'ERROR: El siguiente archivo no pudo ser cortado: {nombre_directorio}\\{nombre_fichero}')
                continue
            print('.OK!')

            print(f'')
            route_imRGB = f'../train_data_fusion_Villar'
            route_croped_image = f'../train_data_fusion_Villar_croped'
            file = f'{patien_ID}-{series_Number}-{instance_Number}.png'
            print(f'Creando los directorios: {route_imRGB}')
            print(f'Creando los directorios: {route_croped_image}')
            mmcv.mkdir_or_exist(route_imRGB)
            mmcv.mkdir_or_exist(route_croped_image)
            print('.Ok')
            print('Guardando Imagen en formato PNG para no perder información..')
            save_path_imRGB = os.path.join(route_imRGB, file)
            save_path_croped_image = os.path.join(route_croped_image, file)
            plt.imsave(save_path_imRGB, imRGB, cmap='gray')
            plt.imsave(save_path_croped_image, croped_image, cmap='gray')
            print('.OK!')

