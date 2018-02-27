

##Function to load libraries and install packages, if necessary
getLibraries <- function(libs) {
  
  for (lib in libs) {
    if(!lib %in% rownames(installed.packages())){install.packages(lib, repos = "http://cran.us.r-project.org")}
    library(as.character(lib), character.only = TRUE)
  }
}

boxplot_total <- function(dataframe){
  #Función que calcula boxplot para el total de datos seperando expediciones con y sin torniquete.
    #Dataframe corresponde a las expediciones por servicio-periodo
  
  #Subsetting dataframe by turnstile usage
  dataframe_st <- subset(dataframe, dataframe$turnstile == 0)
  dataframe_ct <- subset(dataframe, dataframe$turnstile_marip == 1)
  
  if(nrow(dataframe_st) > 0 & nrow(dataframe_ct) > 0){
    
    #Combining two datasets
    dataset <- rbind(dataframe_ct,dataframe_st)
    dataset$categoria <- c(rep("C/T", nrow(dataframe_ct)),rep("S/T",nrow(dataframe_st)))
    
    pdf(file = paste(unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), ".pdf", sep = ""), 10,5)
    
    #Boxplots
    b1 <- ggplot(data = dataframe_ct, aes(x= "", y= texpedicion)) + 
      geom_boxplot() +
      xlab("") +
      stat_summary(fun.y = mean, colour= "green", geom="point", 
                   shape=18, size=3) +
      ylab("TExpedicion (min)") +
      coord_cartesian(ylim = c(min(dataframe_ct$texpedicion,dataframe_st$texpedicion), max(dataframe_ct$texpedicion,dataframe_st$texpedicion))) +
      ggtitle("With turnstile")
    
    b2 <- ggplot(data = dataframe_st, aes(x= "", y= texpedicion)) + 
      geom_boxplot() +
      xlab("") +
      ylab("TExpedicion (min)") +
      stat_summary(fun.y = mean, colour= "green", geom="point", 
                   shape=18, size=3) +
      coord_cartesian(ylim = c(min(dataframe_ct$texpedicion,dataframe_st$texpedicion), max(dataframe_ct$texpedicion,dataframe_st$texpedicion))) +
      ggtitle("Without turnstile")
    
    p1 <- ggplot(data=dataset, aes(x=1:nrow(dataset), y=dataset$texpedicion, col=categoria)) + 
      geom_point() +
      xlab("Obs.") +
      ylab("TExpedicion (min)") +
      theme(legend.title = element_blank(),
            axis.text.x = element_blank(),
            legend.position="top",
            legend.margin=margin(0,0,0,0),
            legend.box.margin=margin(-10,-10,-10,-10)) +
      coord_cartesian(ylim = c(min(dataframe_ct$texpedicion,dataframe_st$texpedicion), max(dataframe_ct$texpedicion,dataframe_st$texpedicion))) +
      ggtitle("Dataset")
    
    
    #Plotting
    grid.arrange(b1, b2, p1, ncol = 3, nrow = 1, widths=c(1,1,2.5), top= paste(unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), sep = ""))
    
    dev.off()
    
  }
}

boxplot_dia <- function(dataframe){
  #Función que calcula boxplot por cada día de una semana.
    #Input corresponde a un dataframe con expediciones con y sin torniquete de toda la semana.
  
  #Subsetting dataframe by turnstile usage
  dataframe_st <- subset(dataframe, dataframe$turnstile == 0)
  dataframe_ct <- subset(dataframe, dataframe$turnstile_marip == 1)
  
  
  #Creating boxplot per day
  if(length(unique(dataframe_ct$wday)) == 5 & length(unique(dataframe_st$wday)) == 5){
    
    pdf(file = paste("BOX_SEMANA - ",unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), ".pdf", sep = ""), 10,5)
    
    #Boxplots
    b1 <- ggplot(data = dataframe_ct, aes(x= weekday, y= texpedicion)) + 
      geom_boxplot(aes(fill=weekday)) +
      xlab("") +
      ylab("TExpedicion (min)") +
      theme(legend.position="none") +
      coord_cartesian(ylim = c(min(dataframe_ct$texpedicion,dataframe_st$texpedicion), max(dataframe_ct$texpedicion,dataframe_st$texpedicion))) +
      ggtitle("With turnstile")
    
    b2 <- ggplot(data = dataframe_st, aes(x= weekday, y= texpedicion)) + 
      geom_boxplot(aes(fill=weekday)) +
      xlab("") +
      ylab("TExpedicion (min)") +
      coord_cartesian(ylim = c(min(dataframe_ct$texpedicion,dataframe_st$texpedicion), max(dataframe_ct$texpedicion,dataframe_st$texpedicion))) +
      ggtitle("Without turnstile")
    
    
    #Plotting
    grid.arrange(b1, b2, ncol = 2, nrow = 1, widths=c(1,1.3), top= paste(unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), sep = ""))
    
    
    dev.off()
    
  }
}

