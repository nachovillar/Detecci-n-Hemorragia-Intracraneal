import shutil
import os
import random
import mmcv

if __name__ == '__main__':
    bounding_boxes = '../Bounding_Boxes'
    images = '../train_data'

    images_train = '../train_data/images/train'
    images_val = '../train_data/images/val'

    bbx_train = '../train_data/labels/train'
    bbx_val = '../train_data/labels/val'

    mmcv.mkdir_or_exist(images_train)
    mmcv.mkdir_or_exist(images_val)
    mmcv.mkdir_or_exist(bbx_train)
    mmcv.mkdir_or_exist(bbx_val)

    list = []
    for nombre_directorio, dirs, ficheros in os.walk(images, topdown=True):
        for nombre_fichero in ficheros:

            nombre_archivo = nombre_fichero[0:-4]
            list.append(nombre_archivo)

    train_percent = int(0.8 * len(list))
    train_set = random.sample(list, train_percent)
    val_set = set(list) - set(train_set)

    for nombre_directorio_2, dirs_2, ficheros_2 in os.walk(images, topdown=True):
        for nombre_fichero_2 in ficheros_2:

            filename = nombre_fichero_2[0:-4]
            print(filename)

            if filename in train_set:
                print(f'Moviendo archivos de ENTRENAMIENTO con ID: {filename}')
                try:
                    shutil.move(f'{nombre_directorio_2}\\{filename}.png', images_train)
                except:
                    raise Exception(f'No se pudo mover el archivo {filename}.png al directorio {images_train}')

                try:
                    shutil.move(f'{bounding_boxes}\\{filename}.txt', bbx_train)
                except:
                    raise Exception(f'No se pudo mover el archivo {filename}.txt al directorio {bbx_train}')

            elif filename in val_set:
                print(f'Moviendo archivos de VALIDACIÓN con ID: {filename}')
                try:
                    shutil.move(f'{nombre_directorio_2}\\{filename}.png', images_val)
                except:
                    raise Exception(f'No se pudo mover el archivo {filename}.png al directorio {images_val}')

                try:
                    shutil.move(f'{bounding_boxes}\\{filename}.txt', bbx_val)
                except:
                    raise Exception(f'No se pudo mover el archivo {filename}.png al directorio {bbx_train}')
