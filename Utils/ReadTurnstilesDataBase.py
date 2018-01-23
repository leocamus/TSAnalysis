"""Reads turnstile database into a pandas dataframe"""
import os
import pandas as pd
import re
from Utils import TransantiagoConstants

busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir

def readTurnstileData():
	"""Reading turnstile data"""
	ana_turnstiles_file = 'Torniquetes_Instalados_19.01.18.xlsx'
	mauricio_turnstiles_file = 'Avance_Consolidado_v2.xlsx'

	ana_turnstiles_path = os.path.join(busesTorniqueteDir, ana_turnstiles_file)
	mauricio_turnstiles_path = os.path.join(busesTorniqueteDir, mauricio_turnstiles_file)

	ana_turnstiles_df = pd.read_excel(ana_turnstiles_path) #dates are parsed as pandas._libs.tslib.Timestamp
	mauricio_turnstiles_df = pd.read_excel(mauricio_turnstiles_path) #dates are parsed as pandas._libs.tslib.Timestamp

	ana_turnstiles_df.columns = ['UN','sitio_subida','fecha_instalacion']
	mauricio_turnstiles_df.columns = ['sitio_subida', 'fecha_instalacion']

	return ana_turnstiles_df, mauricio_turnstiles_df

def processMauricioTurnstiles(mauricio_turnstiles_df):
	pass #Nothing to-do

def processAnaTurnstiles(ana_turnstiles_df):
	"""reads and formats plates"""
	for index,row in ana_turnstiles_df.iterrows():
		patente = row['sitio_subida']
		if '-' not in patente:
			patente = re.split('(\d+)',patente)[0] + '-' + re.split('(\d+)',patente)[1]
		ana_turnstiles_df.loc[index,'sitio_subida'] = patente

	return ana_turnstiles_df

def printTurnstile(ana_turnstiles_df,mauricio_turnstiles_df):
	ana_path = os.path.join(busesTorniqueteDir, 'ana_torniquetes_file.xlsx')
	mauricio_path = os.path.join(busesTorniqueteDir, 'mauricio_torniquetes_file.xlsx')
	ana_turnstiles_df.to_excel(ana_path)
	mauricio_turnstiles_df.to_excel(mauricio_path)
