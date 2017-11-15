"""Module to run the complete methodology for building histograms, and build it"""
from Utils import SimplifyEtapasUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import os

analyzedDate = input('Enter the date to analyze: ')
analyzedVehicle = input('Enter the vehicle to analyze: ')
SSHDir = TransantiagoConstants.SSHDir
busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir
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

def mergeTurnstileData(df):
	torniquetesFile = 'Avance_Consolidado_v2.xlsx'
	torniquetesDataPath = os.path.join(busesTorniqueteDir, torniquetesFile)
	busesTorniquete_df = pd.read_excel(torniquetesDataPath)
	busesTorniquete_df.columns=['sitio_subida','fecha_instalacion']
	merged_df = pd.merge(df,busesTorniquete_df, on='sitio_subida', how='left')
	checking_missing = pd.isnull(merged_df['fecha_instalacion'])
	print('Not found in turnstile database: ' + str(sum(checking_missing)))#Without turnstiles.
	return merged_df

def cleanDataFrame(df):
	df = df[df.t_subida != '-']
	df = df[df.servicio_subida != '-']
	df = df[df.par_subida != '-']
	df = df[df.sitio_subida != '-']
	return df

def sortDataFrame(df):
	df['t_subida']=pd.to_datetime(df.t_subida)
	sortedDataFrame = df.sort_values(['sitio_subida', 't_subida'], ascending=[True, True])
	return sortedDataFrame
