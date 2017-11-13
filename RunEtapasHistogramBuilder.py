"""Module to run the complete methodology for building histograms"""
from Utils import SimplifyEtapasUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import os

analyzedDate = input('Enter the date to analyze: ')
analyzedVehicule = input('Enter the vehicle to analyze: ')
SSHDir = HeadersUtils.SSHDir
currentSSHDates = TransantiagoConstants.currentSSHDates

def runSimplifyEtapas():
	SimplifyEtapasUtils.writeSimplifiedEtapa(analyzedDate,analyzedVehicule,'id','nviaje','tipo_transporte','t_subida','servicio_subida','par_subida','sitio_subida')

def loadSimplifiedEtapas():
	try:
		if analyzedDate in currentSSHDates:
			simplifiedEtapasFile = analyzedDate + '_simplifiedEtapas.txt'
			simplifiedEtapasPath = os.path.join(SSHDir, simplifiedEtapasFile)	
		else:
			raise ValueError('date is not correctly specified')
	except ValueError as dateErr:
		print(dateErr)

	etapas_df = pd.read_table('C:/Users/Tesista/Desktop/Evasión/01_analisis/03_datos/01_SSH/hola.txt')