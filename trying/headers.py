etapasHeaders= ['id','nviaje','netapa','tipo_dia','tipo_transporte','fExpansionServicioPeriodoTS','tiene_bajada','tiempo2','t_subida','t_bajada','t_etapa','media_hora_subida','media_hora_bajada','x_subida','y_subida','x_bajada','y_bajada','dist_ruta_paraderos','dist_eucl_paraderos','servicio_subida','servicio_bajada','par_subida','par_bajada','comuna_subida','comuna_bajada','zona_subida','zona_bajada','sitio_subida','fExpansionZonaPeriodoTS','tEsperaMediaIntervalo']
viajesHeaders=['id','nviaje','netapa','etapas','netapassinbajada','ultimaetapaconbajada','tviaje_seg','tviaje_min','dviajeeuclidiana_mts','dviajeenruta_mts','paraderosubida','paraderobajada','comunasubida','comunabajada','diseno777subida','diseno777bajada','tiemposubida','tiempobajada','periodosubida','periodobajada','tipodia','mediahora','contrato','factorexpansion','tiempomediodeviaje','periodomediodeviaje','mediahoramediodeviaje','tipodiamediodeviaje','t_1era_etapa','d_1era_etapa','tespera_1era_etapa','ttrasbordo_1era_etapa','tcaminata_1era_etapa','dtransbordo_1era_etapa','t_2da_etapa','d_2da_etapa','tespera_2da_etapa','ttrasbordo_2da_etapa','tcaminata_2da_etapa','dtransbordo_2da_etapa','t_3era_etapa','d_3era_etapa','tespera_3era_etapa','ttrasbordo_3era_etapa','tcaminata_3era_etapa','dtransbordo_3era_etapa','t_4ta_etapa','d_4ta_etapa','tespera_4ta_etapa','ttrasbordo_4ta_etapa','tcaminata_4ta_etapa','dtransbordo_4ta_etapa','op_1era_etapa','op_2da_etapa','op_3era_etapa','op_4ta_etapa','tipoop_1era_etapa','tipoop_2da_etapa','tipoop_3era_etapa','tipoop_4ta_etapa','serv_1era_etapa','serv_2da_etapa','serv_3era_etapa','serv_4ta_etapa','linea_metro_subida_1','linea_metro_subida_2','linea_metro_subida_3','linea_metro_subida_4','linea_metro_bajada_1','linea_metro_bajada_2','linea_metro_bajada_3','linea_metro_bajada_4','paraderosubida_1era','paraderosubida_2da','paraderosubida_3era','paraderosubida_4ta','tiemposubida_1era','tiemposubida_2da','tiemposubida_3era','tiemposubida_4ta','zona777subida_1era','zona777subida_2da','zona777subida_3era','zona777subida_4ta','paraderobajada_1era','paraderobajada_2da','paraderobajada_3era','paraderobajada_4ta','tiempobajada_1era','tiempobajada_2da','tiempobajada_3era','tiempobajada_4ta','zona777bajada_1era','zona777bajada_2da','zona777bajada_3era','zona777bajada_4ta','tipotransporte_1era','tipotransporte_2da','tipotransporte_3era','tipotransporte_4ta','tesperaest_1era','tesperaest_2da','tesperaest_3era','tesperaest_4ta','escolar','tviaje_en_vehiculo_min','tipo_corte_etapa_viaje','proposito','dviaje_buses']
perfilesHeaders=['ServicioSentido','Patente','Paradero','NombreParada','Hini','Hfin','Cumplimiento','Correlativo','idExpedicion','DistEnRuta','#Subidas','#SubidasLejanas','Subidastotal','SubidasExpandidas','#Bajadas','#BajadasLejanas','Bajadastotal','BajadasExpandidas','Carga','Capacidad','TiempoGPSInterpolado','TiempoPrimeraTrx','TiempoGPSMasCercano','Tiempo','nSubidasTmp','ParaderoUsuario','PeriodoTSExpedicion','PeriodoTSParada','TipoDia','ZP','DeltaTrxs']

def getHeaders(file):
	if file == 'etapas':
		return etapasHeaders
	elif file == 'viajes':
		return viajesHeaders
	elif file == 'perfiles':
		return perfilesHeaders
	else:
		print('Tipo de archivo incorrectamente especificado.')

def getNumberOfAttribute(file,name):
	if file == 'etapas':
		return [i for i,x in enumerate(etapasHeaders) if x == name]
	elif file == 'viajes':
		return [i for i,x in enumerate(viajesHeaders) if x == name]
	elif file == 'perfiles':
		return [i for i,x in enumerate(perfilesHeaders) if x == name]
	else:
		print('Tipo de archivo o nombre de atributo incorrectamente especificado')

def updateHeaders(file):
	#TODO: Implement this. Read the first line and update the respective list.