"""Module to reduce the size of the 'Transantiago' files"""

import HeadersUtils

def main(fileType,date):
	complexFile = readComplexFile(fileType,date)
	partiallySimplifiedFile = simplifyAttributes(complexFile)
	completeSimplifiedFile = simplifyObservations(partiallySimplifiedFile)
	writeSimplifiedFile(completeSimplifiedFile)

def readComplexFile(fileType,date):
	HeadersUtils.
	return complexFile

def simplifyAttributes():

def simplifyObservations():

def writeSimplifiedFile():	