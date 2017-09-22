import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import headers

# Este será el script principal, que utilizará a los demás módulos/clases(?) en su ejecución. Mi idea
# es que este script reciba inputs del usuario directamente. Específicamente, el script debe recibir
# la fecha que se desea analizar en formato dd/mm/aa, el tipo de archivo a analizar (etapa/viaje/perfil)
# el tipo de vehículo (bus/zp/metro) y los atributos a extraer, con tal de bajar el número de atributos
# y registros en los archivos originales. El script debe escribir en una carpeta especialmente creada
# para esto. Si es necesario, este script debe crear el directorio output.

# TODO: Ir actualizando las fechas disponibles.
# TODO: Ir mejorando el sistema de recibimiento de información por parte del usuario. 

levelsUp = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
analysisDir = levelsUp + r'\03_datos'
SSHDir = analysisDir + r'\01_SSH'

# Tarea 1.0: Que el script reciba, en el modo "interactivo", la fecha que se desea analizar.
# TODO: Que el script reciba como arg la fecha que se desea analizar.

downloadedDates = {'01/03/17'}
userDate = input("Introducir fecha a analizar en formato dd/mm/aa: ")
if userDate in downloadedDates:
    dateChosen = userDate
else:
    print("No se encuentra esta fecha")
    raise ValueError("La fecha especificada es incorrecta. Abortando ...")

# Tarea 2.0: Que el script reciba, en el modo "interactivo", el tipo de archivo que desea analizar.
# TODO: Que el script reciba como arg la fecha que se desea analizar.

fileTypes = {'etapas', 'viajes', 'perfiles'}
userType = input("Introducir tipo de archivo a analizar (etapas/viajes/perfiles): ")
if userType in fileTypes:
    typeChosen = userType
else:
    print("No se encuentra este tipo de archivo")
    raise ValueError("El tipo de archivo especificado es incorrecto. Abortando ...")

# Tarea 3.0: Que el script reciba, en el modo "interactivo", el tipo de vehículo a analizar.
# TODO: Que el script reciba como arg la fecha que se desea analizar.

vehicleTypes = {'BUS', 'ZP', 'METRO'}
userVehicle = input("Introducir tipo de vehiculo a analizar (BUS/ZP/METRO): ")
if userVehicle in vehicleTypes:
    vehicleChosen = userVehicle
else:
    print("No se encuentra este tipo de vehículo")
    raise ValueError("El tipo de vehículo especificado es incorrecto. Abortando ...")

# Tarea 4.0: Que el script reciba, en el modo "interactivo", los atributos requeridos.
# TODO: Que el script reciba como arg los atributos requeridos.
attributes = input("Introducir los atributos que deseas que se mantengan en el archivo final (separados por comas): ")
attributesList = attributes.split(",")

# Verificando si los atributos se encuentran en los archivos respectivos ... 
#if typeChosen == "etapas":
#    etapasHeaders = headers.getHeaders('etapas')
#    if 




#etapasPath = str(analysisDir) + r"\SSH\03_datos\2017-03-01.etapas"
#outPath = str(analysisDir) + r"\SSH\03_datos\01_histogramDDBB\1_03_2017E.txt"

#with open(etapasPath, "r") as etapasFile:
#    outFile = open(outPath,'w') 
#    for line in etapasFile:
#        lineList=line.split("|")
#        if(lineList[4]=="BUS"):
#            outFile.write(lineList[0]+"|"+lineList[8]+"|"+lineList[19]+"|"+lineList[21]+"|"+lineList[27]+"\n")
#    outFile.close()
























#    for line in etapasFile:
#        boardingDateAndTime = line.split("|")[8]
#        boardingTime = boardingDateAndTime.split(" ")[1]
#        boardingTimeList = boardingTime.split(":")
#        boardingHour = boardingTimeList[0]
#        boardingMinute = boardingTimeList[1]
#        boardingSecond = boardingTimeList[2]
#        boardingTimeInSeconds = int(boardingHour)*60*60+int(boardingMinute)*60+int(boardingSecond)
#        print(boardingTimeInSeconds)
