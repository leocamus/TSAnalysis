"""Module to run the complete methodology for building descriptives per day"""
from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants

import DailyEtapasBuilder
import pandas as pd
import numpy as np
import os
import datetime as dt

def loadPeriods():
	periods_path = os.path.join(TemporalDescriptivesBuilderClass.DTPMDir,'periodos_ts.xlsx')
	periods = pd.read_excel(periods_path, encoding = 'latin-1')
	return periods

def loadCodes():
	codes_path = os.path.join(TemporalDescriptivesBuilderClass.DTPMDir, 'codes_services.xlsx')
	codes = pd.read_excel(codes_path, encoding = 'latin-1')
	return codes

class TemporalDescriptivesBuilderClass:

	SSHDir = TransantiagoConstants.SSHDir
	busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir
	DTPMDir = TransantiagoConstants.DTPMDir
	currentSSHDates = TransantiagoConstants.updateCurrentSSHDates()

	def __init__(self,date):
		self.analyzedDate = date
		self.df = pd.DataFrame()
		self.grouped_data = pd.DataFrame()		
		self.df = pd.DataFrame()

	def loadEtapasAndOthers(self):
		"""Loads the simplified etapas-file as pandas df"""
		etapas_builder = DailyEtapasBuilder.RunSilentlyDailyEtapasBuilderClass(self.analyzedDate)
		etapas_builder.loadSimplifiedEtapas()
		etapas_builder.mergeTurnstileData()
		etapas_builder.cleanDataFrame()
		etapas_builder.sortDataFrame()
		etapas_builder.postProcessingSortedDataFrame()
		self.df = etapas_builder.etapas_df

	def appendPeriods(self):
		week = set([0,1,2,3,4])
		saturday = set([5])
		sunday = set([6])
		day = dt.datetime.strptime(self.analyzedDate, '%Y-%m-%d').date()

		periods = loadPeriods()

		week_periods = periods[periods['tipo_dia']=='LABORAL']
		saturday_periods = periods[periods['tipo_dia']=='SABADO']
		sunday_periods = periods[periods['tipo_dia']=='DOMINGO']

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

	def groupData(self):
		f = {'id':['count'], 'torniquete_mariposa':['unique']}
		self.grouped_data = self.df.groupby( [ 'PERIODO', 'sitio_subida', 'servicio_subida'] ).agg(f)
		columns = []
		for col in self.grouped_data.columns.values:
			if col[1]!='':
				col = '_'.join(col).strip()
			else:
				col = ''.join(col).strip()

			columns.append(col)

		self.grouped_data.columns = columns
		self.grouped_data = self.grouped_data.reset_index()

	def appendUnidadNegocio(self):
		self.grouped_data['simplified_servicio'] = ''
		self.grouped_data.loc[:,'simplified_servicio'] = self.grouped_data.loc[:,'servicio_subida'].str.replace('T','')
		self.grouped_data.loc[:,'simplified_servicio'] = self.grouped_data.loc[:,'simplified_servicio'].str.replace('00','')
		self.grouped_data.loc[:,'TS_CODE'] = self.grouped_data.loc[:,'simplified_servicio'].str.split(' ').str[0]
		self.grouped_data.loc[:,'DIRECTION'] = self.grouped_data.loc[:,'simplified_servicio'].str[-1:]
		self.grouped_data.loc[:,'DIRECTION'] = self.grouped_data.loc[:,'DIRECTION'].str.replace('R','Ret')
		self.grouped_data.loc[:,'DIRECTION'] = self.grouped_data.loc[:,'DIRECTION'].str.replace('I','Ida')
		#Before merging, codes['TS_CODE'] should be string type.
		codes = loadCodes()
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
