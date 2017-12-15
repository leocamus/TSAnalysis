import pandas as pd
import numpy as np
import datetime as dt
import os

from Utils import TransantiagoConstants

RFADir = TransantiagoConstants.RFADir
DTPMDir = TransantiagoConstants.DTPMDir

first_quarter_path = RFADir + r'\01_EvasionTrimestral\01_analisis\1st_quarter.xlsx'
second_quarter_path = RFADir + r'\01_EvasionTrimestral\01_analisis\2nd_quarter.xlsx'
third_quarter_path = RFADir + r'\01_EvasionTrimestral\01_analisis\3rd_quarter.xlsx'
codes_path = DTPMDir + r'\codes_services.xlsx'

def loadSinglesEvasion():
	"""Returns evasion databases as pandas ddff"""
	first_q = pd.read_excel(first_quarter_path, encoding = 'latin-1')
	second_q = pd.read_excel(second_quarter_path, encoding = 'latin-1')
	third_q = pd.read_excel(third_quarter_path, encoding = 'latin-1')

	return first_q, second_q, third_q

def processSinglesEvasiondAndConcat(first_q, second_q, third_q):
	"""Returns evasion databases as one single pandas ddff"""
	del second_q['TIPO'] #For consistency

	columns_names = {
	'FECHA ':'FECHA',
	'SERVICIO':'SERVICIO',
	'PLACA PATENTE':'PATENTE',
	'NUMERO DE PUERTAS':'PUERTAS',
	'PUERTA NUMERO':'N_PUERTA',
	'LUGAR INICIO':'LUGAR_INICIO',
	'HORA INICIO':'HORA_INICIO',
	'HORA':'HORA',
	'MINUTOS':'MINUTO',
	'INGRESAN':'INGRESAN',
	'NO VALIDAN':'NO_VALIDAN',
	'TP':'TP'}

	first_q = first_q.rename(columns = columns_names)
	second_q = second_q.rename(columns = columns_names)
	third_q = third_q.rename(columns = columns_names)

	first_q['TIEMPO'] = first_q['HORA'].astype(str)+':'+first_q['MINUTO'].astype(str)+':00'
	second_q['TIEMPO'] = second_q['HORA'].astype(str)+':'+second_q['MINUTO'].astype(str)+':00'
	third_q['TIEMPO'] = third_q['HORA'].astype(str)+':'+third_q['MINUTO'].astype(str)+':00'

	frames = [first_q, second_q, third_q]
	complete_evasion = pd.concat(frames, keys=['first', 'second', 'third'])

	return complete_evasion

def mergeTransantiagoCodes(complete_evasion):
	"""Process and merges transantiago codes to evasion ddff"""
	codes = pd.read_excel(codes_path, encoding = 'latin-1')
	codes_ida = codes[codes['DIRECTION']=='Ida']
	codes_ret = codes[codes['DIRECTION']=='Ret']
	codes_ida = codes_ida.rename(columns = {'USER_CODE':'SERVICIO'})
	codes_ret = codes_ret.rename(columns = {'USER_CODE':'SERVICIO'})
	del codes_ida['DIRECTION']
	del codes_ret['DIRECTION']

	complete_evasion_w_codes = pd.merge(complete_evasion,codes_ida, on=['SERVICIO'], how='left')
	
	not_founded_services = complete_evasion_w_codes.loc[complete_evasion_w_codes['TS_CODE'].isnull(),'SERVICIO'].unique().tolist()
	print('The only non-matched user_code services are: ') 
	print(*not_founded_services, sep='\n') #Should be only D06, so the line below makes sense. Anyway, it is hardcoded so be aware.
	complete_evasion_w_codes.loc[complete_evasion_w_codes['TS_CODE'].isnull(),'TS_CODE']='446'
	
	return complete_evasion_w_codes

def processCompleteEvasionDataFrame(complete_evasion_w_codes):
	"""Processing evasion_with_codes dataframe for consistency with trx databases."""
	complete_evasion_w_codes['PATENTE'] =  complete_evasion_w_codes['PATENTE'].str.replace(' ','')

	complete_evasion_w_codes['SERVICIO_TMP'] = complete_evasion_w_codes['SERVICIO'].apply(str)
	complete_evasion_w_codes['TS_CODE_TMP'] = complete_evasion_w_codes['TS_CODE'].apply(str)

	del complete_evasion_w_codes['SERVICIO']
	del complete_evasion_w_codes['TS_CODE']

	processed_evasion = complete_evasion_w_codes.rename(columns = {'SERVICIO_TMP':'SERVICIO_USUARIO', 'TS_CODE_TMP':'SERVICIO'})

	return processed_evasion

def deleteDuplicatedInCompleteEvasion(processed_evasion):
	columns_names = ['FECHA','PATENTE','PUERTAS','N_PUERTA','HORA_INICIO','HORA','MINUTO','TP','TIEMPO','UN','SERVICIO_USUARIO','SERVICIO']
	
	#Getting duplicated rows
	duplicated_evasion = processed_evasion.loc[processed_evasion.duplicated(columns_names, keep=False),:]
	print('Number of duplicated rows in complete evasion database is: ' + str(len(duplicated_evasion.index)))

	#Colapsing duplicated rows
	grouped_duplicated_evasion = duplicated_evasion.groupby(columns_names)['INGRESAN','NO_VALIDAN'].sum()
	grouped_duplicated_evasion = grouped_duplicated_evasion.reset_index()
	print('Number of collapsed-duplicated rows in complete evasion database is: ' + str(len(grouped_duplicated_evasion.index)))

	#Deleting duplicated rows in complete evasion database
	non_duplicated_evasion = processed_evasion.drop_duplicates(columns_names, keep=False)
	print('Number of rows in complete evasion database without duplicated rows at all is: ' + str(len(non_duplicated_evasion.index)))

	#Appending	
	frames = [non_duplicated_evasion, grouped_duplicated_evasion]
	clean_processed_evasion = pd.concat(frames)
	clean_processed_evasion = clean_processed_evasion.reset_index(drop=True)
	print('Final number of rows in complete evasion database with collapsed duplicated rows is: ' + str(len(clean_processed_evasion.index)))

	return clean_processed_evasion