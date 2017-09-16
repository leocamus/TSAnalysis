from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

analysisDir = Path(__file__).parents[3]

etapasPath = str(analysisDir) + r"\03_datos\2017-03-01.etapas"
outPath = str(analysisDir) + r"\03_datos\01_histogramDDBB\1_03_2017E.txt"

with open(etapasPath, "r") as etapasFile:
    outFile = open(outPath,'w') 
    for line in etapasFile:
        lineList=line.split("|")
        if(lineList[4]=="BUS"):
            outFile.write(lineList[0]+"|"+lineList[8]+"|"+lineList[19]+"|"+lineList[21]+"|"+lineList[27]+"\n")
    outFile.close()
























#    for line in etapasFile:
#        boardingDateAndTime = line.split("|")[8]
#        boardingTime = boardingDateAndTime.split(" ")[1]
#        boardingTimeList = boardingTime.split(":")
#        boardingHour = boardingTimeList[0]
#        boardingMinute = boardingTimeList[1]
#        boardingSecond = boardingTimeList[2]
#        boardingTimeInSeconds = int(boardingHour)*60*60+int(boardingMinute)*60+int(boardingSecond)
#        print(boardingTimeInSeconds)
