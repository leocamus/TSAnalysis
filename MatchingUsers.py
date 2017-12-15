import pandas as pd

def simplifyingEvasionAndEtapas(common_dates_evasion, date):
	#First filtering by date.
	evasion_by_date = common_dates_evasion[common_dates_evasion['FECHA']==pd.to_datetime(date)]
	#Then getting the info.
	patentes_by_date = evasion_by_date['PATENTE'].unique()
	patentes_by_date = patentes_by_date.tolist()
	servicios_by_date = evasion_by_date['SERVICIO'].unique()
	servicios_by_date = servicios_by_date.tolist()
	#Then returning
	return evasion_by_date, patentes_by_date, servicios_by_date

def appendingIdExpedicion(clean_sorted_df):
	past_servicio = ''
	past_patente = ''
	past_time = pd.to_datetime('')
	id_exp = 1
	clean_sorted_df['idExpedicion'] = ''

	for index,row in clean_sorted_df.iterrows():
		actual_servicio = row['servicio_subida']
		actual_patente = row['sitio_subida']
		actual_time = row['t_subida']

	if((past_servicio==actual_servicio)&(actual_time - past_time <= pd.Timedelta('15 minutes'))):
		clean_sorted_df.loc[index,'idExpedicion'] = id_exp

	elif((past_servicio==actual_servicio)&(actual_time - past_time > pd.Timedelta('15 minutes'))):
		id_exp = id_exp + 1
		clean_sorted_df.loc[index,'idExpedicion'] = id_exp

	elif((past_servicio!=actual_servicio)):
		id_exp = 1
		clean_sorted_df.loc[index,'idExpedicion'] = id_exp

	past_servicio = actual_servicio
	past_patente = actual_patente
	past_time = actual_time

	return clean_sorted_df

def groupByEtapasDatabase(clean_sorted_df):
	f = {'t_subida':['min', 'max', 'count'], 'diferencia_tiempo_secs':['mean']}
	grouped_clean_sorted_df = clean_sorted_df.groupby(['sitio_subida','servicio_subida','idExpedicion','par_subida']).agg(f)
	grouped_clean_sorted_df = grouped_clean_sorted_df.reset_index()
	grouped_clean_sorted_df.columns = [''.join(col).strip() for col in grouped_clean_sorted_df.columns.values]
	grouped_clean_sorted_df = grouped_clean_sorted_df.sort_values(by=['sitio_subida', 'servicio_subida', 'idExpedicion', 't_subidamin'], ascending=[True, True, True, True])
	grouped_clean_sorted_df = grouped_clean_sorted_df.reset_index(drop=True)

	return grouped_clean_sorted_df

def appendingStartEndCuts(grouped_clean_sorted_df):
	past_plate = ''
	past_service = ''
	past_par_subida = ['']
	past_initial_hour = ''
	past_end_hour = ''
	past_id_expedicion = ''

	grouped_clean_sorted_df['start_cut']=''
	grouped_clean_sorted_df['end_cut']=''

	for index,row in grouped_clean_sorted_df.iterrows():
		future_index = index+1

		actual_plate = row['sitio_subida']
		actual_service = row['servicio_subida']
		actual_initial_hour = row['t_subidamin']
		actual_end_hour = row['t_subidamax']

		actual_id_expedicion = row['idExpedicion']

		if ((actual_plate!=past_plate)|(actual_service!=past_service)|(actual_id_expedicion!=past_id_expedicion)): #Assuming a pre-defined value, i.e., 30 seconds.
			start_cut = actual_initial_hour - (pd.Timedelta('30 seconds'))
		else:
			start_cut = actual_initial_hour - (actual_initial_hour - past_end_hour)/2

		if future_index >= len(grouped_clean_sorted_df.index): #We are at the end of the ddff. Assuming a pre-defined value, i.e., 30 seconds 
			end_cut = actual_end_hour + (pd.Timedelta('30 seconds'))
		else:        
			future_plate = grouped_clean_sorted_df.loc[future_index,'sitio_subida']
			future_service = grouped_clean_sorted_df.loc[future_index,'servicio_subida']
			future_initial_hour = grouped_clean_sorted_df.loc[future_index,'t_subidamin']
			future_end_hour = grouped_clean_sorted_df.loc[future_index,'t_subidamax']
			future_id_expedicion = grouped_clean_sorted_df.loc[future_index,'idExpedicion']
			if ((actual_plate!=future_plate)|(actual_service!=future_service)|(actual_id_expedicion!=future_id_expedicion)): #Changing service or plate... assuming a pre-defined value, i.e., 30 seconds
				end_cut = actual_end_hour + (pd.Timedelta('30 seconds'))
			else:
				end_cut = actual_end_hour + (future_initial_hour - actual_end_hour)/2

		past_initial_hour = actual_initial_hour
		past_end_hour = actual_end_hour
		past_id_expedicion = actual_id_expedicion
		past_plate = actual_plate
		past_service = actual_service
		grouped_clean_sorted_df.loc[index,'start_cut']=start_cut
		grouped_clean_sorted_df.loc[index,'end_cut']=end_cut

	return grouped_clean_sorted_df
    
def slicingEvasionDatabase(grouped_clean_sorted_df, evasion_by_date):

	for index,row in grouped_clean_sorted_df.iterrows():
		actual_plate = row['sitio_subida']
		actual_service = row['servicio_subida']
		start_cut = row['start_cut']
		end_cut = row['end_cut']

		actual_util_df = evasion_by_date[(evasion_by_date['PATENTE']==actual_plate)&(evasion_by_date['SERVICIO']==actual_service)&(start_cut<=evasion_by_date['TIEMPO'])&(evasion_by_date['TIEMPO']<=end_cut)]
		actual_util_df = actual_util_df[(actual_util_df['INGRESAN'] > actual_util_df['NO_VALIDAN'])] #Be aware of this condition
		actual_ev_obs = len(actual_util_df.index)

		grouped_clean_sorted_df.loc[index,'count_ev_obs'] = actual_ev_obs
		grouped_clean_sorted_df.loc[index,'ingresan'] = actual_util_df['INGRESAN'].sum()
		grouped_clean_sorted_df.loc[index,'no_validan'] = actual_util_df['NO_VALIDAN'].sum()

	return grouped_clean_sorted_df