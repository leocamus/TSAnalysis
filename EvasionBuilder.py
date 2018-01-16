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

def deleteDuplicatedInCompleteEvasion(complete_evasion):

	print('Original number of rows in complete evasion database is: ' + str(len(complete_evasion.index)))
	#All columns except for 'INGRESAN' and 'NO_VALIDAN'
	columns_names = ['FECHA', 'SERVICIO', 'PATENTE', 'PUERTAS', 'N_PUERTA', 'LUGAR_INICIO','HORA_INICIO', 'HORA', 'MINUTO','TP','TIEMPO']
	
	#Getting duplicated rows
	duplicated_evasion = complete_evasion.loc[complete_evasion.duplicated(columns_names, keep=False),:]
	print('Number of duplicated rows in complete evasion database is: ' + str(len(duplicated_evasion.index)))

	#Collapsing duplicated rows
	grouped_duplicated_evasion = duplicated_evasion.groupby(columns_names)['INGRESAN','NO_VALIDAN'].sum()
	grouped_duplicated_evasion = grouped_duplicated_evasion.reset_index()
	print('Number of collapsed-duplicated rows in complete evasion database is: ' + str(len(grouped_duplicated_evasion.index)))

	#Deleting duplicated rows in complete evasion database
	non_duplicated_evasion = complete_evasion.drop_duplicates(columns_names, keep=False)
	print('Number of rows in complete evasion database without duplicated rows at all is: ' + str(len(non_duplicated_evasion.index)))

	#Appending	
	frames = [non_duplicated_evasion, grouped_duplicated_evasion]
	clean_complete_evasion = pd.concat(frames)
	clean_complete_evasion = clean_complete_evasion.reset_index(drop=True)
	print('Final number of rows in complete evasion database with collapsed duplicated rows is: ' + str(len(clean_complete_evasion.index)))

	return clean_complete_evasion

def mergeTransantiagoCodes(clean_complete_evasion):
	"""Process and merges transantiago codes to evasion ddff. TODO: Please consider to review this."""
	codes = pd.read_excel(codes_path, encoding = 'latin-1')
	
	codes_ida = codes[codes['DIRECTION']=='Ida']
	codes_ret = codes[codes['DIRECTION']=='Ret']

	# Both, USER_CODE and TS_CODE should be strings, in both codes_ida and codes_ret.
	codes_ida.loc[:,'USER_CODE_TMP'] = codes_ida.loc[:,'USER_CODE'].apply(str)
	codes_ida.loc[:,'TS_CODE_TMP'] = codes_ida.loc[:,'TS_CODE'].apply(str)

	codes_ret.loc[:,'USER_CODE_TMP'] = codes_ret.loc[:,'USER_CODE'].apply(str)
	codes_ret.loc[:,'TS_CODE_TMP'] = codes_ret.loc[:,'TS_CODE'].apply(str)

	del codes_ida['DIRECTION']
	del codes_ret['DIRECTION']

	del codes_ida['TS_CODE']
	del codes_ida['USER_CODE']

	del codes_ret['TS_CODE']
	del codes_ret['USER_CODE']

	#Cleaning codes from special services. Be aware of this since it might generates errors in the final merging with trx database.
	clean_codes_ida = codes_ida[(~codes_ida["TS_CODE_TMP"].str.contains('y'))&(~codes_ida["TS_CODE_TMP"].str.contains('Y'))]
	clean_codes_ret = codes_ida[(~codes_ida["TS_CODE_TMP"].str.contains('y'))&(~codes_ida["TS_CODE_TMP"].str.contains('Y'))]

	clean_codes_ida = clean_codes_ida.rename(columns = {'USER_CODE_TMP':'SERVICIO', 'TS_CODE_TMP':'TS_CODE'})
	clean_codes_ret = clean_codes_ret.rename(columns = {'USER_CODE_TMP':'SERVICIO', 'TS_CODE_TMP':'TS_CODE'})

	#Changing type of SERVICIO in clean_complete_evasion database
	clean_complete_evasion.loc[:,'SERVICIO_TMP'] = clean_complete_evasion.loc[:,'SERVICIO'].apply(str)
	del clean_complete_evasion['SERVICIO']
	clean_complete_evasion = clean_complete_evasion.rename(columns = {'SERVICIO_TMP' : 'SERVICIO'})

	#Merging...
	clean_complete_evasion_w_codes = pd.merge(clean_complete_evasion,clean_codes_ida, on=['SERVICIO'], how='left') #Merging with codes_ida is hardcoded, be aware.
	
	not_founded_services = clean_complete_evasion_w_codes.loc[clean_complete_evasion_w_codes['TS_CODE'].isnull(),'SERVICIO'].unique().tolist()

	print('The only non-matched user_code services are: ')
	print(*not_founded_services, sep='\n') #Should be only D06, so the line below makes sense. Anyway, it is hardcoded so be aware.
	clean_complete_evasion_w_codes.loc[clean_complete_evasion_w_codes['TS_CODE'].isnull(),'TS_CODE']='446'
	
	return clean_complete_evasion_w_codes

def processCompleteEvasionDataFrame(clean_complete_evasion_w_codes):
	"""Processing evasion_with_codes dataframe for consistency with trx databases."""
	clean_complete_evasion_w_codes['PATENTE'] =  clean_complete_evasion_w_codes['PATENTE'].str.replace(' ','')

	clean_complete_evasion_w_codes.loc[:,'TIEMPO'] = clean_complete_evasion_w_codes.loc[:,'FECHA'].dt.strftime('%Y-%m-%d') + ' ' + clean_complete_evasion_w_codes.loc[:,'TIEMPO']
	clean_complete_evasion_w_codes['TIEMPO'] = pd.to_datetime(clean_complete_evasion_w_codes['TIEMPO'])

	processed_evasion = clean_complete_evasion_w_codes.rename(columns = {'SERVICIO':'SERVICIO_USUARIO', 'TS_CODE':'SERVICIO'})

	return processed_evasion

def runCompleteProcess():
	[first_q, second_q, third_q] = loadSinglesEvasion()
	complete_evasion = processSinglesEvasiondAndConcat(first_q,second_q,third_q)
	clean_complete_evasion = deleteDuplicatedInCompleteEvasion(complete_evasion)
	clean_complete_evasion_w_codes = mergeTransantiagoCodes(clean_complete_evasion)
	processed_evasion = processCompleteEvasionDataFrame(clean_complete_evasion_w_codes)
	return processed_evasion

def updateCommonDates(df):
	#Could be better coded.
	currentSSHDates = TransantiagoConstants.updateCurrentSSHDates()
	measured_dates = set(df['FECHA'])
	evasion_dates = [x.strftime('%Y-%m-%d') for x in measured_dates]
	common_dates = 	sorted(list(set(evasion_dates).intersection(currentSSHDates)))
	return common_dates
