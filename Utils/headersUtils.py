"""Module to handling Transantiago-data headers"""

import os
import zipfile
import rarfile
import gzip
#import TransantiagoConstants

#For Jupyter.
from Utils import TransantiagoConstants

defaultEtapasHeaders = TransantiagoConstants.defaultEtapasHeaders
defaultViajesHeaders = TransantiagoConstants.defaultViajesHeaders
defaultPerfilesHeaders = TransantiagoConstants.defaultPerfilesHeaders
defaultTRXPPUHeaders = TransantiagoConstants.defaultTRXPPUHeaders

currentSSHDates = TransantiagoConstants.currentSSHDates
SSHDir = TransantiagoConstants.SSHDir

def getHeaders(*args):
	"""args[0]=fileType, args[1]=date"""
	try:
		if len(args) == 1:
			if args[0] == 'etapas':
				return defaultEtapasHeaders
			elif args[0] == 'viajes':
				return defaultViajesHeaders
			elif args[0] == 'perfiles':
				return defaultPerfilesHeaders
			elif args[0] == 'TRXPPU':
				return defaultTRXPPUHeaders
			else:
				print('Wrong fileType')
		elif len(args) == 2:
			try:
				if args[0] == 'TRXPPU':
					print('Warning: complete path should be specified. Information about available dates is currently not maintained')
					TRXPPUPath = input('Enter the path to the specific file: ')
					readAndPrintZipHeader(TRXPPUPath)
				elif args[0] == 'etapas' and args[1] in currentSSHDates:
					etapasFile = args[1] + '.etapas.gz'
					etapasPath = os.path.join(SSHDir, etapasFile)
					readAndPrintZipHeader(etapasPath)
				elif args[0] == 'viajes' and args[1] in currentSSHDates:
					viajesFile = args[1] + '.viajes.gz'
					viajesPath = os.path.join(SSHDir, viajesFile)
					readAndPrintZipHeader(viajesPath)
				elif args[0] == 'perfiles' and args[1] in currentSSHDates:
					perfilesFile = args[1] + '.perfiles.gz'
					perfilesPath = os.path.join(SSHDir, perfilesFile) 
					readAndPrintZipHeader(perfilesPath)
				else:
					raise ValueError('Wrong SSH date')
			except ValueError as dateErr:
				print (dateErr.args)
		else:
			raise ValueError('Wrong number of arguments')
	except ValueError as argsErr:
		print(argsErr.args)

def getCurrentSSHDates():
	return currentSSHDates

def readAndPrintHeader(filePath):
	with open(filePath, "r") as file:
		first_line = file.readline()
		print(first_line)
	file.close()

def readAndPrintZipHeader(filePath):
	if filePath[-4:] == '.zip':	
		with zipfile.ZipFile(filePath) as myZipFiles:
			files = myZipFiles.infolist()
			with myZipFiles.open(files[0],'rt') as myZipFile:
				first_line = myZipFile.readline()
				print(first_line)
			myZipFile.close()
		myZipFiles.close()
	elif filePath[-4:] == '.rar':
		with rarfile.RarFile(filePath) as myRarFiles:
			files = myRarFiles.infolist()
			with myRarFiles.open(files[0],'rt') as myRarFile:		
				first_line = myRarFile.readline()
				print(first_line)
			myRarFile.close()
		myRarFiles.close()
	elif filePath[-3:] == '.gz':
		with gzip.open(filePath,'rt') as myGzipFile:
			first_line = myGzipFile.readline()
			print(first_line)
		myGzipFile.close()
	

def getIndexOfAttribute(fileType,headerName):
	"""Only referenced to defaultHeaders. TODO: Should be updated when read a new file"""
	try:
		if fileType == 'etapas':
			for i,x in enumerate(defaultEtapasHeaders):
				if x == headerName:
					return i
		elif fileType == 'viajes':
			for i,x in enumerate(defaultViajesHeaders):
				if x == headerName:
					return i
		elif fileType == 'perfiles':
			for i,x in enumerate(defaultPerfilesHeaders):
				if x == headerName:
					return i
		elif fileType == 'TRXPPU':
			for i,x in enumerate(defaultTRXPPUHeaders):
				if x == headerName:
					return i
		else:
			raise ValueError('Wrong fileType or headerName')
	except ValueError as err:
		print(err.args)
		