fill_patente <- function(placa){
  return(paste(unlist(strsplit(as.character(placa), "(?=[A-Za-z])(?<=[0-9])|(?=[0-9])(?<=[A-Za-z])", perl=TRUE)), collapse = "-"))
  }


libs <- c("data.table",
          "plyr",
          "lubridate",
          "chron",
          "ggplot2",
          "ggpubr",
          "gridExtra",
          "stringr",
          "fuzzyjoin",
          "sqldf")

getLibraries(libs)



#Working with: ################################ EVASION ###################################
#Description: Script para procesar RAW BBDD de Fiscalización. Output: evasion_edit (no es el consolidado).
#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/02_Fiscalizacion/01_Evasion (2017)/")

#Reading files
evasion <- read.csv(file = "evasion_2017.csv", header = TRUE, sep = ";")
evasion$FECHA <- as.Date(evasion$FECHA)
#Para 2016
#evasion$TRI <- ifelse(evasion$FECHA <= "2016-03-31",1,ifelse(evasion$FECHA > "2016-03-31" & evasion$FECHA <= "2016-06-30",2,ifelse(evasion$FECHA > "2016-06-30" & evasion$FECHA <= "2016-09-30",3,4)))

#Variable name
names(evasion)[3] <- "Patente"

#Changing plate format
evasion$Patente <- unlist(lapply(evasion$Patente, FUN = fill_patente))

#Deleting white spaces and all to uppercase (just in case)
evasion$FECHA <- gsub(" ","",evasion$FECHA)
evasion$SERVICIO <- gsub(" ","",evasion$SERVICIO)
evasion$Patente <- gsub(" ","",evasion$Patente)
evasion$SERVICIO <- toupper(evasion$SERVICIO)
evasion$Patente <- toupper(evasion$Patente)

#Changing time format
evasion$HORA <- as.integer(as.character(evasion$HORA))
evasion$MINUTOS <- as.integer(as.character(evasion$MINUTOS))

#Reformatting time feature. You could also use formatC() function.
evasion$HORA <- sprintf("%02d",evasion$HORA)
evasion$MINUTOS <- sprintf("%02d",evasion$MINUTOS)

evasion$Hora <- paste(evasion$HORA,":",evasion$MINUTOS, sep = "")


#Reordering
evasion <- evasion[,c(1,3,2,4,5,6,7,14,10,11,12,13)]


write.table(evasion, file = "evasion_2017_edit.csv", row.names = FALSE, sep = ";")


#Working with: ################################ EVASION ###################################





#Working with: ############################ MERGE EVASION WITH TURNSTILE ###############################
#Script description:  Script para procesar datos de fiscalización editados, consolidarlos por expedición y determinar
#                     número de expediciones con y sin torniquete. Output: evasion_consolidado
### PARA AÑO 2017 ###

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/02_Fiscalizacion/02_Evasion (2016)/")

#Reading files
#Evasion
evasion <- read.csv(file = "evasion_2016_edit.csv", header = TRUE, sep = ";")
evasion$FECHA <- as.Date(evasion$FECHA)

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/")

#Torniquete mariposa
torn_marip <- read.csv(file = "torniquetes_mariposa.csv", header = TRUE, sep = ";")
torn_marip$X <- NULL
names(torn_marip) <- c("UN","Patente","Fecha_mariposa")
torn_marip$Patente <- gsub(" ","",torn_marip$Patente)
torn_marip$Patente <- toupper(torn_marip$Patente)
torn_marip$Fecha_mariposa <- gsub(" ","", torn_marip$Fecha_mariposa)
torn_marip$Patente <- as.character(torn_marip$Patente)
ind <- which(!grepl("-", torn_marip$Patente))
torn_marip$Patente[ind] <- unlist(lapply(torn_marip$Patente[ind], FUN = fill_patente))
torn_marip$Fecha_mariposa <- as.Date(torn_marip$Fecha_mariposa, format= "%Y-%m-%d")


#Total torniquete
torniquete <- read.csv(file = "torniquetes.csv", header = TRUE, sep = ";")
torniquete <- torniquete[,1:2]
torniquete$Instalacion <- as.Date(torniquete$Instalacion)
torniquete$Patente <- gsub(" ","",torniquete$Patente)
torniquete$Patente <- toupper(torniquete$Patente)

