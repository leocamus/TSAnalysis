"""Basic information of TS data. Be aware of the format"""
import os
import glob

defaultEtapasHeaders = ['id','nviaje','netapa','tipo_dia','tipo_transporte','fExpansionServicioPeriodoTS','tiene_bajada','tiempo2','t_subida','t_bajada','t_etapa','media_hora_subida','media_hora_bajada','x_subida','y_subida','x_bajada','y_bajada','dist_ruta_paraderos','dist_eucl_paraderos','servicio_subida','servicio_bajada','par_subida','par_bajada','comuna_subida','comuna_bajada','zona_subida','zona_bajada','sitio_subida','fExpansionZonaPeriodoTS','tEsperaMediaIntervalo']
defaultViajesHeaders = ['id','nviaje','netapa','etapas','netapassinbajada','ultimaetapaconbajada','tviaje_seg','tviaje_min','dviajeeuclidiana_mts','dviajeenruta_mts','paraderosubida','paraderobajada','comunasubida','comunabajada','diseno777subida','diseno777bajada','tiemposubida','tiempobajada','periodosubida','periodobajada','tipodia','mediahora','contrato','factorexpansion','tiempomediodeviaje','periodomediodeviaje','mediahoramediodeviaje','tipodiamediodeviaje','t_1era_etapa','d_1era_etapa','tespera_1era_etapa','ttrasbordo_1era_etapa','tcaminata_1era_etapa','dtransbordo_1era_etapa','t_2da_etapa','d_2da_etapa','tespera_2da_etapa','ttrasbordo_2da_etapa','tcaminata_2da_etapa','dtransbordo_2da_etapa','t_3era_etapa','d_3era_etapa','tespera_3era_etapa','ttrasbordo_3era_etapa','tcaminata_3era_etapa','dtransbordo_3era_etapa','t_4ta_etapa','d_4ta_etapa','tespera_4ta_etapa','ttrasbordo_4ta_etapa','tcaminata_4ta_etapa','dtransbordo_4ta_etapa','op_1era_etapa','op_2da_etapa','op_3era_etapa','op_4ta_etapa','tipoop_1era_etapa','tipoop_2da_etapa','tipoop_3era_etapa','tipoop_4ta_etapa','serv_1era_etapa','serv_2da_etapa','serv_3era_etapa','serv_4ta_etapa','linea_metro_subida_1','linea_metro_subida_2','linea_metro_subida_3','linea_metro_subida_4','linea_metro_bajada_1','linea_metro_bajada_2','linea_metro_bajada_3','linea_metro_bajada_4','paraderosubida_1era','paraderosubida_2da','paraderosubida_3era','paraderosubida_4ta','tiemposubida_1era','tiemposubida_2da','tiemposubida_3era','tiemposubida_4ta','zona777subida_1era','zona777subida_2da','zona777subida_3era','zona777subida_4ta','paraderobajada_1era','paraderobajada_2da','paraderobajada_3era','paraderobajada_4ta','tiempobajada_1era','tiempobajada_2da','tiempobajada_3era','tiempobajada_4ta','zona777bajada_1era','zona777bajada_2da','zona777bajada_3era','zona777bajada_4ta','tipotransporte_1era','tipotransporte_2da','tipotransporte_3era','tipotransporte_4ta','tesperaest_1era','tesperaest_2da','tesperaest_3era','tesperaest_4ta','escolar','tviaje_en_vehiculo_min','tipo_corte_etapa_viaje','proposito','dviaje_buses']
defaultPerfilesHeaders = ['ServicioSentido','Patente','Paradero','NombreParada','Hini','Hfin','Cumplimiento','Correlativo','idExpedicion','DistEnRuta','#Subidas','#SubidasLejanas','Subidastotal','SubidasExpandidas','#Bajadas','#BajadasLejanas','Bajadastotal','BajadasExpandidas','Carga','Capacidad','TiempoGPSInterpolado','TiempoPrimeraTrx','TiempoGPSMasCercano','Tiempo','nSubidasTmp','ParaderoUsuario','PeriodoTSExpedicion','PeriodoTSParada','TipoDia','ZP','DeltaTrxs']
defaultTRXPPUHeaders = ['Unidad','Patente','Servicio','Sentido','SerSen','FechaInicio','Dpinicio','Mhinicio','FechaFin','Dpfin','Lruta','TipoDia','Hitrx','Hftrx','Plazas','TrxValidas','TarjetasNoValidas','Operativo']

