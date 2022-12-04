import os
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    bounding_boxes = '../Bounding_Boxes'

    Intraparenchymal_counter = 0
    Subarachnoid_counter = 0
    Intraventricular_counter = 0
    Epidural_counter = 0
    Subdural_counter = 0
    Chronic_counter = 0

    for nombre_directorio, dirs, ficheros in os.walk(bounding_boxes, topdown=True):
        for nombre_fichero in ficheros:

            label = f'{bounding_boxes}/{nombre_fichero}'

            try:
                file = open(label, 'r')
            except OSError as e:
                print(f'El Archivo {label} no esxiste...')
                raise Exception(e)

            for line in file:

                ICH = line[0]

                if ICH == '0':
                    Intraparenchymal_counter += 1
                elif ICH == '1':
                    Subarachnoid_counter += 1
                elif ICH == '2':
                    Intraventricular_counter += 1
                elif ICH == '3':
                    Epidural_counter += 1
                elif ICH == '4':
                    Subdural_counter += 1
                elif ICH == '5':
                    Chronic_counter += 1

    print(f'\nCONTADORES POR TIPO DE ICH\n\n'
          f'Intraparenchymal: {Intraparenchymal_counter}\n'
          f'Subarachnoi: {Subarachnoid_counter}\n' 
          f'Intraventricular: {Intraventricular_counter}\n'
          f'Epidural: {Epidural_counter}\n'
          f'Subdural: {Subdural_counter}\n'
          f'Chronic: {Chronic_counter}\n')

    df = pd.DataFrame()
    df['ICH'] = None
    df['Cantidad'] = None

    ICH_arr = ['Intraparenchymal', 'Subarachnoi',
               'Intraventricular', 'Epidural',
               'Subdural', 'Chronic']

    cantidades_arr = [Intraparenchymal_counter, Subarachnoid_counter,
                      Intraventricular_counter, Epidural_counter,
                      Subdural_counter, Chronic_counter]

    df['ICH'] = ICH_arr
    df['Cantidad'] = cantidades_arr

    df.plot(kind='bar')