#Deleting white spaces
evasion$TP <- gsub(" ", "", evasion$TP)
evasion$TP <- toupper(evasion$TP)

#Changing factor levels
evasion$TP <- factor(evasion$TP, levels = unique(evasion$TP))

#Considerando que no existe evasión en zonas pagas.
evasion$NO.VALIDAN[which(evasion$TP=="Z" & evasion$NO.VALIDAN !=0)] <- 0

#Collapsing evasion dataset by expedition
dataframe <- data.table(evasion)
dataframe <- dataframe[, list(DET = max(table(PUERTA.NUMERO)),
                              Y = sum(INGRESAN),
                              EV = sum(NO.VALIDAN),
                              I.P = sum(INGRESAN[which(TP == "P")]),
                              I.ZP = sum(INGRESAN[which(TP == "Z")]),
                              I.PP1 = sum(INGRESAN[which(PUERTA.NUMERO == 1)]) - sum(NO.VALIDAN[which(PUERTA.NUMERO == 1)]),
                              I.EP1 = sum(NO.VALIDAN[which(PUERTA.NUMERO == 1)]),
                              I.PP2 = sum(INGRESAN[which(PUERTA.NUMERO == 2)]) - sum(NO.VALIDAN[which(PUERTA.NUMERO == 2)]),
                              I.EP2 = sum(NO.VALIDAN[which(PUERTA.NUMERO == 2)]),
                              I.PP3 = sum(INGRESAN[which(PUERTA.NUMERO == 3)]) - sum(NO.VALIDAN[which(PUERTA.NUMERO == 3)]),
                              I.EP3 = sum(NO.VALIDAN[which(PUERTA.NUMERO == 3)]),
                              I.PP4 = sum(INGRESAN[which(PUERTA.NUMERO == 4)]) - sum(NO.VALIDAN[which(PUERTA.NUMERO == 4)]),
                              I.EP4 = sum(NO.VALIDAN[which(PUERTA.NUMERO == 4)]),
                              TRI = unique(TRI)),
                       by= list(FECHA,Patente,SERVICIO,HORA.INICIO)]


#Adding turnstile information
dataframe <- merge(dataframe, torn_marip, by= "Patente", all.x = TRUE)
dataframe <- merge(dataframe, torniquete, by= "Patente", all.x = TRUE)


#Computing number of expedition with turnstile
#Turnstile during the expedition?
dataframe$turnstile[is.na(dataframe$Instalacion) & is.na(dataframe$Fecha_mariposa)] <- 0
dataframe$turnstile_marip[is.na(dataframe$Instalacion) & is.na(dataframe$Fecha_mariposa)] <- 0

#Indexes
ind_na <- which(is.na(dataframe$turnstile))



#Turnstile during the expedition?
dataframe$turnstile[ind_na] <- ifelse(dataframe$FECHA[ind_na] > pmin(dataframe$Fecha_mariposa[ind_na],dataframe$Instalacion[ind_na],na.rm = TRUE),1,0)

#Turnstile during the expedition? 2017 style
dataframe$turnstile_marip[ind_na] <- ifelse(dataframe$FECHA[ind_na] > dataframe$Fecha_mariposa[ind_na],1,0)
dataframe$turnstile_marip[is.na(dataframe$turnstile_marip)] <- 0


write.table(dataframe, file = "evasion_2016_consolidado.csv", row.names = FALSE, sep = ";")

#Working with: ############################ MERGE EVASION WITH TURNSTILE ###############################






#Working with: ############################ MERGE BETWEEN EVASION AND LBS ###############################
#Script description:  Script desarrollado para leer todos los archivos de LBS sacados de Access, combinarlos
#                     en uno solo y realizar el merge entre este archivo y las expediciones medidas en 
#                     fiscalización. Output: BBDD_AÑO_consolidada.csv. Archivo con variables asociadas a 
#                     expediciones para estimación del modelo.


#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/05_LBS/2017/")


#Reading files
filelist <- list.files(pattern = ".*.txt")
datalist <- lapply(filelist, function(x)read.table(x, header=T,sep = ";"))
lbs <- do.call("rbind", datalist) 

#Changing period names and class
lbs$Periodo <- gsub("Transici\xf3n","Transicion",lbs$Periodo)
lbs$Periodo <- gsub("Ma\xf1ana","Manana",lbs$Periodo)
lbs$Periodo <- gsub("Mediod\xeda","Mediodia",lbs$Periodo)
lbs$Periodo <- factor(lbs$Periodo, levels = unique(lbs$Periodo))

