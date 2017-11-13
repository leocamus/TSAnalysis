"""Module to reduce the size of the 'Transantiago' files"""

#import HeadersUtils
#import TransantiagoConstants
import os

#For Jupyter.
from Utils import HeadersUtils
from Utils import TransantiagoConstants

SSHDir = HeadersUtils.SSHDir
currentSSHDates = TransantiagoConstants.currentSSHDates

def writeSimplifiedEtapas(date,vehicleType,*argv):
	"""args[0]=date, args[1]=vehicleType, args[2,3,...]=headers to extract"""
	try:
		if date in currentSSHDates:
			workingEtapaFile = date + '.etapas'
			simplifiedEtapaFile = date + '_simplifiedEtapas.txt'
			workingEtapaPath = os.path.join(SSHDir, workingEtapaFile)
			simplifiedEtapaPath = os.path.join(SSHDir,simplifiedEtapaFile)
		else:
			raise ValueError('date is not correctly specified')
	except ValueError as dateErr:
		print(dateErr)

	with open(workingEtapaPath, "r") as workingEtapa:
		with open(simplifiedEtapaPath,"w") as simplifiedEtapa:
			firstWorkingLine = workingEtapa.readline().split('|') #Headers
			simplifiedFirstWorkingLine = simplifyLine(firstWorkingLine, *argv)
			simplifiedEtapa.write("%s\n"%simplifiedFirstWorkingLine)
			for workingEtapaLine in workingEtapa:
				splittedWorkingEtapaLine = workingEtapaLine.split('|')
				if splittedWorkingEtapaLine[HeadersUtils.getIndexOfAttribute('etapas','tipo_transporte')]==vehicleType:
					simplifiedEtapaString = simplifyLine(splittedWorkingEtapaLine, *argv)
					simplifiedEtapa.write("%s\n"%simplifiedEtapaString)
		simplifiedEtapa.close()
	workingEtapa.close()

def simplifyLine(line, *argv):
	"""args[0]=currentLine, args[1,2,...]=headers to extract"""
	simplifiedLine = []
	for attribute in argv:
		indexOfAttribute = HeadersUtils.getIndexOfAttribute('etapas',attribute)
		attributeToInclude = line[indexOfAttribute]
		simplifiedLine.append(attributeToInclude)

	simplifiedEtapaString = "|".join(simplifiedLine)
	return simplifiedEtapaString
