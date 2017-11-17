"""Reads turnstile database into a pandas dataframe"""
import os
import pandas as pd
from Utils import TransantiagoConstants

busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir

def readTurnstileData():
	"""Merges the loaded etapas-file with the turnstile-file.fecha_instalacion into a pandas df and returns it"""
	torniquetesFile = 'Avance_Consolidado_v2.xlsx'
	torniquetesDataPath = os.path.join(busesTorniqueteDir, torniquetesFile)
	busesTorniquete_df = pd.read_excel(torniquetesDataPath)
	busesTorniquete_df.columns=['sitio_subida','fecha_instalacion']
	return busesTorniquete_df