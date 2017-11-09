import os

defaultEtapasHeaders = ['id','nviaje','netapa','tipo_dia','tipo_transporte','fExpansionServicioPeriodoTS','tiene_bajada','tiempo2','t_subida','t_bajada','t_etapa','media_hora_subida','media_hora_bajada','x_subida','y_subida','x_bajada','y_bajada','dist_ruta_paraderos','dist_eucl_paraderos','servicio_subida','servicio_bajada','par_subida','par_bajada','comuna_subida','comuna_bajada','zona_subida','zona_bajada','sitio_subida','fExpansionZonaPeriodoTS','tEsperaMediaIntervalo']
defaultViajesHeaders = ['id','nviaje','netapa','etapas','netapassinbajada','ultimaetapaconbajada','tviaje_seg','tviaje_min','dviajeeuclidiana_mts','dviajeenruta_mts','paraderosubida','paraderobajada','comunasubida','comunabajada','diseno777subida','diseno777bajada','tiemposubida','tiempobajada','periodosubida','periodobajada','tipodia','mediahora','contrato','factorexpansion','tiempomediodeviaje','periodomediodeviaje','mediahoramediodeviaje','tipodiamediodeviaje','t_1era_etapa','d_1era_etapa','tespera_1era_etapa','ttrasbordo_1era_etapa','tcaminata_1era_etapa','dtransbordo_1era_etapa','t_2da_etapa','d_2da_etapa','tespera_2da_etapa','ttrasbordo_2da_etapa','tcaminata_2da_etapa','dtransbordo_2da_etapa','t_3era_etapa','d_3era_etapa','tespera_3era_etapa','ttrasbordo_3era_etapa','tcaminata_3era_etapa','dtransbordo_3era_etapa','t_4ta_etapa','d_4ta_etapa','tespera_4ta_etapa','ttrasbordo_4ta_etapa','tcaminata_4ta_etapa','dtransbordo_4ta_etapa','op_1era_etapa','op_2da_etapa','op_3era_etapa','op_4ta_etapa','tipoop_1era_etapa','tipoop_2da_etapa','tipoop_3era_etapa','tipoop_4ta_etapa','serv_1era_etapa','serv_2da_etapa','serv_3era_etapa','serv_4ta_etapa','linea_metro_subida_1','linea_metro_subida_2','linea_metro_subida_3','linea_metro_subida_4','linea_metro_bajada_1','linea_metro_bajada_2','linea_metro_bajada_3','linea_metro_bajada_4','paraderosubida_1era','paraderosubida_2da','paraderosubida_3era','paraderosubida_4ta','tiemposubida_1era','tiemposubida_2da','tiemposubida_3era','tiemposubida_4ta','zona777subida_1era','zona777subida_2da','zona777subida_3era','zona777subida_4ta','paraderobajada_1era','paraderobajada_2da','paraderobajada_3era','paraderobajada_4ta','tiempobajada_1era','tiempobajada_2da','tiempobajada_3era','tiempobajada_4ta','zona777bajada_1era','zona777bajada_2da','zona777bajada_3era','zona777bajada_4ta','tipotransporte_1era','tipotransporte_2da','tipotransporte_3era','tipotransporte_4ta','tesperaest_1era','tesperaest_2da','tesperaest_3era','tesperaest_4ta','escolar','tviaje_en_vehiculo_min','tipo_corte_etapa_viaje','proposito','dviaje_buses']
defaultPerfilesHeaders = ['ServicioSentido','Patente','Paradero','NombreParada','Hini','Hfin','Cumplimiento','Correlativo','idExpedicion','DistEnRuta','#Subidas','#SubidasLejanas','Subidastotal','SubidasExpandidas','#Bajadas','#BajadasLejanas','Bajadastotal','BajadasExpandidas','Carga','Capacidad','TiempoGPSInterpolado','TiempoPrimeraTrx','TiempoGPSMasCercano','Tiempo','nSubidasTmp','ParaderoUsuario','PeriodoTSExpedicion','PeriodoTSParada','TipoDia','ZP','DeltaTrxs']
defaultTRXPPUHeaders = ['Unidad','Patente','Servicio','Sentido','SerSen','FechaInicio','Dpinicio','Mhinicio','FechaFin','Dpfin','Lruta','TipoDia','Hitrx','Hftrx','Plazas','TrxValidas','TarjetasNoValidas','Operativo']

currentSSHDates = {'2017-03-01'}  # Be aware of the format.

threeLevelsUp = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SSHDir = threeLevelsUp + r'\03_datos\01_SSH'
TRXPPUDir = threeLevelsUp + r'\03_datos\02_TRXPPU'


# Deberían entregarseles 1 o 2 argumentos:
# Si es sólo un argumento (fileType), entonces devolver los headers por defecto
# Si son dos argumentos (fileType, exactDate), entonces devolver los headers del archivo especificado, separado por comas.

def getHeaders(*args):
	if len(args) == 1: # only fileType, then defaultHeaders
		if fileType == 'etapas':
			return defaultEtapasHeaders
		elif fileType == 'viajes':
			return defaultViajesHeaders
		elif fileType == 'perfiles':
			return defaultPerfilesHeaders
		elif fileType == 'TRXPPU':
			return defaultTRXPPUHeaders
		else:
			print('Tipo de archivo incorrecta')
	elif len(args) == 2: # fileType and date, then readFirstLines
		if args[1] in currentSSHDates:
			#TODO: DO EVERYTHING
			if fileType == 'etapas':
				etapasFile = args[1] + '.etapas'
				etapasPath = os.path.join(SSHDir, etapasFile)
				readAndPrintHeader(etapasPath)
			elif fileType = 'viajes':
				viajesFile = args[1] + '.viajes'
				viajesPath = os.path.join(SSHDir, viajesFile)
				readAndPrintHeader(viajesPath)
			elif fileType = 'perfiles':
				perfilesFile = args[1] + '.perfiles'
				perfilesPath = os.path.join(SSHDir, perfilesFile) 
				readAndPrintHeader(perfilesPath)
		else print ('Fecha incorrectamente especificada')
	else print('Número de argumentos mal especificado')


def getCurrentSSHDates():
	return currentSSHDates

def readAndPrintHeader(filePath):
	with open(filePath, "r") as file:
		first_line = file.readline()
		print(first_line)

def getNumberOfAttribute(fileType,headerName):
	if fileType == 'etapas':
		return [i for i,x in enumerate(defaultEtapasHeaders) if x == headerName]
	elif fileType == 'viajes':
		return [i for i,x in enumerate(defaultViajesHeaders) if x == headerName]
	elif fileType == 'perfiles':
		return [i for i,x in enumerate(defaultPerfilesHeaders) if x == headerName]
	elif fileType == 'TRXPPU':
		return [i for i,x in enumerate(defaultTRXPPUHeaders) if x == headerName]
	else:
		print('Tipo de archivo o nombre de atributo incorrectamente especificado')
