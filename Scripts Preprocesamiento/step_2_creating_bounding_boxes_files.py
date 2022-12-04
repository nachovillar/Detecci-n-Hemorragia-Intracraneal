# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:30:30 2022

@author: Villar
"""
import torch
import utils
import pydicom
import pylibjpeg
import os
import pathlib

import pyspark as spark
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mmcv

if __name__ == '__main__':

    # -------------------------------------- CSVs -------------------------------------------------------------------------
    # Initial_Manual_Labeling = '1_Initial_Manual_Labeling.csv'
    # Extrapolation_to_All_Series = '2_Extrapolation_to_All_Series.csv'
    Extrapolation_to_Selected_Series = '3_Extrapolation_to_Selected_Series.csv'

    # data_Initial_Manual_Labeling = pd.read_csv(Initial_Manual_Labeling)
    # data_Extrapolation_to_All_Series = pd.read_csv(Extrapolation_to_All_Series)
    data_Extrapolation_to_Selected_Series = pd.read_csv(Extrapolation_to_Selected_Series)

    columns_of_interest = data_Extrapolation_to_Selected_Series.drop(
        ['SeriesInstanceUID', 'StudyInstanceUID', 'labelType'], axis=1)
    columns_of_interest = columns_of_interest.drop(columns_of_interest.columns[[0]], axis='columns')
    # ---------------------------------------------------------------------------------------------------------------------

    data = '..\\Brain Hemorrhage Extended (BHX)'

    characters = ['"', "'", "{", "x", ":", ",", "y", "w", "i", "d", "t", "h", "e", "g", "}"]

    bbx_directory = '../Bounding_Boxes'

    print('Creando directorio para alojar las Bounding Boxes...')
    try:
        mmcv.mkdir_or_exist(bbx_directory)
    except:
        raise Exception(f'ERROR: No se puede crear, ni existe el directorio {bbx_directory}')

    print('Directorio Creado!')

    # Le quitamos los caracteres innecesarios a las coordenadas de la columna
    for index, columns in columns_of_interest.iterrows():
        #columns[0] = SOPInstanceUID
        #columns[1] = Bounding Box
        #columns[2] = Hemorrhage Type
        bounding_box = columns[1]
        for x in range(len(characters)):

            bounding_box = bounding_box.replace(characters[x], "")
            bounding_box = bounding_box.replace("  ", " ")
            bb = bounding_box[1:]
        columns_of_interest['data'][index] = bb


    counter = 0
    for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
        for nombre_fichero in ficheros:

            counter += 1
            print(counter)

            file_path = f'{nombre_directorio}\\{nombre_fichero}'
            print(f'Procesando el archivo: {file_path}')

            if not (os.path.isfile(file_path)):
                print('La dirección no corresponde a un archivo...')
                continue

            try:
                print(f'Leyendo archivo DICOM..')
                medical_image = pydicom.dcmread(file_path)
            except:
                print(f'No existe el archivo: {file_path}')
                print(f'Archivo NO Procesado: {nombre_directorio}\\{nombre_fichero}')
                continue

            SOPInstanceUID = medical_image.data_element('SOPInstanceUID').value
            PatientID = medical_image.data_element('PatientID').value
            SeriesNumber = medical_image.data_element('SeriesNumber').value
            InstanceNumber = medical_image.data_element('InstanceNumber').value

            # Nombre y ruta del archivo que se creará para alojar las coordenadas y el tipo de hemorragia
            fileName = f"../Bounding_Boxes/{str(PatientID)}-{str(SeriesNumber)}-{str(InstanceNumber)}.txt"

            for index, columns in columns_of_interest.iterrows():

                ID_DICOM = columns[0]
                bbx = columns[1]
                Hemorrhage = columns[2]

                bbox = np.array(bbx.split())

                try:
                    if str(SOPInstanceUID) == str(ID_DICOM):

                        try:
                            x_min = float(bbox[0])
                            y_min = float(bbox[1])
                            w = float(bbox[2])
                            h = float(bbox[3])

                            x_center = x_min + (w / 2)
                            y_center = y_min + (h / 2)

                            # Normalizamos
                            x_center /= 512
                            y_center /= 512
                            w /= 512
                            h /= 512
                        except:
                            print('ERROR: no se pudieron calcular las coordenadas')
                            print(f'Archivo NO Procesado: {file_path}')
                            print(f'Nombre archivo no Procesado: {fileName}')
                            continue

                        # Si es un archivo agregamos la coordenada al archivo existente
                        # si no existe, creamos el archivo y escribimos la coordenada en él
                        if os.path.isfile(fileName):
                            print(f'{fileName}: Agregando Coordenada y tipo de Hemorragia...')
                            try:
                                file = open(fileName, "a")
                            except OSError as e:
                                print(f'No se pudo agregar coordenada en el archivo: {fileName}')
                                print(e)
                                continue

                            try:
                                if Hemorrhage == 'Intraparenchymal':
                                    file.writelines("0 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Subarachnoid':
                                    file.writelines("1 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Intraventricular':
                                    file.writelines("2 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Epidural':
                                    file.writelines("3 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Subdural':
                                    file.writelines("4 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Chronic':
                                    file.writelines("5 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                file.close()
                            except:
                                print(f'No se pudo agregar en el archivo: {fileName}')
                                file.close()
                                continue


                        else:

                            print(f'{fileName}: Creando Archivo con Coordenada y tipo de Hemorragia...')

                            try:
                                file = open(fileName, "w")
                            except OSError as e:
                                print(f'No se pudo crear el archivo: {fileName}')
                                print(e)
                                continue

                            try:
                                if Hemorrhage == 'Intraparenchymal':
                                    file.write("0 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Subarachnoid':
                                    file.write("1 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Intraventricular':
                                    file.write("2 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Epidural':
                                    file.write("3 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Subdural':
                                    file.write("4 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                elif Hemorrhage == 'Chronic':
                                    file.write("5 " + str(x_center) + " " +
                                                    str(y_center) + " " +
                                                    str(w) + " " +
                                                    str(h)
                                                    + os.linesep)

                                file.close()
                            except:
                                print(f'No se pudo escribir en el archivo: {fileName}')
                                file.close()
                                continue

                except:
                    print('ERROR: No se pudo escribir en el archivo...')
                    print(f'Archivo NO Procesado: {nombre_directorio}\\{nombre_fichero}')
                    print(f'Nombre archivo no Procesado: {fileName}')
                    continue


            if os.path.isfile(fileName):
                print(f'Archivo DICOM Finalizado: {file_path}')
                print(f'Archivo Coordenadas Finalizado: {fileName}')
                print('.OK!\n')
            else:
                print(f'El siguiente archivo no presenta coordenadas: {file_path}')
                print(f'El archivo se iba a nombrar: {fileName}')
                print('.OK!\n')










