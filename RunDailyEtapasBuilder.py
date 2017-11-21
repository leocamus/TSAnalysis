"""Module to run the complete methodology for building histograms, and build it"""
from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import numpy as np
import os
import datetime as dt

analyzedDate = input('Enter the date to analyze: ')
analyzedVehicle = input('Enter the vehicle to analyze: ')
if_ZP = input('Consider ZP in perfiles file (0/1)?: ')

SSHDir = TransantiagoConstants.SSHDir
busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir
currentSSHDates = TransantiagoConstants.currentSSHDates

def runSimplifyEtapas():
	"""Not always necessary. Reducing the complexity of the original etapas-file"""
	SimplifyFilesUtils.writeSimplifiedEtapas(analyzedDate,analyzedVehicle,'id','nviaje','tipo_transporte','t_subida','servicio_subida','par_subida','sitio_subida')

def runSimplifyPerfiles():
	"""Not always necessary. Reducing the complexity of the original etapas-file"""
	SimplifyFilesUtils.writeSimplifiedPerfiles(analyzedDate,if_ZP,'ServicioSentido','Patente','Paradero','Hini','Hfin','idExpedicion','DistEnRuta')

def loadSimplifiedEtapas():
	"""Returns the simplified etapas-file as pandas df"""
	try:
		if analyzedDate in currentSSHDates:
			simplifiedEtapasFile = analyzedDate + '_simplified.etapas'
			simplifiedEtapasPath = os.path.join(SSHDir, simplifiedEtapasFile)	
		else:
			raise ValueError('date is not correctly specified')
	except ValueError as dateErr:
		print(dateErr)

	etapas_df = pd.read_table(simplifiedEtapasPath, sep='|', encoding='latin-1')
	return etapas_df

def loadSimplifiedPerfiles():
	"""Returns the simplified perfiles-file as pandas df"""
	try:
		if analyzedDate in currentSSHDates:
			simplifiedPerfilesFile = analyzedDate + '_simplified.perfiles'
			simplifiedPerfilesPath = os.path.join(SSHDir, simplifiedPerfilesFile)	
		else:
			raise ValueError('date is not correctly specified')
	except ValueError as dateErr:
		print(dateErr)

	perfiles_df = pd.read_table(simplifiedPerfilesPath, sep='|', encoding='latin-1')
	return perfiles_df

#def mergeIdExpedicion(etapas_df):
#	"""Merges the loaded etapas-file with the perfiles-file.idExpedicion into a pandas df and returns it. Consider printing to a file"""
#	#Begin not-so-ugly coding
#	perfiles_df = loadSimplifiedPerfiles()
#	etapas_df['t_subida'] = pd.to_datetime(etapas_df.t_subida)
#	perfiles_df['Hini'] = pd.to_datetime(perfiles_df.Hini)
#	perfiles_df['Hfin'] = pd.to_datetime(perfiles_df.Hfin)
#	for etapas_index, etapas_row in etapas_df.iterrows():
#		for perfiles_index, perfiles_row in perfiles_df.iterrows():
#			if ((etapas_row['servicio_subida']==perfiles_row['ServicioSentido']) &
#				(etapas_row['sitio_subida']==perfiles_row['Patente']) &
#				(etapas_row['par_subida']==perfiles_row['Paradero']) &
#				(perfiles_row['Hini']<=etapas_row['t_subida']<=perfiles_row['Hfin'])):
#				etapas_row['id_expedicion']=perfiles_row['idExpedicion']
#				break
#	#End not-so-ugly coding
#	return etapas_df

def mergeTurnstileData(df):
	"""Merges the loaded etapas-file with the turnstile-file.fecha_instalacion into a pandas df and returns it"""
	torniquetesFile = 'Avance_Consolidado_v2.xlsx'
	torniquetesDataPath = os.path.join(busesTorniqueteDir, torniquetesFile)
	busesTorniquete_df = pd.read_excel(torniquetesDataPath)
	busesTorniquete_df.columns=['sitio_subida','fecha_instalacion']
	merged_turnstiles_df = pd.merge(df,busesTorniquete_df, on='sitio_subida', how='left')
	checking_missing = pd.isnull(merged_turnstiles_df['fecha_instalacion'])
	print('Not found in turnstile database: ' + str(sum(checking_missing))) #Without turnstiles, then NaT.
	merged_turnstiles_df['fecha_instalacion'] = pd.to_datetime(merged_turnstiles_df.fecha_instalacion)
	return merged_turnstiles_df

def cleanDataFrame(df):
	"""Returns a clean pandas dataframe without '-' values"""	
	df = df[df.t_subida != '-']
	df = df[df.servicio_subida != '-']
	df = df[df.par_subida != '-']
	df = df[df.sitio_subida != '-']
	return df

def sortDataFrame(df):
	"""Sorts the final dataframe by sitio_subida and then by t_subida"""		
	df['t_subida']=pd.to_datetime(df.t_subida)
	sortedDataFrame = df.sort_values(by=['sitio_subida', 't_subida'], ascending=[True, True])
	return sortedDataFrame