#Changing time and date format
lbs$Inicio <- as.POSIXct(lbs$Inicio, format= "%d/%m/%Y %H:%M:%S")
lbs$Fin <- as.POSIXct(lbs$Fin, format= "%d/%m/%Y %H:%M:%S")
lbs$Tiempo..hh.mm.ss. <- as.POSIXct(lbs$Tiempo..hh.mm.ss., format= "%d/%m/%Y %H:%M:%S")
lbs$Inicio <- times(strftime(lbs$Inicio, format="%H:%M:%S"))
lbs$Fin <- times(strftime(lbs$Fin, format="%H:%M:%S"))
lbs$Tiempo..hh.mm.ss. <- period_to_seconds(hms(strftime(lbs$Tiempo..hh.mm.ss., format="%H:%M:%S")))
names(lbs)[8] <- "TEXP"
lbs$Fecha <- as.Date(lbs$Fecha, format= "%d/%m/%Y")

#Changing decimal separator
lbs$Distancia..m. <- as.numeric(gsub(",",".",lbs$Distancia..m.))
lbs$Velocidad..Km.hr. <- as.numeric(gsub(",",".",lbs$Velocidad..Km.hr.))



#Writing processed LBS
#write.table(lbs, file = "processed_lbs_2017.csv", row.names = FALSE, sep = ";")

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/05_LBS/2017/")
lbs <- read.csv(file = "processed_lbs_2017.csv", header = TRUE, sep = ";")
lbs$Inicio <- times(as.character(lbs$Inicio))
lbs$Fecha <- as.Date(lbs$Fecha)



#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/02_Fiscalizacion/01_Evasion (2017)/")

#Reading files
evasion <- read.csv(file = "evasion_2017_consolidado.csv", header = TRUE, sep = ";")

#Changing variables format
evasion$HORA.INICIO <- times(paste(evasion$HORA.INICIO,":00",sep = ""))
evasion$FECHA <- as.Date(evasion$FECHA)

#Adding upperbound and lowerbound
evasion$UpperBound <- evasion$HORA.INICIO + "00:10:00"
evasion$LowerBound <- evasion$HORA.INICIO - "00:10:00"

#Creating evasion ID
evasion$ID <- paste(evasion$Patente, evasion$FECHA, evasion$HORA.INICIO, sep = "")

