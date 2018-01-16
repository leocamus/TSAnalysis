"""Module to run the complete methodology for building histograms, and build it silently"""
from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import numpy as np
import os
import datetime as dt

class RunSilentlyDailyEtapasBuilderClass:

	SSHDir = TransantiagoConstants.SSHDir
	busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir
	currentSSHDates = TransantiagoConstants.updateCurrentSSHDates()

	def __init__(self,date,vehicle='BUS',zp='0'):
		self.analyzedDate = date
		self.analyzedVehicle = vehicle
		self.if_ZP = zp
		self.etapas_df = pd.DataFrame()

	def runSimplifyEtapas(self):
		"""Not always necessary. Reducing the complexity of the original etapas-file. Attributes to extract are hardcoded"""
		SimplifyFilesUtils.writeSimplifiedEtapas(self.analyzedDate,self.analyzedVehicle,'id','nviaje','tipo_transporte','t_subida','servicio_subida','par_subida','sitio_subida')
#		SimplifyFilesUtils.writeSimplifiedEtapas(self.analyzedDate,self.analyzedVehicle,'id','nviaje','tipo_transporte','t_subida','media_hora_subida','servicio_subida','par_subida','sitio_subida')

	def loadSimplifiedEtapas(self):
		"""Returns the simplified etapas-file as pandas df"""
		try:
			if self.analyzedDate in RunSilentlyDailyEtapasBuilderClass.currentSSHDates:
				simplifiedEtapasFile = self.analyzedDate + '_simplified.etapas'
				simplifiedEtapasPath = os.path.join(RunSilentlyDailyEtapasBuilderClass.SSHDir, simplifiedEtapasFile)	
			else:
				raise ValueError('date is not correctly specified')
		except ValueError as dateErr:
			print(dateErr)

		self.etapas_df = pd.read_table(simplifiedEtapasPath, sep='|', encoding='latin-1')

	def mergeTurnstileData(self):
		"""Merges the loaded etapas-file with the turnstile-file.fecha_instalacion into a pandas df and returns it"""
		torniquetesFile = 'Avance_Consolidado_v2.xlsx'
		torniquetesDataPath = os.path.join(RunSilentlyDailyEtapasBuilderClass.busesTorniqueteDir, torniquetesFile)
		busesTorniquete_df = pd.read_excel(torniquetesDataPath)
		busesTorniquete_df.columns=['sitio_subida','fecha_instalacion']
		self.etapas_df = pd.merge(self.etapas_df,busesTorniquete_df, on='sitio_subida', how='left')
		checking_missing = pd.isnull(self.etapas_df['fecha_instalacion'])
		print('Not found in turnstile database: ' + str(sum(checking_missing))) #Without turnstiles, then NaT.
		self.etapas_df.loc[:,'fecha_instalacion'] = pd.to_datetime(self.etapas_df.loc[:,'fecha_instalacion'])

	def cleanDataFrame(self):
		"""Returns a clean pandas dataframe without '-' values"""	
		self.etapas_df = self.etapas_df[self.etapas_df['t_subida'] != '-']
		self.etapas_df = self.etapas_df[self.etapas_df['servicio_subida'] != '-']
		self.etapas_df = self.etapas_df[self.etapas_df['par_subida'] != '-']
		self.etapas_df = self.etapas_df[self.etapas_df['sitio_subida'] != '-']

	def sortDataFrame(self):
		"""Sorts the final dataframe by sitio_subida and then by t_subida"""		
		self.etapas_df.loc[:,'t_subida']=pd.to_datetime(self.etapas_df.loc[:,'t_subida'])
		self.etapas_df = self.etapas_df.sort_values(by=['sitio_subida', 't_subida'], ascending=[True, True])
		self.etapas_df = self.etapas_df.reset_index(drop=True)

	def postProcessingSortedDataFrame(self):
		self.etapas_df['mismo_paradero'] = (self.etapas_df['par_subida']==self.etapas_df['par_subida'].shift()).fillna(False)
		self.etapas_df['misma_patente'] = (self.etapas_df['sitio_subida']==self.etapas_df['sitio_subida'].shift()).fillna(False)
		self.etapas_df['mismo_servicio'] = (self.etapas_df['servicio_subida']==self.etapas_df['servicio_subida'].shift()).fillna(False)
		self.etapas_df.loc[(self.etapas_df['mismo_servicio'] == True) & (self.etapas_df['mismo_paradero'] == True) & (self.etapas_df['misma_patente'] == True), 'diferencia_tiempo'] = (self.etapas_df['t_subida']-self.etapas_df['t_subida'].shift())
		self.etapas_df['diferencia_tiempo_secs'] = self.etapas_df['diferencia_tiempo'].dt.total_seconds()
		self.etapas_df['si_torniquete'] = (self.etapas_df['fecha_instalacion']<=self.etapas_df['t_subida'])
		self.etapas_df['si_2017_torniquete'] = ((self.etapas_df['fecha_instalacion']<=self.etapas_df['t_subida'])&(self.etapas_df['fecha_instalacion']>=pd.to_datetime('2017-01-01')))

	def filteringDf(self):
		"""Returns filtered_df, filtered_turnstile_df, filtered_no_turnstile_df"""
		filtered_df = self.etapas_df[(self.etapas_df['mismo_servicio']==True) & (self.etapas_df['mismo_paradero']==True) & (self.etapas_df['misma_patente']==True)]
		filtered_turnstile_df = filtered_df[filtered_df['si_2017_torniquete']==True] #Only 2017 turnstiles
		filtered_no_turnstile_df = filtered_df[filtered_df['si_torniquete']==False]  #Never-installed turnstiles.
		return filtered_df, filtered_turnstile_df, filtered_no_turnstile_df
		