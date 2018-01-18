"""Module to run the complete methodology for building histograms, and build it silently"""
from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import numpy as np
import os
import datetime as dt

class RunSilentlyDailyPerfilesBuilderClass:

	SSHDir = TransantiagoConstants.SSHDir
	busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir
	currentSSHDates = TransantiagoConstants.updateCurrentSSHDates()
	DTPMDir = TransantiagoConstants.DTPMDir

	def total(x): return (x == 1).sum()

	def loadCodes():
		codes_path = os.path.join(RunSilentlyDailyPerfilesBuilderClass.DTPMDir, 'codes_services.xlsx')
		codes = pd.read_excel(codes_path, encoding = 'latin-1')
		return codes

	def __init__(self,date,vehicle='BUS',zp='0'):
		self.analyzedDate = date
		self.analyzedVehicle = vehicle
		self.if_ZP = zp
		self.perfiles_df = pd.DataFrame()
		self.grouped_data = pd.DataFrame()
		self.codes = pd.DataFrame()

	def runSimplifyPerfiles(self):
		"""Not always necessary. Reducing the complexity of the original etapas-file. Attributes to extract are hardcoded"""
		SimplifyFilesUtils.writeSimplifiedPerfiles(self.analyzedDate,self.if_ZP,'ServicioSentido','Patente','Paradero','Hini','Hfin','idExpedicion','DistEnRuta')

	def loadSimplifiedPerfiles(self):
		"""Returns the simplified perfiles-file as pandas df"""
		try:
			if self.analyzedDate in RunSilentlyDailyPerfilesBuilderClass.currentSSHDates:
				simplifiedPerfilesFile = self.analyzedDate + '_simplified.perfiles'
				simplifiedPerfilesPath = os.path.join(RunSilentlyDailyPerfilesBuilderClass.SSHDir, simplifiedPerfilesFile)	
			else:
				raise ValueError('date is not correctly specified')
		except ValueError as dateErr:
			print(dateErr)

		self.perfiles_df = pd.read_table(simplifiedPerfilesPath, sep='|', parse_dates = [3,4] ,encoding='latin-1')

	def dropParaderos(self):
		self.perfiles_df.drop_duplicates(['ServicioSentido','Patente','idExpedicion'], keep='first', inplace=True)
		self.perfiles_df.reset_index(drop=True,inplace=True)

	def mergeTurnstileDatabase(self):
		"""Merges the loaded etapas-file with the turnstile-file.fecha_instalacion into a pandas df and returns it"""
		torniquetesFile = 'Avance_Consolidado_v2.xlsx'
		torniquetesDataPath = os.path.join(RunSilentlyDailyPerfilesBuilderClass.busesTorniqueteDir, torniquetesFile)
		busesTorniquete_df = pd.read_excel(torniquetesDataPath, encoding = 'latin-1')
		busesTorniquete_df.columns=['sitio_subida','fecha_instalacion']
		self.perfiles_df = self.perfiles_df.merge(busesTorniquete_df, left_on='Patente', right_on = 'sitio_subida', how='left')
		checking_missing = pd.isnull(self.perfiles_df['fecha_instalacion'])
		print('Not found in turnstile database: ' + str(sum(checking_missing))) #Without turnstiles, then NaT.
		self.perfiles_df.loc[:,'torniquete_2017_fecha'] = np.where(((self.perfiles_df.loc[:,'fecha_instalacion']>=pd.to_datetime('2017-01-01')) & (self.perfiles_df['fecha_instalacion'] < self.perfiles_df['Hini'])),1,0)
		self.perfiles_df.loc[:,'sin_torniquete'] = np.where((self.perfiles_df.loc[:,'fecha_instalacion'].isnull()),1,0)

	def groupByTurnstilePresence(self):
		f = {'torniquete_2017_fecha': [RunSilentlyDailyPerfilesBuilderClass.total], 'sin_torniquete': [RunSilentlyDailyPerfilesBuilderClass.total]}
		self.grouped_data = self.perfiles_df.groupby(['ServicioSentido']).agg(f)
		self.grouped_data.reset_index(inplace=True)
		columns = []
		for col in self.grouped_data.columns.values:
			if col[1]!='':
				col = '_'.join(col).strip()
			else:
				col = ''.join(col).strip()
			
			columns.append(col)

		self.grouped_data.columns = columns

	def appendUnidadNegocio(self):
		codes = RunSilentlyDailyPerfilesBuilderClass.loadCodes()		
		self.grouped_data['simplified_servicio'] = ''
		self.grouped_data.loc[:,'simplified_servicio'] = self.grouped_data.loc[:,'ServicioSentido'].str.replace('T','')
		self.grouped_data.loc[:,'simplified_servicio'] = self.grouped_data.loc[:,'simplified_servicio'].str.replace('00','')
		self.grouped_data.loc[:,'TS_CODE'] = self.grouped_data.loc[:,'simplified_servicio'].str.split(' ').str[0]
		self.grouped_data.loc[:,'DIRECTION'] = self.grouped_data.loc[:,'simplified_servicio'].str[-1:]
		self.grouped_data.loc[:,'DIRECTION'] = self.grouped_data.loc[:,'DIRECTION'].str.replace('R','Ret')
		self.grouped_data.loc[:,'DIRECTION'] = self.grouped_data.loc[:,'DIRECTION'].str.replace('I','Ida')
		#Before merging, codes['TS_CODE'] should be string type.
		codes['TS_CODE'] = codes['TS_CODE'].astype(str)
		#Merging...
		self.grouped_data = pd.merge(self.grouped_data,codes, on=['TS_CODE','DIRECTION'], how='left')
		self.grouped_data = self.grouped_data.drop(['simplified_servicio'],axis=1)
		#Verifying null values.
		self.grouped_data.loc[(self.grouped_data['UN'].isnull()) & (self.grouped_data['TS_CODE'].str[:1]=='1'),'UN'] = 1 #OK.
		self.grouped_data.loc[(self.grouped_data['UN'].isnull()) & (self.grouped_data['TS_CODE'].str[:1]=='2'),'UN'] = 2 #OK.
		self.grouped_data.loc[(self.grouped_data['UN'].isnull()) & (self.grouped_data['TS_CODE'].str[:1]=='3'),'UN'] = 3 #OK.
		self.grouped_data.loc[(self.grouped_data['UN'].isnull()) & (self.grouped_data['TS_CODE'].str[:1]=='4'),'UN'] = 4 #OK.
		self.grouped_data.loc[(self.grouped_data['UN'].isnull()) & (self.grouped_data['TS_CODE'].str[:1]=='5'),'UN'] = 5 #OK.
		self.grouped_data.loc[(self.grouped_data['UN'].isnull()) & (self.grouped_data['TS_CODE'].str[:1]=='B'),'UN'] = 6 #OK.
		self.grouped_data.loc[(self.grouped_data['UN'].isnull()) & (self.grouped_data['TS_CODE'].str[:1]=='F'),'UN'] = 7 #OK.

