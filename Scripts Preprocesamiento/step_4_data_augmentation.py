# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 16:31:57 2022

@author: Villar
"""

import cv2
import albumentations as A
import numpy as np
import pandas as pd
import os

if __name__ == '__main__':

    print(f'El siguiente programa está encargado de hacer aumento de datos, las cuales son las siguientes:\n'
          f'\n1.-Intraparenchymal'
          f'\n2.-Subarachnoid'
          f'\n3.-Intraventricular'
          f'\n4.-Epidural'
          f'\n5.-Subdural'
          f'\n6.-Chronic')
    
    selected_hemorrhage = int(input('\n¿A cuál hemorragia desea aplicar aumento de datos?: ')) - 1

    amount = int(input('\n¿Cuantos aumentos por cada imagen?: '))

    if ((selected_hemorrhage < 0) or (selected_hemorrhage > 5) or (not isinstance(selected_hemorrhage, int))):
        raise Exception(f'El valor ingresado {selected_hemorrhage} no es una opción esperada. Cerrando...')

    print('')

    # Rutas de las imágenes y Bounding Boxes
    images = '../train_data'
    labels = '../Bounding_Boxes'

    # Recorremos la carpeta con las imágenes
    for nombre_directorio_imagen, dirs, ficheros_images in os.walk(images, topdown=True):
        for nombre_fichero_imagen in ficheros_images:

            # Imagen que estamos tratando
            fileName_images = f'{nombre_directorio_imagen}/{nombre_fichero_imagen}'

            # Le quitamos el ".png" al nombre del fichero
            id_image = nombre_fichero_imagen[0:-4]

            # Ya que las imágenes tienen el mismo nombre que los archivos con sus Bounding Boxes correspondientes
            # entonces el nombre del archivo se distingue en su ruta y nombre en el formato
            label = f'{labels}/{id_image}.txt'

            # Leemos el archivo de texto que tiene las etiquetas y bounding boxes de la imagen
            try:
                print(f'Leyendo el archivo label: {label}')
                label_file = pd.read_csv(label, sep=" ", header=None)
            except:
                print(f'ERROR: No existe el archivo: {label_file}')
                continue

            arr = label_file.to_numpy()

            # Contador para ver la cantidad de veces que se repite un tipo de hemorragia en un archivo de bounding boxes
            type_hemorrhage_counter = 0
            # Recorremos los archivos de texto si es que contienen el tipo de hemorragia a la cual queremos hacer aumento de datos
            # Y obviamente no lo volveremos a revisar si el tipo de hemorragia se repite dentro del mismo archivo
            for hemorrhage_type in arr[:, 0]:
                if int(hemorrhage_type) == selected_hemorrhage and type_hemorrhage_counter < 1:

                    print(f'\nRealizando aumento de datos para: {id_image}')

                    type_hemorrhage_counter += 1

                    # Arreglos para almacenar los datos de bounding boxes y tipos de hemorragia dentro del archivo
                    hemorrhage_types = []
                    bboxes = []

                    # Recorremos el archivo para extraer la información de los arreglos anteriores
                    for ht in arr:
                        hem_type = int(ht[0])
                        bb = ht[1:]
                        hemorrhage_types.append(hem_type)
                        bboxes.append(bb)

                    # Leemos las imágenes
                    image = cv2.imread(fileName_images)

                    # Pascal_voc (x_min, y_min, x_max, y_max), YOLO, COCO
                    transform = A.Compose(
                                            [
                                                A.Transpose(),
                                                A.ToGray(),
                                                A.Rotate(limit=40, p=1.0, border_mode=cv2.BORDER_CONSTANT),
                                                A.HorizontalFlip(p=0.5),
                                                A.VerticalFlip(p=0.5),
                                                A.RGBShift(r_shift_limit=25, g_shift_limit=25, b_shift_limit=25, p=0.5),
                                                A.OneOf([
                                                    A.Blur(blur_limit=(3, 4), p=0.5),
                                                    A.ColorJitter(p=0.5),
                                                ], p=1.0),
                                            ], bbox_params=A.BboxParams(format="yolo", label_fields=[])
                                        )

                    # Contador para dar nombre distinto a las imágenes y labels creadas
                    counter_image = 1

                    # Creamos una aumento de datos del tipo de hemorragía. Esto según la cantidad ingresada, y por cada imagen que tenga ese tipo de ICH
                    for i in range(amount):

                        transformed = transform(image=image, bboxes=bboxes, class_labels=hemorrhage_types)
                        transformed_image = transformed['image']
                        transformed_bboxes = transformed['bboxes']

                        try:
                            cv2.imwrite(f'{images}/{id_image}({str(counter_image)}).png', transformed_image)
                        except:
                            raise Exception(f'No se pudo crear la imagen: {id_image}({str(counter_image)}).png')

                        try:
                            file = open(f'{labels}/{id_image}({str(counter_image)}).txt', "w")
                        except OSError as e:
                            raise Exception(f'No se pudo crear el archivo label: '
                                            f'{id_image}({str(counter_image)}).txt\n{e}')

                        bboxes_counter = 0
                        for transformed_box in transformed_bboxes:

                            bbox_string = str(transformed_box).replace('(', "")
                            bbox_string = bbox_string.replace(',', "")
                            bbox_string = bbox_string.replace(')', "")
                            if bboxes_counter > 0:
                                file.writelines(str(int(hemorrhage_types[bboxes_counter])) + " " + bbox_string + os.linesep)
                                bboxes_counter += 1
                            else:
                                file.write(str(int(hemorrhage_types[bboxes_counter])) + " " + bbox_string + os.linesep)
                                bboxes_counter += 1

                        counter_image += 1

                else:
                    print('Este archivo no coincide con el tipo de ICH ingresado.\nContinuamos...')
