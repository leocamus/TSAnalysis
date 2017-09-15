etapasPath='C:/Users/Tesista/Desktop/Evasión/01_analisis/03_datos/2017-03-01.etapas'
perfilesPath='C:/Users/Tesista/Desktop/Evasión/01_analisis/03_datos/2017-03-01.perfiles'
viajesPath='C:/Users/Tesista/Desktop/Evasión/01_analisis/03_datos/2017-03-01.viajes'

nOfLinesToExtract=50


muestraEtapasPath='C:/Users/Tesista/Desktop/Evasión/01_analisis/03_datos/1Marzo2017Etapas.txt'
muestraPerfilesPath='C:/Users/Tesista/Desktop/Evasión/01_analisis/03_datos/1Marzo2017Perfiles.txt'
muestraViajesPath='C:/Users/Tesista/Desktop/Evasión/01_analisis/03_datos/1Marzo2017Viajes.txt'



with open(etapasPath, 'r') as etapasFile:
    muestraEtapasFile = open(muestraEtapasPath,'w') 
    for i in range(nOfLinesToExtract):
        line=etapasFile.readline()
        muestraEtapasFile.write(line)
    muestraEtapasFile.close()

with open(perfilesPath, 'r') as perfilesFile:
    muestraPerfilesFile = open(muestraPerfilesPath,'w') 
    for i in range(nOfLinesToExtract):
        line=perfilesFile.readline()
        muestraPerfilesFile.write(line)
    muestraPerfilesFile.close()

with open(viajesPath, 'r') as viajesFile:
    muestraViajesFile = open(muestraViajesPath,'w') 
    for i in range(nOfLinesToExtract):
        line=viajesFile.readline()
        muestraViajesFile.write(line)
    muestraViajesFile.close()

