"""Module to write the first n-lines of etapas to a new file"""

#import HeadersUtils
#import TransantiagoConstants
import os

#For Jupyter.
from Utils import HeadersUtils
from Utils import TransantiagoConstants

#NEW
SSHDir = HeadersUtils.SSHDir
currentSSHDates = TransantiagoConstants.currentSSHDates

def writeTesterEtapa(fileType,date, numberOfLines):
	"""args[0]=fileType, args[1]=date, args[2]=numberOfLines"""
	try:
		if fileType == 'etapas' and date in currentSSHDates:
			workingEtapaFile = date + '.etapas'
			simplifiedEtapaFile = date + '_tester.etapas'
			workingEtapaPath = os.path.join(SSHDir, workingEtapaFile)
			simplifiedEtapaPath = os.path.join(SSHDir,simplifiedEtapaFile)
		else:
			raise ValueError('fileType or date is not correctly specified')
	except ValueError as fileTypeErr:
		print(fileTypeErr)

	with open(workingEtapaPath, "r") as workingEtapa:
		with open(simplifiedEtapaPath,"w") as simplifiedEtapa:
			for x in range(0, int(numberOfLines)):
				simplifiedEtapa.write(workingEtapa.readline())
		simplifiedEtapa.close()
	workingEtapa.close()
