"""Module to reduce the size of the 'Transantiago' files"""

#import HeadersUtils
#import TransantiagoConstants
import os
import gzip
#For Jupyter.
from Utils import HeadersUtils
from Utils import TransantiagoConstants

SSHDir = HeadersUtils.SSHDir
currentSSHDates = TransantiagoConstants.currentSSHDates

def writeSimplifiedEtapas(date,vehicleType,*argv):
	"""args[0]=date, args[1]=vehicleType, args[2,3,...]=headers to extract"""
	try:
		if date in currentSSHDates:
			workingPerfilesFile = date + '.etapas.gz'
			simplifiedPerfilesFile = date + '_simplified.etapas'
			workingPerfilesPath = os.path.join(SSHDir, workingPerfilesFile)
			simplifiedPerfilesPath = os.path.join(SSHDir,simplifiedPerfilesFile)
		else:
			raise ValueError('date is not correctly specified')
	except ValueError as dateErr:
		print(dateErr)

	with gzip.open(workingPerfilesPath, "rt") as workingPerfiles:
		with open(simplifiedPerfilesPath,"wt") as simplifiedPerfiles:
			firstWorkingLine = workingPerfiles.readline().split('|') #Headers
			simplifiedFirstWorkingLine = simplifyEtapasLine(firstWorkingLine, *argv)
			simplifiedPerfiles.write("%s\n"%simplifiedFirstWorkingLine)
			for workingPerfilesLine in workingPerfiles:
				splittedworkingPerfilesLine = workingPerfilesLine.split('|')
				if splittedworkingPerfilesLine[HeadersUtils.getIndexOfAttribute('etapas','tipo_transporte')]==vehicleType:
					simplifiedPerfilesString = simplifyEtapasLine(splittedworkingPerfilesLine, *argv)
					simplifiedPerfiles.write("%s\n"%simplifiedPerfilesString)
		simplifiedPerfiles.close()
	workingPerfiles.close()

def writeSimplifiedPerfiles(date,ZP,*argv):
	"""args[0]=date, args[1]=ZP, args[2,3,...]=headers to extract"""
	try:
		if date in currentSSHDates:
			workingPerfilesFile = date + '.perfiles.gz'
			simplifiedPerfilesFile = date + '_simplified.perfiles'
			workingPerfilesPath = os.path.join(SSHDir, workingPerfilesFile)
			simplifiedPerfilesPath = os.path.join(SSHDir,simplifiedPerfilesFile)
		else:
			raise ValueError('date is not correctly specified')
	except ValueError as dateErr:
		print(dateErr)

	with gzip.open(workingPerfilesPath, "rt") as workingPerfiles:
		with open(simplifiedPerfilesPath,"wt") as simplifiedPerfiles:
			firstWorkingLine = workingPerfiles.readline().split('|') #Headers
			simplifiedFirstWorkingLine = simplifyPerfilesLine(firstWorkingLine, *argv)
			simplifiedPerfiles.write("%s\n"%simplifiedFirstWorkingLine)
			for workingPerfilesLine in workingPerfiles:
				splittedworkingPerfilesLine = workingPerfilesLine.split('|')
				if splittedworkingPerfilesLine[HeadersUtils.getIndexOfAttribute('perfiles','ZP')]==ZP:
					simplifiedPerfilesString = simplifyPerfilesLine(splittedworkingPerfilesLine, *argv)
					simplifiedPerfiles.write("%s\n"%simplifiedPerfilesString)
		simplifiedPerfiles.close()
	workingPerfiles.close()


def simplifyEtapasLine(line, *argv):
	"""args[0]=currentLine, args[1,2,...]=headers to extract"""
	simplifiedLine = []
	for attribute in argv:
		indexOfAttribute = HeadersUtils.getIndexOfAttribute('etapas',attribute)
		attributeToInclude = line[indexOfAttribute]
		simplifiedLine.append(attributeToInclude)

	simplifiedPerfilesString = "|".join(simplifiedLine)
	return simplifiedPerfilesString

def simplifyPerfilesLine(line, *argv):
	"""args[0]=currentLine, args[1,2,...]=headers to extract"""
	simplifiedLine = []
	for attribute in argv:
		indexOfAttribute = HeadersUtils.getIndexOfAttribute('perfiles',attribute)
		attributeToInclude = line[indexOfAttribute]
		simplifiedLine.append(attributeToInclude)

	simplifiedPerfilesString = "|".join(simplifiedLine)
	return simplifiedPerfilesString