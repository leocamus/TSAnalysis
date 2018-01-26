"""Module to run the complete methodology for building histograms, and build it silently"""
from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
from Utils import ReadTurnstilesDataBase

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

		self.etapas_df = pd.read_table(simplifiedEtapasPath, sep='|', encoding='latin-1', parse_dates = [3])

	def mergeTurnstileData(self):
		"""Merges the loaded etapas-file with the turnstile-file.fecha_instalacion into a pandas df"""
		[ana_turnstiles_df, mauricio_turnstiles_df] = ReadTurnstilesDataBase.readTurnstileData()
		ana_turnstiles_df = ReadTurnstilesDataBase.processAnaTurnstiles(ana_turnstiles_df)

		self.etapas_df = self.etapas_df.merge(ana_turnstiles_df, left_on = 'sitio_subida', right_on = 'sitio_subida', how='left')
		self.etapas_df = self.etapas_df.merge(mauricio_turnstiles_df, left_on = 'sitio_subida', right_on = 'sitio_subida' , suffixes=('_ana', '_mauricio'), how='left')

#		del self.etapas_df['sitio_subida_ana']
#		del self.etapas_df['sitio_subida_mauricio']

		torniquetes_mariposa_conditions = (self.etapas_df.loc[:,'fecha_instalacion_ana'].dt.date<self.etapas_df.loc[:,'t_subida'].dt.date)
		
		self.etapas_df['min_fecha'] = pd.concat([self.etapas_df['fecha_instalacion_ana'], self.etapas_df['fecha_instalacion_mauricio']], axis=1).min(axis=1)
		no_torniquetes_conditions = (((self.etapas_df.loc[:,'fecha_instalacion_ana'].isnull()) & (self.etapas_df.loc[:,'fecha_instalacion_mauricio'].isnull())) | (self.etapas_df.loc[:,'t_subida'].dt.date<=self.etapas_df['min_fecha'].dt.date))

		self.etapas_df.loc[:,'torniquete_mariposa'] = np.where(torniquetes_mariposa_conditions,1,0)
		self.etapas_df.loc[:,'no_torniquete'] = np.where(no_torniquetes_conditions,1,0)

	def cleanDataFrame(self):
		"""Returns a clean pandas dataframe without '-' values"""	
		self.etapas_df = self.etapas_df[(~self.etapas_df['t_subida'].isnull())]
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

	def filteringDf(self):
		"""Returns filtered_df, filtered_turnstile_df, filtered_no_turnstile_df"""
		filtered_df = self.etapas_df[(self.etapas_df['mismo_servicio']==True) & (self.etapas_df['mismo_paradero']==True) & (self.etapas_df['misma_patente']==True)]
		filtered_turnstile_df = filtered_df[filtered_df['torniquete_mariposa']==1] #Only 'mariposa' turnstiles
		filtered_no_turnstile_df = filtered_df[filtered_df['no_torniquete']==1]  #Never-installed turnstiles.
		return filtered_df, filtered_turnstile_df, filtered_no_turnstile_df
		