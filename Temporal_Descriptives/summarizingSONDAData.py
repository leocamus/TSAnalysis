from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants

import pandas as pd
import numpy as np
import os
import datetime as dt

DTPM_TRXDir = TransantiagoConstants.DTPM_TRXDir

def reOrderingDataFrame(how_to):

	summary = pd.DataFrame()

	if(how_to=='by month'):

		pn_input_path = os.path.join(DTPM_TRXDir, '1_MONTHLY/monthly_pn.csv')
		zp_input_path = os.path.join(DTPM_TRXDir, '1_MONTHLY/monthly_zp.csv')

		pn_summary = pd.read_csv(pn_input_path, sep=';', encoding = 'latin-1', index_col = 0)
		zp_summary = pd.read_csv(zp_input_path, sep=';', encoding = 'latin-1', index_col = 0)
	
		no_turnstile = pn_summary.loc[(pn_summary['torniquete_mariposa']==0)&(pn_summary['no_torniquete']==1),:]
		three_turnstile = pn_summary.loc[(pn_summary['torniquete_mariposa']==0)&(pn_summary['no_torniquete']==0),:]
		butterfly_turnstile = pn_summary.loc[(pn_summary['torniquete_mariposa']==1)&(pn_summary['no_torniquete']==0),:]
	
		summary = no_turnstile.loc[:,['YEAR','MONTH','pn_SUM_TRX','pn_SUM_EXP','ratio']]
		#First merge...
		three_turnstile = three_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH']], how='outer', on = ['YEAR','MONTH'])
		three_turnstile = three_turnstile.fillna(0)
		summary = summary.merge(three_turnstile.loc[:,['YEAR','MONTH','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH'], suffixes=('_no_t','_3t'))
	
		#Second merge...
		butterfly_turnstile = butterfly_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH']], how='outer', on = ['YEAR','MONTH'])
		butterfly_turnstile = butterfly_turnstile.fillna(0)
		summary = summary.merge(butterfly_turnstile.loc[:,['YEAR','MONTH','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH'])
	
		#Third merge...
		zp_summary = zp_summary.merge(no_turnstile.loc[:,['YEAR','MONTH']], how='outer', on = ['YEAR','MONTH'])
		zp_summary = zp_summary.fillna(0)
		summary = summary.merge(zp_summary.loc[:,['YEAR','MONTH','zp_SUM_TRX','zp_SUM_TRX_NO_VALIDAS']], how='left', on=['YEAR','MONTH'])
	
		#Renaming and final sorting...
		summary.rename(columns={"pn_SUM_TRX": "pn_SUM_TRX_tm", "pn_SUM_EXP": "pn_SUM_EXP_tm", "ratio":"ratio_tm"}, inplace=True)
		summary.sort_values(by=['YEAR','MONTH'], ascending=[True, True], inplace=True)

		output_path = os.path.join(DTPM_TRXDir,'1_MONTHLY/monthly_summary.csv')
		summary.to_csv(output_path,sep=';',encoding='latin-1')

	elif(how_to=='by day'):

		pn_input_path = os.path.join(DTPM_TRXDir, '3_DAILY/daily_pn.csv')
		zp_input_path = os.path.join(DTPM_TRXDir, '3_DAILY/daily_zp.csv')

		pn_summary = pd.read_csv(pn_input_path, sep=';', encoding = 'latin-1', index_col = 0)
		zp_summary = pd.read_csv(zp_input_path, sep=';', encoding = 'latin-1', index_col = 0)	

		no_turnstile = pn_summary.loc[(pn_summary['torniquete_mariposa']==0)&(pn_summary['no_torniquete']==1),:]
		three_turnstile = pn_summary.loc[(pn_summary['torniquete_mariposa']==0)&(pn_summary['no_torniquete']==0),:]
		butterfly_turnstile = pn_summary.loc[(pn_summary['torniquete_mariposa']==1)&(pn_summary['no_torniquete']==0),:]
	
		summary = no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','pn_SUM_TRX','pn_SUM_EXP','ratio']]
		#First merge...
		three_turnstile = three_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY']], how='outer', on = ['YEAR','MONTH','YEAR_DAY'])
		three_turnstile = three_turnstile.fillna(0)
		summary = summary.merge(three_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','YEAR_DAY'], suffixes=('_no_t','_3t'))
	
		#Second merge...
		butterfly_turnstile = butterfly_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY']], how='outer', on = ['YEAR','MONTH','YEAR_DAY'])
		butterfly_turnstile = butterfly_turnstile.fillna(0)
		summary = summary.merge(butterfly_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','YEAR_DAY'])
	
		#Third merge...
		zp_summary = zp_summary.merge(no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY']], how='outer', on = ['YEAR','MONTH','YEAR_DAY'])
		zp_summary = zp_summary.fillna(0)
		summary = summary.merge(zp_summary.loc[:,['YEAR','MONTH','YEAR_DAY','zp_SUM_TRX','zp_SUM_TRX_NO_VALIDAS']], how='left', on=['YEAR','MONTH','YEAR_DAY'])
	
		#Renaming and final sorting...
		summary.rename(columns={"pn_SUM_TRX": "pn_SUM_TRX_tm", "pn_SUM_EXP": "pn_SUM_EXP_tm", "ratio":"ratio_tm"}, inplace=True)
		summary.sort_values(by=['YEAR','MONTH','YEAR_DAY'], ascending=[True, True, True], inplace=True)

		output_path = os.path.join(DTPM_TRXDir,'3_DAILY/daily_summary.csv')
		summary.to_csv(output_path,sep=';',encoding='latin-1')


def reOrderingDataFrameByUN(how_to):

	unidades = ['U1','U2','U3','U4','U5','U6','U7']

	if (how_to == 'by month by un'):
		pn_input_path = os.path.join(DTPM_TRXDir, '2_MONTHLY_UN/monthly_un_pn.csv')
		zp_input_path = os.path.join(DTPM_TRXDir, '2_MONTHLY_UN/monthly_un_zp.csv')

		pn_summary = pd.read_csv(pn_input_path, sep=';', encoding = 'latin-1', index_col = 0)
		zp_summary = pd.read_csv(zp_input_path, sep=';', encoding = 'latin-1', index_col = 0)

		for unidad in unidades:
			
			summary = pd.DataFrame()
			pn_summary_un = pn_summary.loc[pn_summary['UN']==unidad,:]
			zp_summary_un = zp_summary.loc[zp_summary['UN']==unidad,:]
		
			no_turnstile = pn_summary_un.loc[(pn_summary_un['torniquete_mariposa']==0)&(pn_summary_un['no_torniquete']==1),:]
			three_turnstile = pn_summary_un.loc[(pn_summary_un['torniquete_mariposa']==0)&(pn_summary_un['no_torniquete']==0),:]
			butterfly_turnstile = pn_summary_un.loc[(pn_summary_un['torniquete_mariposa']==1)&(pn_summary_un['no_torniquete']==0),:]

			if (unidad!='U2'):
				summary = no_turnstile.loc[:,['YEAR','MONTH','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']]
				#First merge...
				three_turnstile = three_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH','UN']], how='outer', on = ['YEAR','MONTH','UN'])
				three_turnstile = three_turnstile.fillna(0)
				summary = summary.merge(three_turnstile.loc[:,['YEAR','MONTH','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','UN'], suffixes=('_no_t','_3t'))
			
				#Second merge...
				butterfly_turnstile = butterfly_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH','UN']], how='outer', on = ['YEAR','MONTH','UN'])
				butterfly_turnstile = butterfly_turnstile.fillna(0)
				summary = summary.merge(butterfly_turnstile.loc[:,['YEAR','MONTH','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','UN'])
			
				#Third merge...
				zp_summary = zp_summary.merge(no_turnstile.loc[:,['YEAR','MONTH','UN']], how='outer', on = ['YEAR','MONTH','UN'])
				zp_summary = zp_summary.fillna(0)
				summary = summary.merge(zp_summary.loc[:,['YEAR','MONTH','UN','zp_SUM_TRX','zp_SUM_TRX_NO_VALIDAS']], how='left', on=['YEAR','MONTH','UN'])
			
				#Renaming and final sorting...
				summary.rename(columns={"pn_SUM_TRX": "pn_SUM_TRX_tm", "pn_SUM_EXP": "pn_SUM_EXP_tm", "ratio":"ratio_tm"}, inplace=True)
				summary.sort_values(by=['YEAR','MONTH'], ascending=[True, True], inplace=True)
			else:
				summary = three_turnstile.loc[:,['YEAR','MONTH','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']]
				#First merge...
				no_turnstile = no_turnstile.merge(three_turnstile.loc[:,['YEAR','MONTH','UN']], how='outer', on = ['YEAR','MONTH','UN'])
				no_turnstile = no_turnstile.fillna(0)
				summary = summary.merge(no_turnstile.loc[:,['YEAR','MONTH','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','UN'], suffixes=('_3t','_no_t'))
				
				#Second merge...
				butterfly_turnstile = butterfly_turnstile.merge(three_turnstile.loc[:,['YEAR','MONTH','UN']], how='outer', on = ['YEAR','MONTH','UN'])
				butterfly_turnstile = butterfly_turnstile.fillna(0)
				summary = summary.merge(butterfly_turnstile.loc[:,['YEAR','MONTH','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','UN'])
				
				#Third merge...
				zp_summary = zp_summary.merge(three_turnstile.loc[:,['YEAR','MONTH','UN']], how='outer', on = ['YEAR','MONTH','UN'])
				zp_summary = zp_summary.fillna(0)
				summary = summary.merge(zp_summary.loc[:,['YEAR','MONTH','UN','zp_SUM_TRX','zp_SUM_TRX_NO_VALIDAS']], how='left', on=['YEAR','MONTH','UN'])

				#Renaming and final sorting...
				summary.rename(columns={"pn_SUM_TRX": "pn_SUM_TRX_tm", "pn_SUM_EXP": "pn_SUM_EXP_tm", "ratio":"ratio_tm"}, inplace=True)
				summary.sort_values(by=['YEAR','MONTH'], ascending=[True, True], inplace=True)

			output_path = os.path.join(DTPM_TRXDir,'2_MONTHLY_UN/' + unidad + '/' + unidad + '_summary.csv')
			summary.to_csv(output_path,sep=';',encoding='latin-1')

	elif (how_to == 'by day by un'):
		pn_input_path = os.path.join(DTPM_TRXDir, '4_DAILY_UN/daily_un_pn.csv')
		zp_input_path = os.path.join(DTPM_TRXDir, '4_DAILY_UN/daily_un_zp.csv')

		pn_summary = pd.read_csv(pn_input_path, sep=';', encoding = 'latin-1', index_col = 0)
		zp_summary = pd.read_csv(zp_input_path, sep=';', encoding = 'latin-1', index_col = 0)

		for unidad in unidades:

			summary = pd.DataFrame()
			pn_summary_un = pn_summary.loc[pn_summary['UN']==unidad,:]
			zp_summary_un = zp_summary.loc[zp_summary['UN']==unidad,:]
		
			no_turnstile = pn_summary_un.loc[(pn_summary_un['torniquete_mariposa']==0)&(pn_summary_un['no_torniquete']==1),:]
			three_turnstile = pn_summary_un.loc[(pn_summary_un['torniquete_mariposa']==0)&(pn_summary_un['no_torniquete']==0),:]
			butterfly_turnstile = pn_summary_un.loc[(pn_summary_un['torniquete_mariposa']==1)&(pn_summary_un['no_torniquete']==0),:]

			if (unidad!='U2'):
				summary = no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']]
				#First merge...
				three_turnstile = three_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN']], how='outer', on = ['YEAR','MONTH','YEAR_DAY','UN'])
				three_turnstile = three_turnstile.fillna(0)
				summary = summary.merge(three_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','YEAR_DAY','UN'], suffixes=('_no_t','_3t'))
			
				#Second merge...
				butterfly_turnstile = butterfly_turnstile.merge(no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN']], how='outer', on = ['YEAR','MONTH','YEAR_DAY','UN'])
				butterfly_turnstile = butterfly_turnstile.fillna(0)
				summary = summary.merge(butterfly_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','YEAR_DAY','UN'])
			
				#Third merge...
				zp_summary = zp_summary.merge(no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN']], how='outer', on = ['YEAR','MONTH','YEAR_DAY','UN'])
				zp_summary = zp_summary.fillna(0)
				summary = summary.merge(zp_summary.loc[:,['YEAR','MONTH','YEAR_DAY','UN','zp_SUM_TRX','zp_SUM_TRX_NO_VALIDAS']], how='left', on=['YEAR','MONTH','YEAR_DAY','UN'])
			
				#Renaming and final sorting...
				summary.rename(columns={"pn_SUM_TRX": "pn_SUM_TRX_tm", "pn_SUM_EXP": "pn_SUM_EXP_tm", "ratio":"ratio_tm"}, inplace=True)
				summary.sort_values(by=['YEAR','MONTH','YEAR_DAY'], ascending=[True, True, True], inplace=True)
			else:
				summary = three_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']]
				#First merge...
				no_turnstile = no_turnstile.merge(three_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN']], how='outer', on = ['YEAR','MONTH','YEAR_DAY','UN'])
				no_turnstile = no_turnstile.fillna(0)
				summary = summary.merge(no_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','YEAR_DAY','UN'], suffixes=('_3t','_no_t'))
				
				#Second merge...
				butterfly_turnstile = butterfly_turnstile.merge(three_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN']], how='outer', on = ['YEAR','MONTH','YEAR_DAY','UN'])
				butterfly_turnstile = butterfly_turnstile.fillna(0)
				summary = summary.merge(butterfly_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN','pn_SUM_TRX','pn_SUM_EXP','ratio']], how='left', on=['YEAR','MONTH','YEAR_DAY','UN'])
				
				#Third merge...
				zp_summary = zp_summary.merge(three_turnstile.loc[:,['YEAR','MONTH','YEAR_DAY','UN']], how='outer', on = ['YEAR','MONTH','YEAR_DAY','UN'])
				zp_summary = zp_summary.fillna(0)
				summary = summary.merge(zp_summary.loc[:,['YEAR','MONTH','YEAR_DAY','UN','zp_SUM_TRX','zp_SUM_TRX_NO_VALIDAS']], how='left', on=['YEAR','MONTH','YEAR_DAY','UN'])

				#Renaming and final sorting...
				summary.rename(columns={"pn_SUM_TRX": "pn_SUM_TRX_tm", "pn_SUM_EXP": "pn_SUM_EXP_tm", "ratio":"ratio_tm"}, inplace=True)
				summary.sort_values(by=['YEAR','MONTH','YEAR_DAY'], ascending=[True, True, True], inplace=True)

			output_path = os.path.join(DTPM_TRXDir,'4_DAILY_UN/' + unidad + '/' + unidad + '_summary.csv')
			summary.to_csv(output_path,sep=';',encoding='latin-1')