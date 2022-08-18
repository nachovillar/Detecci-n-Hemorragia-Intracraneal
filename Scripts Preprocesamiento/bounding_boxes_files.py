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


#-------------------------------------- CSVs -------------------------------------------------------------------------
Initial_Manual_Labeling = '../1_Initial_Manual_Labeling.csv'
Extrapolation_to_All_Series = '../2_Extrapolation_to_All_Series.csv'
Extrapolation_to_Selected_Series = '../3_Extrapolation_to_Selected_Series.csv'

data_Initial_Manual_Labeling = pd.read_csv(Initial_Manual_Labeling)
data_Extrapolation_to_All_Series = pd.read_csv(Extrapolation_to_All_Series)
data_Extrapolation_to_Selected_Series = pd.read_csv(Extrapolation_to_Selected_Series)

columns_of_interest = data_Extrapolation_to_Selected_Series.drop(['SeriesInstanceUID', 'StudyInstanceUID', 'labelType'], axis=1)
columns_of_interest = columns_of_interest.drop(columns_of_interest.columns[[0]], axis='columns')
#---------------------------------------------------------------------------------------------------------------------

data = '../Data/BHX'

characters = ['"', "'", "{", "x", ":", ",", "y", "w", "i", "d", "t", "h", "e", "g", "}"]

for index, columns  in columns_of_interest.iterrows():
    #columns[0] = SOPInstanceUID
    #columns[1] = Bounding Box
    #columns[2] = Hemorrhage Type    
    bounding_box = columns[1]
    for x in range(len(characters)):
        
        bounding_box = bounding_box.replace(characters[x],"")
        bounding_box = bounding_box.replace("  ", " ")
        bb = bounding_box[1:]
    columns_of_interest['data'][index] = bb
    
    
counter = 0  
for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
    for nombre_fichero in ficheros:
        im = pydicom.data.data_manager.get_files(nombre_directorio, nombre_fichero)[0]
        ds = pydicom.dcmread(im, force=True)
        
        SOPInstanceUID = ds.data_element('SOPInstanceUID').value
        PatientID = ds.data_element('PatientID').value
        SeriesNumber = ds.data_element('SeriesNumber').value
        InstanceNumber = ds.data_element('InstanceNumber').value
        
        counter += 1
        print(counter)
        for index, columns  in columns_of_interest.iterrows():

            ID_DICOM = columns[0]
            bbx = columns[1]
            Hemorrhage = columns[2]
            
            bbox = np.array(bbx.split())
            
            x = float(bbox[0])
            y = float(bbox[1])
            w = float(bbox[2])
            h = float(bbox[3])
            
            x_center = x + w / 2
            y_center = y + w / 2
            
            x_center /= 512
            y_center /= 512
            w /= 512
            h /= 512
            
            if str(SOPInstanceUID) == str(ID_DICOM):
                
                    fileName =  str(nombre_directorio) + "/" + str(PatientID) + "-" + str(SeriesNumber) + "-" + str(InstanceNumber) + ".txt"
                    
                    if os.path.isfile(fileName):
                        
                        file = open(fileName, "a")
                                                          
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
                
        
                    else:
                    
                        file = open(fileName, "w")
                        
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
        print(nombre_fichero)





        


