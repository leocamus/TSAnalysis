"""Module to print the first n-lines of an specified file"""

import os
import zipfile
import rarfile
#import TransantiagoConstants

# For Jupyter.
from Utils import TransantiagoConstants

fourLevelsUp = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
SSHDir = fourLevelsUp + r'\03_datos\01_SSH'
TRXPPUDir = fourLevelsUp + r'\03_datos\02_TRXPPU'
currentSSHDates = TransantiagoConstants.currentSSHDates

def readAndPrintLines(*args):
	"""args[0]=fileType, args[1]=linesNumber, args[2]=date"""
	try:
		if args[0] == 'TRXPPU':
			print('Warning: complete path should be specified. Information about available dates is currently not maintained')
			TRXPPUPath = input('Enter the path to the specific file: ')
			readAndPrintZip(TRXPPUPath,args[1])
		elif args[0] == 'etapas' and args[2] in currentSSHDates:
			etapasFile = args[2] + '.etapas'
			etapasPath = os.path.join(SSHDir, etapasFile)
			readAndPrint(etapasPath,args[1])
		elif args[0] == 'viajes' and args[2] in currentSSHDates:
			viajesFile = args[2] + '.viajes'
			viajesPath = os.path.join(SSHDir, viajesFile)
			readAndPrint(viajesPath,args[1])
		elif args[0] == 'perfiles' and args[2] in currentSSHDates:
			perfilesFile = args[2] + '.perfiles'
			perfilesPath = os.path.join(SSHDir, perfilesFile) 
			readAndPrint(perfilesPath,args[1])
		else:
			raise ValueError('fileType is not correctly specified')
	except ValueError as fileTypeErr:
		print(fileTypeErr)

def readAndPrint(filePath,linesNumber):
	with open(filePath, "r") as file:
		for x in range(0, int(linesNumber)):
			print(file.readline())
	file.close()

def readAndPrintZip(filePath,linesNumber):
	if filePath[-4:] == '.zip':
		with zipfile.ZipFile(filePath) as myZipFiles:
			files = myZipFiles.infolist()
			with myZipFiles.open(files[0]) as myZipFile:
				for x in range(0, int(linesNumber)):
					print(myZipFile.readline())
			myZipFile.close()
		myZipFiles.close()
	elif filePath[-4:] == '.rar':
		with rarfile.RarFile(filePath) as myRarFiles:
			files = myRarFiles.infolist()
			with myRarFiles.open(files[0]) as myRarFile:
				for x in range(0, int(linesNumber)):
					print(myRarFile.readline())
			myRarFile.close()
		myRarFiles.close()		