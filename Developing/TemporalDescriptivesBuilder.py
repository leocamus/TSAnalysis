from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import numpy as np
import os
import datetime as dt

SSHDir = TransantiagoConstants.SSHDir
busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir
DTPMDir = TransantiagoConstants.DTPMDir
currentSSHDates = TransantiagoConstants.updateCurrentSSHDates()

class TemporalDescriptivesBuilderClass:

	def __init__(self,date):
		self.analyzedDate = date
		self.df = pd.DataFrame()
		self.periods = pd.DataFrame()

	def loadEtapas(self):
		"""Returns the simplified etapas-file as pandas df"""
		try:
			if self.analyzedDate in currentSSHDates:
				simplifiedEtapasFile = self.analyzedDate + '_simplified.etapas'
				simplifiedEtapasPath = os.path.join(SSHDir, simplifiedEtapasFile)	
			else:
				raise ValueError('date is not correctly specified')
		except ValueError as dateErr:
			print(dateErr)
		self.df = pd.read_table(simplifiedEtapasPath, sep='|', encoding='latin-1')

	def loadPeriods(self):
		periods_path = os.path.join(DTPMDir,'periodos_ts.xlsx')
		self.periods = pd.read_excel(periods_path, encoding = 'latin-1')

	def cleanAndProcessEtapas(self):
		"""Returns a clean pandas dataframe without '-' values and pre-processed"""	
		self.df = self.df[self.df.t_subida != '-']
		self.df = self.df[self.df.servicio_subida != '-']
		self.df = self.df[self.df.par_subida != '-']
		self.df = self.df[self.df.sitio_subida != '-']

		self.df['t_subida']=pd.to_datetime(self.df.t_subida)
		self.df = self.df.sort_values(by=['sitio_subida', 't_subida'], ascending=[True, True])
		self.df = self.df.reset_index(drop=True)

		torniquetesFile = 'Avance_Consolidado_v2.xlsx'
		torniquetesDataPath = os.path.join(busesTorniqueteDir, torniquetesFile)
		busesTorniquete_df = pd.read_excel(torniquetesDataPath)
		busesTorniquete_df.columns=['sitio_subida','fecha_instalacion']
		self.df = pd.merge(self.df,busesTorniquete_df, on='sitio_subida', how='left')
		checking_missing = pd.isnull(self.df['fecha_instalacion'])
		print('Not found in turnstile database: ' + str(sum(checking_missing))) #Without turnstiles, then NaT.
		self.df['fecha_instalacion'] = pd.to_datetime(self.df.fecha_instalacion)

		self.df['mismo_paradero'] = (self.df['par_subida']==self.df['par_subida'].shift()).fillna(False)
		self.df['misma_patente'] = (self.df['sitio_subida']==self.df['sitio_subida'].shift()).fillna(False)
		self.df['mismo_servicio'] = (self.df['servicio_subida']==self.df['servicio_subida'].shift()).fillna(False)
		self.df.loc[(self.df.mismo_servicio == True) & (self.df.mismo_paradero == True) & (self.df.misma_patente == True), 'diferencia_tiempo'] = (self.df['t_subida']-self.df['t_subida'].shift())
		self.df['diferencia_tiempo_secs'] = self.df['diferencia_tiempo'].dt.total_seconds()
		self.df['si_torniquete'] = (self.df['fecha_instalacion']<=self.df['t_subida'])
		self.df['si_2017_torniquete'] = ((self.df['fecha_instalacion']<=self.df['t_subida'])&(self.df['fecha_instalacion']>=pd.to_datetime('2017-01-01')))

	def appendPeriods(self):
		week = set([0,1,2,3,4])
		saturday = set([5])
		sunday = set([6])
		day = dt.datetime.strptime(self.analyzedDate, '%Y-%m-%d').date()

		week_periods = self.periods[self.periods['tipo_dia']=='LABORAL']
		saturday_periods = self.periods[self.periods['tipo_dia']=='SABADO']
		sunday_periods = self.periods[self.periods['tipo_dia']=='DOMINGO']

		if day.weekday() in week:
			n = []
			for index,row in week_periods.iterrows():
				period_name = row['periodo']
				n.append(period_name)
				self.df[period_name] = np.where((week_periods.loc[index,'inicio'] <= self.df['t_subida'].dt.time)&(self.df['t_subida'].dt.time <=week_periods.loc[index,'fin']) , period_name, '')
			self.df['PERIODO'] =  self.df[n[0]] + self.df[n[1]] + self.df[n[2]] + self.df[n[3]] + self.df[n[4]] + self.df[n[5]] + self.df[n[6]] + self.df[n[7]] + self.df[n[8]] + self.df[n[9]] + self.df[n[10]] + self.df[n[11]]
			self.df = self.df.drop([n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[7],n[8],n[9],n[10],n[11]],axis=1)
		elif day.weekday() in saturday:
			n = []
			for index,row in saturday_periods.iterrows():
				period_name = row['periodo']
				n.append(period_name)
				self.df[period_name] = np.where((saturday_periods.loc[index,'inicio'] <= self.df['t_subida'].dt.time)&(self.df['t_subida'].dt.time <=saturday_periods.loc[index,'fin']) , period_name, '')
			self.df['PERIODO'] =  self.df[n[0]] + self.df[n[1]] + self.df[n[2]] + self.df[n[3]] + self.df[n[4]] + self.df[n[5]] + self.df[n[6]] + self.df[n[7]] + self.df[n[8]]
			self.df = self.df.drop([n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[7],n[8]],axis=1)
		else:
			n = []
			for index,row in sunday_periods.iterrows():
				period_name = row['periodo']
				n.append(period_name)
				self.df[period_name] = np.where((sunday_periods.loc[index,'inicio'] <= self.df['t_subida'].dt.time)&(self.df['t_subida'].dt.time <=sunday_periods.loc[index,'fin']) , period_name, '')			
			self.df['PERIODO'] =  self.df[n[0]] + self.df[n[1]] + self.df[n[2]] + self.df[n[3]] + self.df[n[4]] + self.df[n[5]] + self.df[n[6]] + self.df[n[7]]
			self.df = self.df.drop([n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[7]],axis=1)


