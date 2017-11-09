"""Module to print the first n-lines of an specified file"""

import os
from Utils import TransantiagoConstants

fourLevelsUp = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
SSHDir = fourLevelsUp + r'\03_datos\01_SSH'
TRXPPUDir = fourLevelsUp + r'\03_datos\02_TRXPPU'
currentSSHDates = TransantiagoConstants.currentSSHDates

def readAndPrintLines(fileType,date,linesNumber):
	"""args[0]=fileType, args[1]=date, args[2]=linesNumber"""	
	if args[1] in currentSSHDates:
		if fileType == 'etapas' or fileType == 'viajes' or fileType == 'perfiles':
			if args[0] == 'etapas':
				etapasFile = args[1] + '.etapas'
				etapasPath = os.path.join(SSHDir, etapasFile)
				readAndPrint(etapasPath,linesNumber)
			elif args[0] == 'viajes':
				viajesFile = args[1] + '.viajes'
				viajesPath = os.path.join(SSHDir, viajesFile)
				readAndPrint(viajesPath,linesNumber)
			elif args[0] == 'perfiles':
				perfilesFile = args[1] + '.perfiles'
				perfilesPath = os.path.join(SSHDir, perfilesFile) 
				readAndPrint(perfilesPath,linesNumber)
		elif fileType == 'TRXPPU':
			print('Warning: complete path should be specified. Information about available dates is currently not maintained')
			TRXPPUPath = input('Enter the path to the specific file: ')
			readAndPrint(perfilesPath,linesNumber)
		else:
			print('fileType is not correctly specified')
	else:
		print('Date is not correctly specified')

def readAndPrint(filePath,linesNumber):
	with open(filePath, "r") as file:
		for x in range(0, linesNumber):
			print(file.readline().split('|'))
	file.close()
