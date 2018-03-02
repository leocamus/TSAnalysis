from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
from Utils import ReadTurnstilesDataBase

import pandas as pd
import numpy as np
import os
import datetime as dt

DTPM_TRXDir = TransantiagoConstants.DTPM_TRXDir

def grouping_data(how_to, ana_turnstiles_df, mauricio_turnstiles_df):
	years = [2015,2016,2017]
	final_grouped_data = pd.DataFrame()

	for year in years:
		print('Year ' + str(year) + ' is being analyzed...')
		path = os.path.join(DTPM_TRXDir,'un_ppu_sersen_sumtrx_' + str(year) + '_by_date.csv')
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', usecols=[0,1,2,3,4,5], parse_dates=[3])
		df.columns = ['UN','PPU','SER_SEN','DATE','SUM_TRX','COUNT']
		print('Number of observations before merge info. of turnstile is: ' + str(len(df.index)))
		df = df.merge(ana_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida', how='left', suffixes=('','_ana'))
		df = df.merge(mauricio_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida' , suffixes=('_ana', '_mauricio'), how='left')
		print('Number of observations after merge info. of turnstile is: ' + str(len(df.index)))
		
		torniquetes_mariposa_conditions = (df.loc[:,'fecha_instalacion_ana'].dt.date<df.loc[:,'DATE'].dt.date)
		df.loc[:,'min_fecha'] = pd.concat([df['fecha_instalacion_ana'], df['fecha_instalacion_mauricio']], axis=1).min(axis=1)
		no_torniquetes_conditions = (((df.loc[:,'fecha_instalacion_ana'].isnull()) & (df.loc[:,'fecha_instalacion_mauricio'].isnull())) | (df.loc[:,'DATE'].dt.date<=df['min_fecha'].dt.date))
		df.loc[:,'torniquete_mariposa'] = np.where(torniquetes_mariposa_conditions,1,0)
		df.loc[:,'no_torniquete'] = np.where(no_torniquetes_conditions,1,0)

		f = {'SUM_TRX':{'pn_SUM_TRX':['sum']},'COUNT':{'pn_SUM_EXP':['sum']}}

		if(how_to=='by month') or (how_to=='by month by un'):
			df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year
			df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month

			if(how_to=='by month'):
				grouped_df = df.groupby(['YEAR','MONTH','torniquete_mariposa','no_torniquete']).agg(f)
				grouped_df.columns = grouped_df.columns.droplevel(1)
				grouped_df.reset_index(inplace=True,level=['torniquete_mariposa','no_torniquete'])
				months = grouped_df.groupby(['YEAR','MONTH']).agg({'pn_SUM_EXP': 'sum'})
				grouped_df.loc[:,'ratio'] = grouped_df['pn_SUM_EXP'].div(months['pn_SUM_EXP'], axis='index') * 100
			elif(how_to=='by month by un'):
				grouped_df = df.groupby(['YEAR','MONTH','UN','torniquete_mariposa','no_torniquete']).agg(f)
				grouped_df.columns = grouped_df.columns.droplevel(1)
				grouped_df.reset_index(inplace=True,level=['torniquete_mariposa','no_torniquete'])
				months = grouped_df.groupby(['YEAR','MONTH','UN']).agg({'pn_SUM_EXP': 'sum'})
				grouped_df.loc[:,'ratio'] = grouped_df['pn_SUM_EXP'].div(months['pn_SUM_EXP'], axis='index') * 100














def monthly_pn_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	monthly_pn_grouped_database = pd.DataFrame()

	for year in years:
		print('Year ' + str(year) + ' is being analyzed')
		path = os.path.join(DTPM_TRXDir,'un_ppu_sersen_sumtrx_' + str(year) + '_by_date.csv')
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', usecols=[0,1,2,3,4,5], parse_dates=[3])
		df.columns = ['UN','PPU','SER_SEN','DATE','SUM_TRX','COUNT']
		print('Number of observations before merge info. of turnstile is: ' + str(len(df.index)))
		
		df = df.merge(ana_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida', how='left', suffixes=('','_ana'))
		df = df.merge(mauricio_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida' , suffixes=('_ana', '_mauricio'), how='left')
		print('Number of observations after merge info. of turnstile is: ' + str(len(df.index)))
		
		torniquetes_mariposa_conditions = (df.loc[:,'fecha_instalacion_ana'].dt.date<df.loc[:,'DATE'].dt.date)
		df.loc[:,'min_fecha'] = pd.concat([df['fecha_instalacion_ana'], df['fecha_instalacion_mauricio']], axis=1).min(axis=1)
		no_torniquetes_conditions = (((df.loc[:,'fecha_instalacion_ana'].isnull()) & (df.loc[:,'fecha_instalacion_mauricio'].isnull())) | (df.loc[:,'DATE'].dt.date<=df['min_fecha'].dt.date))
		df.loc[:,'torniquete_mariposa'] = np.where(torniquetes_mariposa_conditions,1,0)
		df.loc[:,'no_torniquete'] = np.where(no_torniquetes_conditions,1,0)

		df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year     
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month

		f = {'SUM_TRX':
			 {'pn_SUM_TRX':['sum']},
			 'COUNT':
			 {'pn_SUM_EXP':['sum']}}

		grouped_df = df.groupby(['YEAR','MONTH','torniquete_mariposa','no_torniquete']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		grouped_df.reset_index(inplace=True,level=['torniquete_mariposa','no_torniquete'])
		months = grouped_df.groupby(['YEAR','MONTH']).agg({'pn_SUM_EXP': 'sum'})
		grouped_df.loc[:,'ratio'] = grouped_df['pn_SUM_EXP'].div(months['pn_SUM_EXP'], axis='index') * 100

		monthly_pn_grouped_database = pd.concat([monthly_pn_grouped_database,grouped_df])
	
	return monthly_pn_grouped_database

def monthly_zp_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	monthly_zp_grouped_database = pd.DataFrame()
	for year in years:
		path = os.path.join(DTPM_TRXDir,'trxzp_' + str(year))
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', parse_dates=[2])
		df.columns = ['UN','RMZP','DATE','TIPODIA','MHORA','PERIODO','TRX_VALIDAS','TARJETAS_NO_VALIDAS','TRX_NO_VALIDAS']
		print('Number of observations is: ' + str(len(df.index)))
		
		df.loc[:,'YEAR'] = df.loc[:,'YEAR'].dt.year     
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month

		f = {'TRX_VALIDAS':
			 {'zp_SUM_TRX':['sum']},
			'TRX_NO_VALIDAS':
			{'zp_SUM_TRX_NO_VALIDAS':['sum']}}
		
		grouped_df = df.groupby(['YEAR','MONTH']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		monthly_zp_grouped_database = pd.concat([monthly_zp_grouped_database,grouped_df])

	return monthly_zp_grouped_database

def monthly_un_pn_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	monthly_un_pn_grouped_database = pd.DataFrame()

	for year in years:
		print('Year ' + str(year) + ' is being analyzed')
		path = os.path.join(DTPM_TRXDir,'un_ppu_sersen_sumtrx_' + str(year) + '_by_date.csv')
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', usecols=[0,1,2,3,4,5], parse_dates=[3])
		df.columns = ['UN','PPU','SER_SEN','DATE','SUM_TRX','COUNT']
		print('Number of observations before merge info. of turnstile is: ' + str(len(df.index)))
		
		df = df.merge(ana_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida', how='left', suffixes=('','_ana'))
		df = df.merge(mauricio_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida' , suffixes=('_ana', '_mauricio'), how='left')
		print('Number of observations after merge info. of turnstile is: ' + str(len(df.index)))
		
		torniquetes_mariposa_conditions = (df.loc[:,'fecha_instalacion_ana'].dt.date<df.loc[:,'DATE'].dt.date)
		df.loc[:,'min_fecha'] = pd.concat([df['fecha_instalacion_ana'], df['fecha_instalacion_mauricio']], axis=1).min(axis=1)
		no_torniquetes_conditions = (((df.loc[:,'fecha_instalacion_ana'].isnull()) & (df.loc[:,'fecha_instalacion_mauricio'].isnull())) | (df.loc[:,'DATE'].dt.date<=df['min_fecha'].dt.date))
		df.loc[:,'torniquete_mariposa'] = np.where(torniquetes_mariposa_conditions,1,0)
		df.loc[:,'no_torniquete'] = np.where(no_torniquetes_conditions,1,0)

		df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year     
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month

		f = {'SUM_TRX':
			 {'pn_SUM_TRX':['sum']},
			 'COUNT':
			 {'pn_SUM_EXP':['sum']}}

		grouped_df = df.groupby(['YEAR','MONTH','UN','torniquete_mariposa','no_torniquete']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		grouped_df.reset_index(inplace=True,level=['torniquete_mariposa','no_torniquete'])
		months = grouped_df.groupby(['YEAR','MONTH','UN']).agg({'pn_SUM_EXP': 'sum'})
		grouped_df.loc[:,'ratio'] = grouped_df['pn_SUM_EXP'].div(months['pn_SUM_EXP'], axis='index') * 100

		monthly_un_pn_grouped_database = pd.concat([monthly_un_pn_grouped_database,grouped_df])
	
	return monthly_un_pn_grouped_database

def monthly_un_zp_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	monthly_un_zp_grouped_database = pd.DataFrame()
	for year in years:
		path = os.path.join(DTPM_TRXDir,'trxzp_' + str(year))
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', parse_dates=[2])
		df.columns = ['UN','RMZP','DATE','TIPODIA','MHORA','PERIODO','TRX_VALIDAS','TARJETAS_NO_VALIDAS','TRX_NO_VALIDAS']
		print('Number of observations is: ' + str(len(df.index)))

		df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year     
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month

		f = {'TRX_VALIDAS':
			 {'zp_SUM_TRX':['sum']},
			'TRX_NO_VALIDAS':
			{'zp_SUM_TRX_NO_VALIDAS':['sum']}}
		
		grouped_df = df.groupby(['YEAR','MONTH','UN']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		monthly_un_zp_grouped_database = pd.concat([monthly_un_zp_grouped_database,grouped_df])

	return monthly_un_zp_grouped_database

def daily_pn_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	daily_pn_grouped_database = pd.DataFrame()

	for year in years:
		print('Year ' + str(year) + ' is being analyzed')
		path = os.path.join(DTPM_TRXDir,'un_ppu_sersen_sumtrx_' + str(year) + '_by_date.csv')
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', usecols=[0,1,2,3,4,5], parse_dates=[3])
		df.columns = ['UN','PPU','SER_SEN','DATE','SUM_TRX','COUNT']
		print('Number of observations before merge info. of turnstile is: ' + str(len(df.index)))
		
		df = df.merge(ana_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida', how='left', suffixes=('','_ana'))
		df = df.merge(mauricio_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida' , suffixes=('_ana', '_mauricio'), how='left')
		print('Number of observations after merge info. of turnstile is: ' + str(len(df.index)))
		
		torniquetes_mariposa_conditions = (df.loc[:,'fecha_instalacion_ana'].dt.date<df.loc[:,'DATE'].dt.date)
		df.loc[:,'min_fecha'] = pd.concat([df['fecha_instalacion_ana'], df['fecha_instalacion_mauricio']], axis=1).min(axis=1)
		no_torniquetes_conditions = (((df.loc[:,'fecha_instalacion_ana'].isnull()) & (df.loc[:,'fecha_instalacion_mauricio'].isnull())) | (df.loc[:,'DATE'].dt.date<=df['min_fecha'].dt.date))
		df.loc[:,'torniquete_mariposa'] = np.where(torniquetes_mariposa_conditions,1,0)
		df.loc[:,'no_torniquete'] = np.where(no_torniquetes_conditions,1,0)

		new_year_day = dt.date(year=year, month=1, day=1)
		df.loc[:,'YEAR_DAY'] = df.loc[:,'DATE'].apply(lambda x: (x.date() - new_year_day).days + 1)
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month
		df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year
		
		f = {'SUM_TRX':
			 {'pn_SUM_TRX':['sum']},
			 'COUNT':
			 {'pn_SUM_EXP':['sum']}}
		
		grouped_df = df.groupby(['YEAR','MONTH','YEAR_DAY','DATE','torniquete_mariposa','no_torniquete']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		grouped_df.reset_index(inplace=True,level=['MONTH','DATE','torniquete_mariposa','no_torniquete'])
		days = grouped_df.groupby(['YEAR','YEAR_DAY']).agg({'pn_SUM_EXP': 'sum'})
		grouped_df.loc[:,'ratio'] = grouped_df['pn_SUM_EXP'].div(days['pn_SUM_EXP'],axis='index') * 100
		
		daily_pn_grouped_database = pd.concat([daily_pn_grouped_database,grouped_df])
		
	return daily_pn_grouped_database

def daily_zp_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	daily_zp_grouped_database = pd.DataFrame()
	for year in years:
		path = os.path.join(DTPM_TRXDir,'trxzp_' + str(year))
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', parse_dates=[2])
		df.columns = ['UN','RMZP','DATE','TIPODIA','MHORA','PERIODO','TRX_VALIDAS','TARJETAS_NO_VALIDAS','TRX_NO_VALIDAS']
		print('Number of observations is: ' + str(len(df.index)))
		
		new_year_day = dt.date(year=year, month=1, day=1)
		df.loc[:,'YEAR_DAY'] = df.loc[:,'DATE'].apply(lambda x: (x.date() - new_year_day).days + 1)    
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month
		df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year
		
		f = {'TRX_VALIDAS':
			 {'zp_SUM_TRX':['sum']},
			'TRX_NO_VALIDAS':
			{'zp_SUM_TRX_NO_VALIDAS':['sum']}}
		
		grouped_df = df.groupby(['YEAR','MONTH','YEAR_DAY','DATE']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		daily_zp_grouped_database = pd.concat([daily_zp_grouped_database,grouped_df])

	return daily_zp_grouped_database

def daily_un_pn_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	daily_un_pn_grouped_database = pd.DataFrame()

	for year in years:
		print('Year ' + str(year) + ' is being analyzed')
		path = os.path.join(DTPM_TRXDir,'un_ppu_sersen_sumtrx_' + str(year) + '_by_date.csv')
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', usecols=[0,1,2,3,4,5], parse_dates=[3])
		df.columns = ['UN','PPU','SER_SEN','DATE','SUM_TRX','COUNT']
		print('Number of observations before merge info. of turnstile is: ' + str(len(df.index)))
		
		df = df.merge(ana_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida', how='left', suffixes=('','_ana'))
		df = df.merge(mauricio_turnstiles_df, left_on = 'PPU', right_on = 'sitio_subida' , suffixes=('_ana', '_mauricio'), how='left')
		print('Number of observations after merge info. of turnstile is: ' + str(len(df.index)))
		
		torniquetes_mariposa_conditions = (df.loc[:,'fecha_instalacion_ana'].dt.date<df.loc[:,'DATE'].dt.date)
		df.loc[:,'min_fecha'] = pd.concat([df['fecha_instalacion_ana'], df['fecha_instalacion_mauricio']], axis=1).min(axis=1)
		no_torniquetes_conditions = (((df.loc[:,'fecha_instalacion_ana'].isnull()) & (df.loc[:,'fecha_instalacion_mauricio'].isnull())) | (df.loc[:,'DATE'].dt.date<=df['min_fecha'].dt.date))
		df.loc[:,'torniquete_mariposa'] = np.where(torniquetes_mariposa_conditions,1,0)
		df.loc[:,'no_torniquete'] = np.where(no_torniquetes_conditions,1,0)

		new_year_day = dt.date(year=year, month=1, day=1)
		df.loc[:,'YEAR_DAY'] = df.loc[:,'DATE'].apply(lambda x: (x.date() - new_year_day).days + 1)
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month
		df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year

		f = {'SUM_TRX':
			 {'pn_SUM_TRX':['sum']},
			 'COUNT':
			 {'pn_SUM_EXP':['sum']}}
		
		grouped_df = df.groupby(['YEAR','MONTH','YEAR_DAY','DATE','UN','torniquete_mariposa','no_torniquete']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		grouped_df.reset_index(inplace=True,level=['MONTH','DATE','torniquete_mariposa','no_torniquete'])
		days = grouped_df.groupby(['YEAR','YEAR_DAY','UN']).agg({'pn_SUM_EXP': 'sum'})
		grouped_df.loc[:,'ratio'] = grouped_df['pn_SUM_EXP'].div(days['pn_SUM_EXP'],axis='index') * 100
		
		daily_un_pn_grouped_database = pd.concat([daily_un_pn_grouped_database,grouped_df])
		
	return daily_un_pn_grouped_database

def daily_un_zp_grouping(ana_turnstiles_df,mauricio_turnstiles_df):
	years = [2015,2016,2017]
	daily_zp_grouped_database = pd.DataFrame()
	for year in years:
		path = os.path.join(DTPM_TRXDir,'trxzp_' + str(year))
		df = pd.read_csv(path, sep=";", header=None, encoding='latin-1', parse_dates=[2])
		df.columns = ['UN','RMZP','DATE','TIPODIA','MHORA','PERIODO','TRX_VALIDAS','TARJETAS_NO_VALIDAS','TRX_NO_VALIDAS']
		print('Number of observations is: ' + str(len(df.index)))
		
		new_year_day = dt.date(year=year, month=1, day=1)
		df.loc[:,'YEAR_DAY'] = df.loc[:,'DATE'].apply(lambda x: (x.date() - new_year_day).days + 1)    
		df.loc[:,'MONTH'] = df.loc[:,'DATE'].dt.month
		df.loc[:,'YEAR'] = df.loc[:,'DATE'].dt.year
		
		f = {'TRX_VALIDAS':
			 {'zp_SUM_TRX':['sum']},
			'TRX_NO_VALIDAS':
			{'zp_SUM_TRX_NO_VALIDAS':['sum']}}
		
		grouped_df = df.groupby(['YEAR','MONTH','YEAR_DAY','DATE','UN']).agg(f)
		grouped_df.columns = grouped_df.columns.droplevel(1)
		daily_zp_grouped_database = pd.concat([daily_zp_grouped_database,grouped_df])

	return daily_zp_grouped_database
