from Utils import TransantiagoConstants
from Utils import ReadTurnstilesDataBase
import pandas as pd
import numpy as np

class LBS_analysis_functionality_class:

	def __init__(self, month, name):
		self.month = month
		self.name = name
		self.lbs_df =  pd.DataFrame()

	def loadLBS(self):
		lbs_path = 'G:/LeoCamus/0_LBS/2017/' +  self.month + '/' + self.name + '.csv'
		self.lbs_df = pd.read_csv(lbs_path, sep=';', encoding='latin-1', na_values='None') #Dates and times are not parsed. Missing values were translated in Access query as 'None'
		self.lbs_df = self.lbs_df.drop(['Unnamed: 11'], axis=1)
		self.lbs_df = self.lbs_df.dropna(axis=0, how='any')
		self.lbs_df = self.lbs_df.rename(columns=lambda x: x.replace('í', 'i')) #Changing 'Período' to 'Periodo'...
		self.lbs_df.loc[:,'Fecha'] = pd.to_datetime(self.lbs_df.loc[:,'LBS.[Fecha]'], format='%d/%m/%Y').dt.date
		self.lbs_df.loc[:,'Media_hora'] = pd.to_datetime(self.lbs_df.loc[:,'LBS.[Cada media Hora]'], format='%Y-%m-%d %H:%M:%S').dt.time

	def simplifyingLBS_byDayByPeriod(self, day, period_number):
		switcher_day = {
		'monday': 0,
		'tuesday': 1,
		'wednesday': 2,
		'thursday': 3,
		'friday': 4,
		'saturday': 5,
		'sunday': 6
		}
		switcher_period = {
		1: '01 - Pre Nocturno',
		2: '02 - Nocturno',
		3: '03 - Transición Nocturno',
		4: '04 - Punta Mañana',
		5: '05 - Transición Punta Mañana',
		6: '06 - Fuera de Punta Mañana',
		7: '07 - Punta Mediodía',
		8: '08 - Fuera de Punta Tarde',
		9: '09 - Punta Tarde',
		10: '10 - Transición Punta Tarde',
		11: '11 - Fuera de Punta Nocturno',
		12: '12 - Pre Nocturno',
		13: '13 - Pre Nocturno Sábado',
		14: '14 - Nocturno Sábado',
		15: '15 - Transición Sábado Mañana',
		16: '16 - Punta Mañana Sábado',
		17: '17 - Mañana Sábado',
		18: '18 - Punta Mediodía Sábado',
		19: '19 - Tarde Sábado',
		20: '20 - Transición Sábado Nocturno',
		21: '21 - Pre Nocturno Sábado',
		22: '22 - Pre Nocturno Domingo',
		23: '23 - Nocturno Domingo',
		24: '24 - Transición Domingo Mañana',
		25: '25 - Mañana Domingo',
		26: '26 - Mediodía Domingo',
		27: '27 - Tarde Domingo',
		28: '28 - Transición Domingo Nocturno',
		29: '29 - Pre Nocturno Domingo'
		}
	
		day_number = switcher_day.get(day)
		period_name = switcher_period.get(period_number)
	
		self.lbs_df = self.lbs_df.loc[(self.lbs_df['Fecha'].apply(lambda x: x.weekday())==day_number)&(self.lbs_df.loc[:,'LBS.[Periodo]']==period_name),:]

	def simplifyingLBS_byPeriod(self, period_number):
		switcher_period = {
		1: '01 - Pre Nocturno',
		2: '02 - Nocturno',
		3: '03 - Transición Nocturno',
		4: '04 - Punta Mañana',
		5: '05 - Transición Punta Mañana',
		6: '06 - Fuera de Punta Mañana',
		7: '07 - Punta Mediodía',
		8: '08 - Fuera de Punta Tarde',
		9: '09 - Punta Tarde',
		10: '10 - Transición Punta Tarde',
		11: '11 - Fuera de Punta Nocturno',
		12: '12 - Pre Nocturno',
		13: '13 - Pre Nocturno Sábado',
		14: '14 - Nocturno Sábado',
		15: '15 - Transición Sábado Mañana',
		16: '16 - Punta Mañana Sábado',
		17: '17 - Mañana Sábado',
		18: '18 - Punta Mediodía Sábado',
		19: '19 - Tarde Sábado',
		20: '20 - Transición Sábado Nocturno',
		21: '21 - Pre Nocturno Sábado',
		22: '22 - Pre Nocturno Domingo',
		23: '23 - Nocturno Domingo',
		24: '24 - Transición Domingo Mañana',
		25: '25 - Mañana Domingo',
		26: '26 - Mediodía Domingo',
		27: '27 - Tarde Domingo',
		28: '28 - Transición Domingo Nocturno',
		29: '29 - Pre Nocturno Domingo'
		}
	
		period_name = switcher_period.get(period_number)	
		self.lbs_df = self.lbs_df.loc[self.lbs_df.loc[:,'LBS.[Periodo]']==period_name,:]

	def simplifyingLBS_byMidHr(self, midHr_string, dayType):
		#TODO: Consider to refactor this. Mid_Hrs can be mapped to periods.
		midHr_time = pd.to_datetime(midHr_string, format='%H:%M:%S').time()
		if dayType=='laboral':
			self.lbs_df = self.lbs_df.loc[(self.lbs_df.loc[:,'Media_hora']==midHr_time)&(1<=self.lbs_df.loc[:,'LBS.[Periodo]'].apply(lambda x: int(x.split('-')[0])))&(self.lbs_df.loc[:,'LBS.[Periodo]'].apply(lambda x: int(x.split('-')[0]))<=12),:]
		elif dayType=='saturday':
			self.lbs_df = self.lbs_df.loc[(self.lbs_df.loc[:,'Media_hora']==midHr_time)&(13<=self.lbs_df.loc[:,'LBS.[Periodo]'].apply(lambda x: int(x.split('-')[0])))&(self.lbs_df.loc[:,'LBS.[Periodo]'].apply(lambda x: int(x.split('-')[0]))<=21),:]
		else:
			self.lbs_df = self.lbs_df.loc[(self.lbs_df.loc[:,'Media_hora']==midHr_time)&(22<=self.lbs_df.loc[:,'LBS.[Periodo]'].apply(lambda x: int(x.split('-')[0])))&(self.lbs_df.loc[:,'LBS.[Periodo]'].apply(lambda x: int(x.split('-')[0]))<=29),:]


	def travelTimeProcessing(self):
		self.lbs_df.loc[:,'Tiempo_Expedicion'] = pd.to_datetime(self.lbs_df.loc[:,'LBS.[Tiempo (hh:mm:ss)]'], format='%Y-%m-%d %H:%M:%S').dt.time
		self.lbs_df.loc[:,'Tiempo_Expedicion_secs'] = self.lbs_df.loc[:,'Tiempo_Expedicion'].apply(lambda x: x.hour*60*60 + x.minute*60 + x.second)
		self.lbs_df.loc[:,'ser_sen'] = self.lbs_df.loc[:,'LBS.[Servicio]'] + self.lbs_df.loc[:,'LBS.[Sentido]'].apply(lambda x: x[:1])
	

	def mergeTurnstileDatabase(self):
		[ana_turnstiles_df, mauricio_turnstiles_df] = ReadTurnstilesDataBase.readTurnstileData()
		ana_turnstiles_df = ReadTurnstilesDataBase.processAnaTurnstiles(ana_turnstiles_df)

		self.lbs_df = self.lbs_df.merge(ana_turnstiles_df, left_on = 'LBS.[Patente]', right_on = 'sitio_subida', how='left')
		self.lbs_df = self.lbs_df.merge(mauricio_turnstiles_df, left_on = 'LBS.[Patente]', right_on = 'sitio_subida' , suffixes=('_ana', '_mauricio'), how='left')

		torniquetes_mariposa_conditions = (self.lbs_df.loc[:,'fecha_instalacion_ana'].dt.date<self.lbs_df.loc[:,'Fecha'])

		self.lbs_df['min_fecha'] = pd.concat([self.lbs_df['fecha_instalacion_ana'], self.lbs_df['fecha_instalacion_mauricio']], axis=1).min(axis=1)
		no_torniquetes_conditions = (((self.lbs_df.loc[:,'fecha_instalacion_ana'].isnull()) & (self.lbs_df.loc[:,'fecha_instalacion_mauricio'].isnull())) | (self.lbs_df.loc[:,'Fecha']<=self.lbs_df['min_fecha'].dt.date))

		self.lbs_df.loc[:,'torniquete_mariposa'] = np.where(torniquetes_mariposa_conditions,1,0)
		self.lbs_df.loc[:,'no_torniquete'] = np.where(no_torniquetes_conditions,1,0)