currentSSHDates = [
'2017-03-01',
'2017-03-02',
'2017-03-03',
'2017-03-04',
'2017-03-05',
'2017-03-07',
'2017-03-09',
'2017-03-11',
'2017-03-12',
'2017-03-13',
'2017-03-14',#new_perfil
'2017-03-15',
'2017-03-16',
'2017-03-17',
'2017-03-18',
'2017-03-19',
'2017-03-26',
'2017-04-08',
'2017-04-09',
'2017-04-10',#new_etapa,new_perfil
'2017-04-11',
'2017-04-12',
'2017-04-14',
'2017-04-15',
'2017-04-16',
'2017-04-17',#new_etapa
'2017-04-18',
'2017-04-19',
'2017-04-20',
'2017-04-22',
'2017-04-23',
'2017-04-25',
'2017-04-26',
'2017-04-27',
'2017-04-28',
'2017-04-29',
'2017-04-30',
'2017-05-01',
'2017-05-02',
'2017-05-03',
'2017-05-04',
'2017-05-06',
'2017-05-07',
'2017-05-08',
'2017-05-10',
'2017-05-14',
'2017-05-15',
'2017-05-17',
'2017-05-19',
'2017-05-20',
'2017-05-21',
'2017-05-22',
'2017-05-25',#new_perfil
'2017-05-26',
'2017-05-27',
'2017-05-28',
'2017-05-29',
'2017-05-30',
'2017-05-31',
'2017-06-01',
'2017-06-02',
'2017-06-03',
'2017-06-04',
'2017-06-05',#new_etapa
'2017-06-13',
'2017-06-14',
'2017-06-15',
'2017-06-16',
'2017-06-17',
'2017-06-18',
'2017-06-19',
'2017-06-21',
'2017-06-22',
'2017-06-23',
'2017-06-24',
'2017-06-25',
'2017-06-26',
'2017-06-27',
'2017-06-29',
'2017-06-30',
'2017-07-01',
'2017-07-02',
'2017-07-03',
'2017-07-04',
'2017-07-05',
'2017-07-06',
'2017-07-07',
'2017-07-08',
'2017-07-09',
'2017-07-10',
'2017-07-11',#new_perfil
'2017-07-12',
'2017-07-13',
'2017-07-14',
'2017-07-15',
'2017-07-16',
'2017-07-18',
'2017-07-19',
'2017-08-01',
'2017-08-02',
'2017-08-03',
'2017-08-04',
'2017-08-05',
'2017-08-06',
'2017-08-08',
'2017-08-09',
'2017-08-11',
'2017-08-12',
'2017-08-13',
'2017-08-14',
'2017-08-15',
'2017-08-17',
'2017-08-18',
'2017-08-19',
'2017-08-20',
'2017-08-21',
'2017-08-22',
'2017-08-23',
'2017-08-24',
'2017-08-25',
'2017-08-26',
'2017-08-27']

common_dates = [
'2017-03-09',
'2017-03-14',
'2017-03-15',
'2017-03-16',
'2017-04-11',
'2017-04-12',
'2017-04-18',
'2017-06-14',
'2017-06-15',
'2017-07-11',
'2017-07-13',
'2017-07-18',
'2017-07-19',
'2017-08-08',
'2017-08-09',
'2017-08-17',
'2017-08-22',
'2017-08-24']


currentTRXPPUDates = {} #TODO: Sometime it should be filled

fourLevelsUp = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

SSHDir = os.path.join(fourLevelsUp,'03_datos/01_SSH')
TRXPPUDir = os.path.join(fourLevelsUp,'03_datos/02_TRXPPU')
busesTorniqueteDir = os.path.join(fourLevelsUp,'03_datos/03_BUSESTORNIQUETE')
DTPMDir = os.path.join(fourLevelsUp,'03_datos/04_DTPM')
SummaryDir = os.path.join(fourLevelsUp,'03_datos/05_SUMMARY')
RFADir = os.path.join(fourLevelsUp,'03_datos/06_RFA')
DTPM_TRXDir = os.path.join(fourLevelsUp,'03_datos/08_DTPM_TRX')

def updateCurrentSSHDates():
	currentSSHDates = [] #Cleaning and filling again
	for file in os.listdir(SSHDir):
		if file.endswith('.etapas'): #Be aware that dates are updated based on etapas files
			date = file.split('_')[0]
			currentSSHDates.append(date)
	return currentSSHDates