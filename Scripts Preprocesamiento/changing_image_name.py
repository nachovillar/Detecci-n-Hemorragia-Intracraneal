# -*- coding: utf-8 -*-
"""
Created on Mon May 16 19:19:59 2022

@author: Villar
"""

#CQ500-CT-0-3-80
#img-00002-00017
import os
import re

def if_integer(string):

    reg_exp = "[-+]?\d+$"
    return re.match(reg_exp, string) is not None

data = '../../data_training'
characters = ["S", "\\", "i", "m", "g"]

for nombre_directorio, dirs, ficheros in os.walk(data, topdown=True):
    for nombre_fichero in ficheros:
        
        fileName = str(nombre_directorio) + str(nombre_fichero)
        newFileName = fileName[28:40] + "-" + nombre_fichero
       
        
        for x in range(len(characters)):
            
            newFileName = newFileName.replace(characters[x],"")
            
            
        if if_integer(newFileName[9:12]):
            
            #newFileName = newFileName.replace(newFileName[14:19], str(int(newFileName[14:19])))
            #newFileName[14:19] = str(int(newFileName[14:19]))
            
            serie = str(int(newFileName[14:19]))
            newFileName = newFileName[0:14] + serie + newFileName[19:]
              
            if len(newFileName) == 24:
                
                newFileName = newFileName.replace(newFileName[16:21], str(int(newFileName[16:21])))
                
                
            elif len(newFileName) == 25:
                
                newFileName = newFileName.replace(newFileName[17:22], str(int(newFileName[17:22])))
             
            elif len(newFileName) == 26:
                newFileName = newFileName.replace(newFileName[18:23], str(int(newFileName[18:23])))
            
            newFileName = newFileName[0:12] + newFileName[13:] + "g"
            
            print(newFileName)
        
            file_oldname = os.path.join(nombre_directorio, nombre_fichero)
            file_newname = os.path.join(nombre_directorio, newFileName)
            
            os.rename(file_oldname, file_newname)
        
        elif if_integer(newFileName[9:11]):
            
            #newFileName = newFileName.replace(newFileName[13:18], str(int(newFileName[13:18])))
            #[13:18] = str(int(newFileName[13:18]))
            
            serie = str(int(newFileName[13:18]))
            newFileName = newFileName[0:13] + serie + newFileName[18:]
            
            if len(newFileName) == 23:
                
                newFileName = newFileName.replace(newFileName[15:20], str(int(newFileName[15:20])))
                
                
            elif len(newFileName) == 24:
                
                newFileName = newFileName.replace(newFileName[16:21], str(int(newFileName[16:21])))
             
            elif len(newFileName) == 25:
                newFileName = newFileName.replace(newFileName[17:22], str(int(newFileName[17:22])))
                
            newFileName = newFileName[0:11] + newFileName[12:] + "g"
            
            print(newFileName)
        
            file_oldname = os.path.join(nombre_directorio, nombre_fichero)
            file_newname = os.path.join(nombre_directorio, newFileName)
            
            os.rename(file_oldname, file_newname)
        
            
        else:
        
            #newFileName = newFileName.replace(newFileName[12:17], str(int(newFileName[12:17])))
            serie = str(int(newFileName[12:17]))
            newFileName = newFileName[0:12] + serie + newFileName[17:]
            #newFileName[12:17] = str(int(newFileName[12:17]))
            
            if len(newFileName) == 22:
                
                newFileName = newFileName.replace(newFileName[14:19], str(int(newFileName[14:19])))
                
                
            elif len(newFileName) == 23:
                
                newFileName = newFileName.replace(newFileName[15:20], str(int(newFileName[15:20])))
             
            elif len(newFileName) == 24:
                newFileName = newFileName.replace(newFileName[16:21], str(int(newFileName[16:21])))
            
            newFileName = newFileName[0:10] + newFileName[11:] + "g"
            
            print(newFileName)
        
            file_oldname = os.path.join(nombre_directorio, nombre_fichero)
            file_newname = os.path.join(nombre_directorio, newFileName)
            
            os.rename(file_oldname, file_newname)
        