#Merge between fiscalizacion and LBS
fiscalizacion <- sqldf('SELECT evasion.*, lbs.* 
                      FROM evasion 
                       LEFT JOIN lbs 
                       ON lbs.Patente = evasion.Patente
                       AND lbs.Fecha = evasion.FECHA
                       AND lbs.Inicio BETWEEN evasion.LowerBound AND evasion.UpperBound')

fiscalizacion <- fiscalizacion[!is.na(fiscalizacion$TEXP),]
nocurr <- data.frame(table(fiscalizacion$ID))
nocurr <- nocurr[which(nocurr$Freq > 1),]

#Para 2016
#fiscalizacion <- fiscalizacion[-which(fiscalizacion$ID %in% nocurr$Var1),]


#Reordering and saving database
fiscalizacion <- fiscalizacion[,c(1:18,20:23,27,28,30:34,36,38)]
names(fiscalizacion)[2] <- "Fecha"
names(fiscalizacion)[3] <- "COD_USU"
names(fiscalizacion)[4] <- "Ini_Fisca"
names(fiscalizacion)[23] <- "UN"
names(fiscalizacion)[24] <- "COD_TS"
names(fiscalizacion)[26] <- "Ini_LBS"
names(fiscalizacion)[27] <- "Fin_LBS"
names(fiscalizacion)[28] <- "L(m)"

fiscalizacion <- fiscalizacion[,c(2,18,3,24,25,1,23,31,4,26,27,29,28,5:17,21,22,30)]

ind_ntor <- which(fiscalizacion$turnstile==0)

fiscalizacion$turnstile <- 0
names(fiscalizacion)[27] <- "n_turnstile"
fiscalizacion$n_turnstile[ind_ntor] <- 1

write.table(fiscalizacion, file = "BBDD_2017_consolidada.csv", row.names = FALSE, sep = ";")

#Working with: ############################ MERGE BETWEEN EVASION AND LBS ###############################
  








#Working with: ############################ MERGE BETWEEN BBDD CONSOLIDADA Y DATAVEL ###############################

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/08_datavel/")
datavel <- read.csv(file = "datavel_2017.csv", header = FALSE, sep = ";")
datavel <- datavel[,-5]
names(datavel) <- c("Patente","COD_SINRUTA","PosIni","PosFin")

#Adding time and date variables
datavel$PosIni <- as.POSIXct(datavel$PosIni, format= "%Y-%m-%d %H:%M:%S")
datavel$PosFin <- as.POSIXct(datavel$PosFin, format= "%Y-%m-%d %H:%M:%S")

datavel$Date <- as.Date(datavel$PosIni)    
datavel$Inicio <- times(strftime(datavel$PosIni, format="%H:%M:%S"))
datavel$PosIni <- NULL
datavel$PosFin <- NULL
datavel$Patente <- gsub(" ","",datavel$Patente)
datavel$Patente <- toupper(datavel$Patente)
datavel$Patente <- as.factor(datavel$Patente)


#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/07_Bases_consolidadas/")
evasion <- read.csv(file = "BBDD_2017_consolidada.csv", header = TRUE, sep = ";")
evasion$Fecha <- as.Date(evasion$Fecha)
evasion$Ini_Fisca <- times(as.character(evasion$Ini_Fisca))

#Adding upperbound and lowerbound
evasion$UpperBound <- evasion$Ini_Fisca + "00:10:00"
evasion$LowerBound <- evasion$Ini_Fisca - "00:10:00"

#Creating evasion ID
evasion$ID <- paste(evasion$Patente, evasion$Fecha, evasion$Ini_Fisca, sep = "")

#Merge between fiscalizacion and DATAVEL
dataframe <- sqldf('SELECT evasion.*, datavel.* 
                       FROM evasion 
                       LEFT JOIN datavel 
                       ON datavel.Patente = evasion.Patente
                       AND datavel.Date = evasion.FECHA
                       AND datavel.Inicio BETWEEN evasion.LowerBound AND evasion.UpperBound')

dataframe <- dataframe[!is.na(dataframe$COD_SINRUTA),]
nocurr <- data.frame(table(dataframe$ID))
nocurr <- nocurr[which(nocurr$Freq > 1),]

#Para 2016
dataframe <- dataframe[-which(dataframe$ID %in% nocurr$Var1),]


write.table(dataframe, file = "BBDD_2017_consolidada_CODSIN.csv", row.names = FALSE, sep = ";")



#Working with: ############################ MERGE BETWEEN BBDD CONSOLIDADA Y DATAVEL ###############################





#Working with: ################################ Getting Route name code ################################

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/07_Bases_consolidadas/")

base_2016 <- read.csv(file = "BBDD_2016_consolidada_CODSIN.csv", header = TRUE, sep = ";")
base_2017 <- read.csv(file = "BBDD_2017_consolidada_CODSIN.csv", header = TRUE, sep = ";")
base_fisca <- rbind(base_2016,base_2017)
rm(base_2016,base_2017)

base_fisca$ID <- paste(base_fisca$Fecha,base_fisca$Patente,base_fisca$Ini_Fisca,sep = "")

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/")

diccionario <- read.csv(file = "diccionario_arena_tcad.csv", header = TRUE, sep = ";")
diccionario$Código.TCAD <- as.character(diccionario$Código.TCAD)
diccionario$Código.Arena <- as.character(diccionario$Código.Arena)

#Deleting white spaces and all to upper
diccionario$Código.TCAD <- gsub(" ","",diccionario$Código.TCAD)
diccionario$Código.Arena <- gsub(" ","",diccionario$Código.Arena)
diccionario$Código.TCAD <- toupper(diccionario$Código.TCAD)
diccionario$Código.Arena <- toupper(diccionario$Código.Arena)
base_fisca$COD_SINRUTA <- gsub(" ","",base_fisca$COD_SINRUTA)
base_fisca$COD_SINRUTA <- toupper(base_fisca$COD_SINRUTA)

#Merge between fiscalizacion database and dictionary 
names(diccionario)[3] <- "COD_SINRUTA"
ind_01 <- which(base_fisca$COD_SINRUTA == "T38701I")
base_fisca$COD_SINRUTA[2622] <- "T38706I"
ind_01 <- ind_01[-1]
base_fisca$COD_SINRUTA[ind_01] <- "T38700I"

#Merge
data <- join(base_fisca,diccionario, by="COD_SINRUTA")

#Missing values
missing <- data[is.na(data$Código.TCAD),]
data <- data[!is.na(data$Código.TCAD),]
duplicados <- data[duplicated(data$ID) | duplicated(data$ID, fromLast = TRUE),]

#Getting route names by date
data$Fecha <- factor(data$Fecha, levels = unique(data$Fecha))
expedicion <- split(data, data$Fecha)

route_day <- unlist(lapply(expedicion, function(dataframe){
  route <- unique(dataframe$Código.TCAD)
  return(gsub(" ","",paste("'",route,"'", collapse = ",")))
}))

route_byday <- data.frame(route_day)
route_byday$Date <- names(route_day)

write.table(route_byday, file = "route_bydate.csv", row.names = FALSE, sep = ";")


#Working with: ################################ Getting Route name code ################################








#Working with: ############################ ESTIMACION MODELO ###############################
#Script description:  Script que toma la base de datos consolidadas y crea una dataframe con todas las variables
#                     requeridas para la construcción del modelo econométrico. Además, se estiman diferentes modelos

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/04_Intersections/")
signals <- read.csv(file = "TrafficSignals.csv", header = TRUE, sep = ";")
signals <- signals[,2:5]
signals$YEAR <- as.factor(as.character(signals$YEAR))
names(signals)[3] <- "TS_Sentido"

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/07_Bases_consolidadas/")

#Reading input files
dataframe <- read.csv(file = "BBDD_modelotiempo.csv", header = TRUE, sep = ";")
dataframe$TS_Sentido <- paste(dataframe$COD_TS,dataframe$Sentido,sep = "")
dataframe$YEAR <- substr(dataframe$Fecha,1,4)

dataframe$SEMESTER <- ""
dataframe$SEMESTER[dataframe$TRI == 1 | dataframe$TRI == 2] <- 1
dataframe$SEMESTER[!(dataframe$TRI == 1 | dataframe$TRI == 2)] <- 2
dataframe$SEMESTER <- as.integer(dataframe$SEMESTER)

#Getting number of traffic signals by semester
dataframe <- join(dataframe, signals, by= c("YEAR","SEMESTER","TS_Sentido"))


#Adding time period variables
period <- as.data.frame(model.matrix(~dataframe$Periodo-1))
names(period) <- sprintf("P%s",3:10)
periodo_punta <- period$P4+period$P9

#Adding route variable
route <- as.data.frame(dataframe$TS_Sentido)
route <- as.data.frame(model.matrix(~route[,1]-1))
names(route) <- gsub("route\\[, 1\\]","",names(route))
largo_r <- route*dataframe$L.m.


#Bus demand with turnstile
Y_P_turnstile <- dataframe$turnstile_marip * dataframe$I.P
Y_P_turnstile_periodo <- dataframe$turnstile_marip * period * dataframe$I.P
#Y_P_turnstile_periodo <- dataframe$turnstile_marip * periodo_punta * dataframe$I.P



#Working with: ############################ ESTIMACION MODELO ###############################










#Working with: ############################ MERGE PERFILES 2017 Y BBDD ZP ###############################

#Script description: Pequeño script para procesar BBDD de zonas pagas (elimina duplicados). Output: zonas_pagas_edit
#Setting working space
# setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/03_Perfiles/")
# 
# perfiles <- read.csv(file = "perfiles.csv", header = TRUE, sep = ";")
# zp <- read.csv(file = "zonas_pagas_edit.csv", header = TRUE, sep = ";")
# 
# #Changing variable name and deleting duplicated
# names(zp)[4] <- "Nombre_Paradero"
# zp <- zp[!duplicated(zp),]
# 
# #Adding zona paga schedule
# zp[16,"laboral.ini1"] <- "06:00"
# zp[16,"laboral.fin1"] <- "14:00"
# zp[16,"laboral.ini2"] <- "17:00"
# zp[16,"laboral.fin2"] <- "20:30"
# 
# zp <- zp[-199,]
# 
# write.csv(zp, file = "zonas_pagas_edit.csv", row.names = FALSE)


#Script description: Output: perfiles editados que tiene la categoría de cada paradero (Z o P)
#Setting working space
# setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/03_Perfiles/")
# 
# perfiles <- read.csv(file = "perfiles.csv", header = TRUE, sep = ";")
# zp <- read.csv(file = "zonas_pagas_edit.csv", header = TRUE, sep = ",")
# 
# 
# 
# 
# #Collapsing evasion dataset by expedition
# dataframe <- data.table(perfiles)
# dataframe <- dataframe[, list(Y = sum(Suben) + sum(Suben_E),
#                               EV = sum(Suben_E),
#                               BAJAN= sum(Bajan)),
#                        by= list(Fecha,Patente,Servicio,Sentido,Periodo)]
# 
# 
# 
# 
# 
# #Merge between perfiles and zonas pagas
# dataframe <- join(perfiles,zp, by="Nombre_Paradero")
# 
# #Adding date format
# dataframe$Fecha <- as.Date(dataframe$Fecha, format= "%d-%m-%y")
# 
# #Changing variable class
# dataframe$Hora_Pasada <- as.character(dataframe$Hora_Pasada)
# dataframe$laboral.ini1 <- as.character(dataframe$laboral.ini1)
# dataframe$laboral.fin1 <- as.character(dataframe$laboral.fin1)
# dataframe$laboral.ini2 <- as.character(dataframe$laboral.ini2)
# dataframe$laboral.fin2 <- as.character(dataframe$laboral.fin2)
# dataframe$sabado <- as.character(dataframe$sabado)
# dataframe$domingo <- as.character(dataframe$domingo)
# 
# #Adding saturday and sunday schedule
# ind_zp_sat <- which(dataframe$sabado != "" & !is.na(dataframe$sabado))
# ind_zp_sun <- which(dataframe$domingo != "" & !is.na(dataframe$domingo))
# 
# dataframe$sabado <- gsub(" ","", dataframe$sabado)
# dataframe$domingo <- gsub(" ","", dataframe$domingo)
# 
# #Adding new variables
# dataframe$sabado.ini1 <- ""
# dataframe$sabado.fin1 <- ""
# dataframe$sabado.ini1[ind_zp_sat] <- unlist(lapply(strsplit(as.character(dataframe$sabado[ind_zp_sat]), "-"), `[[`, 1))
# dataframe$sabado.fin1[ind_zp_sat] <- unlist(lapply(strsplit(as.character(dataframe$sabado[ind_zp_sat]), "-"), `[[`, 2))
# 
# dataframe$domingo.ini1 <- ""
# dataframe$domingo.fin1 <- ""
# dataframe$domingo.ini1[ind_zp_sun] <- unlist(lapply(strsplit(as.character(dataframe$domingo[ind_zp_sun]), "-"), `[[`, 1))
# dataframe$domingo.fin1[ind_zp_sun] <- unlist(lapply(strsplit(as.character(dataframe$domingo[ind_zp_sun]), "-"), `[[`, 2))
# 
# dataframe$sabado.ini1[which(dataframe$sabado.ini1 == "7:30")] <- "07:30"
# 
# #Adding bus stop type
# dataframe$TP <- rep("P", nrow(dataframe))
# 
# #Adding indexes
# ind_zp_work <- which(!is.weekend(dataframe$Fecha) & (!is.na(dataframe$laboral.ini1) | !is.na(dataframe$laboral.ini2)))
# ind_zp_sat <- which(weekdays(dataframe$Fecha) == "Saturday" & dataframe$sabado != "" & !is.na(dataframe$sabado))
# ind_zp_sun <- which(weekdays(dataframe$Fecha) == "Sunday" & dataframe$domingo != "" & !is.na(dataframe$domingo))
# 
# #Computing kind of bus stop
# dataframe$TP[ind_zp_work] <- ifelse((dataframe$Hora_Pasada[ind_zp_work] >= dataframe$laboral.ini1[ind_zp_work] & dataframe$Hora_Pasada[ind_zp_work] <= dataframe$laboral.fin1[ind_zp_work]) | (dataframe$Hora_Pasada[ind_zp_work] >= dataframe$laboral.ini2[ind_zp_work] & dataframe$Hora_Pasada[ind_zp_work] <= dataframe$laboral.fin2[ind_zp_work]),"Z","P")
# dataframe$TP[ind_zp_sat] <- ifelse(dataframe$Hora_Pasada[ind_zp_sat] >= dataframe$sabado.ini1[ind_zp_sat] & dataframe$Hora_Pasada[ind_zp_sat] <= dataframe$sabado.fin1[ind_zp_sat],"Z","P")
# dataframe$TP[ind_zp_sun] <- ifelse(dataframe$Hora_Pasada[ind_zp_sun] >= dataframe$domingo.ini1[ind_zp_sun] & dataframe$Hora_Pasada[ind_zp_sun] <= dataframe$sabado.fin1[ind_zp_sun],"Z","P")
# 
# #Deleting "GENTE EN EL BUS DESPUÉS DE ÚLTIMA PARADA"
# ind_ultimo <- which(dataframe$Nombre_Paradero == "GENTE EN EL BUS DESPUÉS DE ÚLTIMA PARADA")
# dataframe <- dataframe[-ind_ultimo,]
# 
# write.csv(dataframe,file = "perfiles_edit.csv", row.names = FALSE)
# 
# 
# #Collapsing dataframe
# perfiles <- read.csv(file = "perfiles_edit.csv", header = TRUE, sep = ",")
# 

#Working with: ############################ MERGE PERFILES 2017 Y BBDD ZP ###############################











# #Working with: ############################ MERGE WITH TURNSTILE ###############################
# 
# #Creating dataframe
# dataframe <- data.frame()
# 
# #Setting working space
# setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/01_SSH")
# 
# #Getting files names in the directory
# file_name <- list.files()
# 
# for (i in file_name) {
#   
#   #reading files
#   perfiles <- read.csv(gzfile(i), sep = "|", header = TRUE)
#   
#   #Subsetting perfiles by route number
#   perfiles <- perfiles[grepl(paste(route, collapse = "|"), perfiles$ServicioSentido),]
#   
# 
#   #Collapsing the table by idExpedition
#   dframe <- data.table(perfiles)
#   dframe <- dframe[, list(Subidastotal = sum(Subidastotal),
#                           Bajadastotal = sum(Bajadastotal),
#                           SubidasExpandidas = sum(SubidasExpandidas),
#                           BajadasExpandidas = sum(BajadasExpandidas)), by= list(ServicioSentido,
#                                                                                 Patente,
#                                                                                 PeriodoTSExpedicion,
#                                                                                 idExpedicion,
#                                                                                 Hini,
#                                                                                 Hfin)]
#   
#   #Adding time and date variables
#   dframe$Date <- as.Date(dframe$Hini)
#   dframe$ti <- format(as.POSIXct(dframe$Hini) ,format = "%H:%M:%S")
#   dframe$tf <- format(as.POSIXct(dframe$Hfin) ,format = "%H:%M:%S")
#   
#   #Adding half hour of the day
#   dframe$media_hora <- 2*hour(hms(dframe$ti)) + ifelse(minute(hms(dframe$ti)) < 30,1,2)
#   
#   #Adding weekday (Staring from Sunday: 0) and number of the week
#   dframe$wday <- wday(dframe$Date)
#   dframe$weekday <- weekdays(dframe$Date)
#   dframe$nweek <- strftime(dframe$Date,format="%W") 
#   
#   
#   #Adding expedition time
#   dframe$texpedicion <- period_to_seconds(hms(dframe$tf) - hms(dframe$ti))/60
#   
#   #Adding expedition time to negative values
#   dframe_neg <- dframe[which(dframe$texpedicion < 0),]
#   
#   dframe_neg$ti_0 <- hms("23:59:59") - hms(dframe_neg$ti)
#   dframe_neg$tf_1 <- hms(dframe_neg$tf) - hms("00:00:00")
#   dframe_neg$texp_corr <- dframe_neg$ti_0 + dframe_neg$tf_1
#   
#   dframe$texpedicion[which(dframe$texpedicion < 0)] <- period_to_seconds(dframe_neg$texp_corr)/60
#   
#   
#   #Adding turnstile information.
#   dframe <- merge(dframe, torn_marip, by= "Patente", all.x = TRUE)
#   dframe <- merge(dframe, torniquete, by= "Patente", all.x = TRUE)
#   
#   
#   #Turnstile during the expedition?
#   dframe$turnstile[is.na(dframe$Instalacion) & is.na(dframe$Fecha_mariposa)] <- 0
#   dframe$turnstile_marip[is.na(dframe$Instalacion) & is.na(dframe$Fecha_mariposa)] <- 0
#   
#   #Indexes
#   ind_na <- which(is.na(dframe$turnstile))
# 
#   #Turnstile during the expedition?
#   dframe$turnstile[ind_na] <- ifelse(dframe$Date[ind_na] > pmin(dframe$Fecha_mariposa[ind_na],dframe$Instalacion[ind_na],na.rm = TRUE),1,0)
#   
#   #Turnstile during the expedition? 2017 style
#   dframe$turnstile_marip[ind_na] <- ifelse(dframe$Date[ind_na] > dframe$Fecha_mariposa[ind_na],1,0)
#   dframe$turnstile_marip[is.na(dframe$turnstile_marip)] <- 0
#   
#   #Combining days
#   dataframe <- rbind(dataframe,dframe)
#   
# }
# 
# write.csv(dataframe, file = "perfiles.csv", row.names = FALSE)
# 
# 
# #Working with: ############################ MERGE WITH TURNSTILE ###############################



