import os
#a comment
etapasHeaders= ['id','nviaje','netapa','tipo_dia','tipo_transporte','fExpansionServicioPeriodoTS','tiene_bajada','tiempo2','t_subida','t_bajada','t_etapa','media_hora_subida','media_hora_bajada','x_subida','y_subida','x_bajada','y_bajada','dist_ruta_paraderos','dist_eucl_paraderos','servicio_subida','servicio_bajada','par_subida','par_bajada','comuna_subida','comuna_bajada','zona_subida','zona_bajada','sitio_subida','fExpansionZonaPeriodoTS','tEsperaMediaIntervalo']
viajesHeaders=['id','nviaje','netapa','etapas','netapassinbajada','ultimaetapaconbajada','tviaje_seg','tviaje_min','dviajeeuclidiana_mts','dviajeenruta_mts','paraderosubida','paraderobajada','comunasubida','comunabajada','diseno777subida','diseno777bajada','tiemposubida','tiempobajada','periodosubida','periodobajada','tipodia','mediahora','contrato','factorexpansion','tiempomediodeviaje','periodomediodeviaje','mediahoramediodeviaje','tipodiamediodeviaje','t_1era_etapa','d_1era_etapa','tespera_1era_etapa','ttrasbordo_1era_etapa','tcaminata_1era_etapa','dtransbordo_1era_etapa','t_2da_etapa','d_2da_etapa','tespera_2da_etapa','ttrasbordo_2da_etapa','tcaminata_2da_etapa','dtransbordo_2da_etapa','t_3era_etapa','d_3era_etapa','tespera_3era_etapa','ttrasbordo_3era_etapa','tcaminata_3era_etapa','dtransbordo_3era_etapa','t_4ta_etapa','d_4ta_etapa','tespera_4ta_etapa','ttrasbordo_4ta_etapa','tcaminata_4ta_etapa','dtransbordo_4ta_etapa','op_1era_etapa','op_2da_etapa','op_3era_etapa','op_4ta_etapa','tipoop_1era_etapa','tipoop_2da_etapa','tipoop_3era_etapa','tipoop_4ta_etapa','serv_1era_etapa','serv_2da_etapa','serv_3era_etapa','serv_4ta_etapa','linea_metro_subida_1','linea_metro_subida_2','linea_metro_subida_3','linea_metro_subida_4','linea_metro_bajada_1','linea_metro_bajada_2','linea_metro_bajada_3','linea_metro_bajada_4','paraderosubida_1era','paraderosubida_2da','paraderosubida_3era','paraderosubida_4ta','tiemposubida_1era','tiemposubida_2da','tiemposubida_3era','tiemposubida_4ta','zona777subida_1era','zona777subida_2da','zona777subida_3era','zona777subida_4ta','paraderobajada_1era','paraderobajada_2da','paraderobajada_3era','paraderobajada_4ta','tiempobajada_1era','tiempobajada_2da','tiempobajada_3era','tiempobajada_4ta','zona777bajada_1era','zona777bajada_2da','zona777bajada_3era','zona777bajada_4ta','tipotransporte_1era','tipotransporte_2da','tipotransporte_3era','tipotransporte_4ta','tesperaest_1era','tesperaest_2da','tesperaest_3era','tesperaest_4ta','escolar','tviaje_en_vehiculo_min','tipo_corte_etapa_viaje','proposito','dviaje_buses']
perfilesHeaders=['ServicioSentido','Patente','Paradero','NombreParada','Hini','Hfin','Cumplimiento','Correlativo','idExpedicion','DistEnRuta','#Subidas','#SubidasLejanas','Subidastotal','SubidasExpandidas','#Bajadas','#BajadasLejanas','Bajadastotal','BajadasExpandidas','Carga','Capacidad','TiempoGPSInterpolado','TiempoPrimeraTrx','TiempoGPSMasCercano','Tiempo','nSubidasTmp','ParaderoUsuario','PeriodoTSExpedicion','PeriodoTSParada','TipoDia','ZP','DeltaTrxs']
TRXPPUHeaders = ['Unidad','Patente','Servicio','Sentido','SerSen','FechaInicio','Dpinicio','Mhinicio','FechaFin','Dpfin','Lruta','TipoDia','Hitrx','Hftrx','Plazas','TrxValidas','TarjetasNoValidas','Operativo']

defaultDate = "2017-03-01"

threeLevelsUp = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
analysisDir = threeLevelsUp + r'\03_datos'
SSHDir = analysisDir + r'\01_SSH'


def getHeaders(fileType):
	if fileType == 'etapas':
		return etapasHeaders
	elif fileType == 'viajes':
		return viajesHeaders
	elif fileType == 'perfiles':
		return perfilesHeaders
	elif fileType == 'TRXPPU':
		return TRXPPUHeaders
	else:
		print('Tipo de archivo incorrectamente especificado.')

def getNumberOfAttribute(fileType,headerName):
	if fileType == 'etapas':
		return [i for i,x in enumerate(etapasHeaders) if x == headerName]
	elif fileType == 'viajes':
		return [i for i,x in enumerate(viajesHeaders) if x == headerName]
	elif fileType == 'perfiles':
		return [i for i,x in enumerate(perfilesHeaders) if x == headerName]
	elif fileType == 'TRXPPU':
		return [i for i,x in enumerate(TRXPPUHeaders) if x == headerName]
	else:
		print('Tipo de archivo o nombre de atributo incorrectamente especificado')

#TODO: Terminar de escribir esto. arg[0] = fileType, arg[1] = date.
def updateHeaders(*args):
    if len(args) == 1 and isinstance(args[0], str):
    	if (args[0] == 'etapas'):
    		filePath = SSHDir + 







    	 or args[0] == 'viajes' or args[0] == 'perfiles'):

        print('Leyendo la primera línea del archivo especificado para la fecha por defecto: 1 marzo 2017')






        
#outPath = str(analysisDir) + r"\SSH\03_datos\01_histogramDDBB\1_03_2017E.txt"

#with open(etapasPath, "r") as etapasFile:
#    outFile = open(outPath,'w') 
#    for line in etapasFile:
#        lineList=line.split("|")
#        if(lineList[4]=="BUS"):
#            outFile.write(lineList[0]+"|"+lineList[8]+"|"+lineList[19]+"|"+lineList[21]+"|"+lineList[27]+"\n")
#    outFile.close()



    elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
        print('Leyendo la primera línea del archivo especificado para la fecha especificada')
    else:
    	print('Something went wrong.')