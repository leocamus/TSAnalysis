import pandas as pd

def getTrxByServiceAndPeriodInTime(clean_working_sumtrx,servicio, periodo):

	TORNIQUETE = clean_working_sumtrx.loc[(clean_working_sumtrx['servicio_subida'].str.contains(servicio))&(clean_working_sumtrx['PERIODO']==periodo)&(clean_working_sumtrx['torniquete_mariposa']==1),:]
	SIN_TORNIQUETE = clean_working_sumtrx.loc[(clean_working_sumtrx['servicio_subida'].str.contains(servicio))&(clean_working_sumtrx['PERIODO']==periodo)&(clean_working_sumtrx['no_torniquete']==1),:]
	OTROS = clean_working_sumtrx.loc[(clean_working_sumtrx['servicio_subida'].str.contains(servicio))&(clean_working_sumtrx['PERIODO']==periodo)&(clean_working_sumtrx['no_torniquete']==0)&(clean_working_sumtrx['torniquete_mariposa']==0),:]
	
	grouped_TORNIQUETE = TORNIQUETE.groupby(TORNIQUETE['fecha'])['id_count'].sum()
	grouped_SIN_TORNIQUETE = SIN_TORNIQUETE.groupby(SIN_TORNIQUETE['fecha'])['id_count'].sum()
	grouped_OTROS = OTROS.groupby(OTROS['fecha'])['id_count'].sum()    
	
	if(len(grouped_TORNIQUETE.index)<len(grouped_SIN_TORNIQUETE.index)):
		missing_indexes_con_vs_sin = set(grouped_SIN_TORNIQUETE.index) - (set(grouped_SIN_TORNIQUETE.index) & set(grouped_TORNIQUETE.index))
		for time in missing_indexes_con_vs_sin:
			grouped_TORNIQUETE.at[time] = 0
			
	if(len(grouped_OTROS.index)<len(grouped_SIN_TORNIQUETE.index)):
		missing_indexes_con_vs_tres = set(grouped_SIN_TORNIQUETE.index) - (set(grouped_SIN_TORNIQUETE.index) & set(grouped_OTROS.index))
		for time in missing_indexes_con_vs_tres:
			grouped_OTROS.at[time] = 0
			
	grouped_TORNIQUETE.sort_index(ascending = True, inplace = True)
	grouped_SIN_TORNIQUETE.sort_index(ascending = True, inplace = True)
	grouped_OTROS.sort_index(ascending = True, inplace = True)
	
	return grouped_SIN_TORNIQUETE,grouped_TORNIQUETE,grouped_OTROS

def getTrxByServiceInTime(clean_working_sumtrx,servicio):
	TORNIQUETE = clean_working_sumtrx.loc[(clean_working_sumtrx['servicio_subida'].str.contains(servicio))&(clean_working_sumtrx['torniquete_mariposa']==1),:]
	SIN_TORNIQUETE = clean_working_sumtrx.loc[(clean_working_sumtrx['servicio_subida'].str.contains(servicio))&(clean_working_sumtrx['no_torniquete']==1),:]
	OTROS = clean_working_sumtrx.loc[(clean_working_sumtrx['servicio_subida'].str.contains(servicio))&(clean_working_sumtrx['no_torniquete']==0)&(clean_working_sumtrx['torniquete_mariposa']==0),:]
	
	grouped_TORNIQUETE = TORNIQUETE.groupby(TORNIQUETE['fecha'])['id_count'].sum()
	grouped_SIN_TORNIQUETE = SIN_TORNIQUETE.groupby(SIN_TORNIQUETE['fecha'])['id_count'].sum()
	grouped_OTROS = OTROS.groupby(OTROS['fecha'])['id_count'].sum()    
	
	if(len(grouped_TORNIQUETE.index)<len(grouped_SIN_TORNIQUETE.index)):
		missing_indexes_con_vs_sin = set(grouped_SIN_TORNIQUETE.index) - (set(grouped_SIN_TORNIQUETE.index) & set(grouped_TORNIQUETE.index))
		for time in missing_indexes_con_vs_sin:
			grouped_TORNIQUETE.at[time] = 0
			
	if(len(grouped_OTROS.index)<len(grouped_SIN_TORNIQUETE.index)):
		missing_indexes_con_vs_tres = set(grouped_SIN_TORNIQUETE.index) - (set(grouped_SIN_TORNIQUETE.index) & set(grouped_OTROS.index))
		for time in missing_indexes_con_vs_tres:
			grouped_OTROS.at[time] = 0
			
	grouped_TORNIQUETE.sort_index(ascending = True, inplace = True)
	grouped_SIN_TORNIQUETE.sort_index(ascending = True, inplace = True)
	grouped_OTROS.sort_index(ascending = True, inplace = True)
	
	return grouped_SIN_TORNIQUETE,grouped_TORNIQUETE,grouped_OTROS

def getTrxByUNInTime(clean_working_sumtrx,un):
	TORNIQUETE = clean_working_sumtrx.loc[(clean_working_sumtrx['UN_x']==un)&(clean_working_sumtrx['torniquete_mariposa']==1),:]
	SIN_TORNIQUETE = clean_working_sumtrx.loc[(clean_working_sumtrx['UN_x']==un)&(clean_working_sumtrx['no_torniquete']==1),:]
	OTROS = clean_working_sumtrx.loc[(clean_working_sumtrx['UN_x']==un)&(clean_working_sumtrx['torniquete_mariposa']==0)&(clean_working_sumtrx['no_torniquete']==0),:]    
	
	grouped_TORNIQUETE = TORNIQUETE.groupby(TORNIQUETE['fecha'])['id_count'].sum()
	grouped_SIN_TORNIQUETE = SIN_TORNIQUETE.groupby(SIN_TORNIQUETE['fecha'])['id_count'].sum()
	grouped_OTROS = OTROS.groupby(OTROS['fecha'])['id_count'].sum()

	if(un!=2):
		if(len(grouped_TORNIQUETE.index)<len(grouped_SIN_TORNIQUETE.index)):
			missing_indexes_con_vs_sin = set(grouped_SIN_TORNIQUETE.index) - (set(grouped_SIN_TORNIQUETE.index) & set(grouped_TORNIQUETE.index))
			for time in missing_indexes_con_vs_sin:
				grouped_TORNIQUETE.at[time] = 0

		if(len(grouped_OTROS.index)<len(grouped_SIN_TORNIQUETE.index)):
			missing_indexes_con_vs_tres = set(grouped_SIN_TORNIQUETE.index) - (set(grouped_SIN_TORNIQUETE.index) & set(grouped_OTROS.index))
			for time in missing_indexes_con_vs_tres:
				grouped_OTROS.at[time] = 0

	else:
		for time in set(grouped_OTROS.index):
			grouped_SIN_TORNIQUETE.at[time]=0

	grouped_TORNIQUETE.sort_index(ascending = True, inplace = True)
	grouped_SIN_TORNIQUETE.sort_index(ascending = True, inplace = True)
	grouped_OTROS.sort_index(ascending = True, inplace = True)

	return grouped_SIN_TORNIQUETE,grouped_TORNIQUETE,grouped_OTROS