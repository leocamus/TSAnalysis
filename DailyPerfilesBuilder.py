"""Module to run the complete methodology for building histograms, and build it silently"""
from Utils import SimplifyFilesUtils
from Utils import HeadersUtils
from Utils import TransantiagoConstants
import pandas as pd
import numpy as np
import os
import datetime as dt

class RunSilentlyDailyPerfilesBuilderClass:

	SSHDir = TransantiagoConstants.SSHDir
	busesTorniqueteDir = TransantiagoConstants.busesTorniqueteDir
	currentSSHDates = TransantiagoConstants.updateCurrentSSHDates()

	def __init__(self,date,vehicle='BUS',zp='0'):
		self.analyzedDate = date
		self.analyzedVehicle = vehicle
		self.if_ZP = zp
		self.perfiles_df = pd.DataFrame()

	def runSimplifyPerfiles(self):
		"""Not always necessary. Reducing the complexity of the original etapas-file. Attributes to extract are hardcoded"""
		SimplifyFilesUtils.writeSimplifiedPerfiles(self.analyzedDate,self.if_ZP,'ServicioSentido','Patente','Paradero','Hini','Hfin','idExpedicion','DistEnRuta')

	def loadSimplifiedPerfiles(self):
		"""Returns the simplified perfiles-file as pandas df"""
		try:
			if self.analyzedDate in RunSilentlyDailyPerfilesBuilderClass.currentSSHDates:
				simplifiedPerfilesFile = self.analyzedDate + '_simplified.perfiles'
				simplifiedPerfilesPath = os.path.join(RunSilentlyDailyPerfilesBuilderClass.SSHDir, simplifiedPerfilesFile)	
			else:
				raise ValueError('date is not correctly specified')
		except ValueError as dateErr:
			print(dateErr)

		self.perfiles_df = pd.read_table(simplifiedPerfilesPath, sep='|', encoding='latin-1')