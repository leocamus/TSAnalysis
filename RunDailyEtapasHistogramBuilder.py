"""Module to run the complete methodology for building histograms, and build it"""
from Utils import SimplifyEtapasUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import os

analyzedDate = input('Enter the date to analyze: ')
analyzedVehicle = input('Enter the vehicle to analyze: ')
SSHDir = HeadersUtils.SSHDir
currentSSHDates = TransantiagoConstants.currentSSHDates

def runSimplifyEtapas():
	"""Not always necessary. To simplify"""
	SimplifyEtapasUtils.writeSimplifiedEtapas(analyzedDate,analyzedVehicle,'id','nviaje','tipo_transporte','t_subida','servicio_subida','par_subida','sitio_subida')

def loadSimplifiedEtapas():
	try:
		if analyzedDate in currentSSHDates:
			simplifiedEtapasFile = analyzedDate + '_simplified.etapas'
			simplifiedEtapasPath = os.path.join(SSHDir, simplifiedEtapasFile)	
		else:
			raise ValueError('date is not correctly specified')
	except ValueError as dateErr:
		print(dateErr)

	etapas_df = pd.read_table(simplifiedEtapasPath, sep='|')
	return etapas_df

def cleanDataFrame(df):
	df = df[df.t_subida != '-']
	df = df[df.servicio_subida != '-']
	df = df[df.par_subida != '-']
	df = df[df.sitio_subida != '-']
	return df

def sortDataFrame(df):
	sortedDataFrame = df.sort_values(['sitio_subida', 't_subida'], ascending=[True, True])
	return sortedDataFrame

#def main():
#	etapas_df = loadSimplifiedEtapas() #no args since analyzedDate and analyzedVehicle are fields.
#	cleanEtapas_df = cleanDataFrame(etapas_df)
#	sortedEtapas_df = sortDataFrame(cleanEtapas_df)

