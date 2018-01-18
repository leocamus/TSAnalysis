
#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/01_SSH")

##Function to load libraries and install packages, if necessary
getLibraries <- function(libs) {
  
  for (lib in libs) {
    if(!lib %in% rownames(installed.packages())){install.packages(lib, repos = "http://cran.us.r-project.org")}
    library(as.character(lib), character.only = TRUE)
  }
}


libs <- c("data.table",
          "plyr",
          "lubridate",
          "chron")

getLibraries(libs)

#Getting files names in the directory
file_name <- list.files()


for (i in file_name) {
  #reading files
  perfiles <- read.csv(gzfile(i), sep = "|", header = TRUE)
  torniquete <- read.csv(file = "torniquetes.csv", header = TRUE, sep = ";")
  
  
  #Changing class variable
  torniquete <- torniquete[,1:2]
  names(torniquete)[2] <- "Instalacion"
  torniquete$Instalacion <- as.Date(torniquete$Instalacion)
  
  #Collapsing the table by idExpedition
  dframe <- data.table(perfiles)
  dframe <- dframe[, list(Subidastotal = sum(Subidastotal),
                          Bajadastotal = sum(Bajadastotal),
                          SubidasExpandidas = sum(SubidasExpandidas),
                          BajadasExpandidas = sum(BajadasExpandidas)), by= list(ServicioSentido,
                                                                                Patente,
                                                                                PeriodoTSExpedicion,
                                                                                idExpedicion,
                                                                                Hini,
                                                                                Hfin)]
  
  #Adding time and date variables
  dframe$Date <- as.Date(dframe$Hini)
  dframe$ti <- format(as.POSIXct(dframe$Hini) ,format = "%H:%M:%S")
  dframe$tf <- format(as.POSIXct(dframe$Hfin) ,format = "%H:%M:%S")
  
  
  #Adding expedition time
  dframe$texpedicion <- period_to_seconds(hms(dframe$tf) - hms(dframe$ti))/60
  
  #Adding expedition time to negative values
  dframe_neg <- dframe[which(dframe$texpedicion < 0),]
  
  dframe_neg$ti_0 <- hms("23:59:59") - hms(dframe_neg$ti)
  dframe_neg$tf_1 <- hms(dframe_neg$tf) - hms("00:00:00")
  dframe_neg$texp_corr <- dframe_neg$ti_0 + dframe_neg$tf_1
  
  dframe$texpedicion[which(dframe$texpedicion < 0)] <- period_to_seconds(dframe_neg$texp_corr)/60
  
  #Adding turnstile information.
  dframe <- merge(dframe, torniquete, by= "Patente", all.x = TRUE)
  
  #Keeping 2017 turnstile style
  dframe <- subset(dframe, is.na(dframe$Instalacion) | year(dframe$Instalacion) == 2017)
  
  #Turnstile during the expedition?
  dframe$turnstile[is.na(dframe$Instalacion)] <- 0
  dframe$turnstile[which(dframe$Date >= dframe$Instalacion)] <- 1
  dframe$turnstile[which(dframe$Date < dframe$Instalacion)] <- 0
  
  
  
  ###############################
  
  
  
  #Expedition time analysis
  #We split the data into several dataframe by bus line and time period.
  expediciones <- split(dframe, list(dframe$ServicioSentido, dframe$PeriodoTSExpedicion))
  
  #Deleting dataframe without data
  expediciones <- Filter(function(x) dim(x)[1] > 0, expediciones)
  
  #Boxplot per dataframe
  exped_s_out <- lapply(expediciones, 
                        FUN = function(dataframe){
                          
                          pdf(file = paste(unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), ".pdf", sep = ""))
                          
                          #Plot frame
                          par(mfrow=c(3, 2), oma=c(0,0,3,0))
                          
                          #Boxplot and points with extreme values
                          boxplot(dataframe$texpedicion, main="Full data")
                          plot(1:nrow(dataframe), dataframe$texpedicion, xlab = "Observations", ylab = "Expedition Time (min)")
                          
                          #Identifying outliers
                          boxplot_out <- boxplot.stats(dataframe$texpedicion, coef = 1.5)
                          
                          #Identifying extreme values
                          boxplot_extreme <- boxplot.stats(dataframe$texpedicion, coef = 3)
                          
                          #Deleting outliers and extreme values
                          dtframe_out <- subset(dataframe, !(dataframe$texpedicion %in% boxplot_out$out))
                          dtframe_extreme <- subset(dataframe, !(dataframe$texpedicion %in% boxplot_extreme$out))
                          
                          #Boxplot and observations without extreme values
                          boxplot(dtframe_extreme$texpedicion, main="Without extreme values")
                          plot(1:nrow(dtframe_extreme), dtframe_extreme$texpedicion, xlab = "Observations", ylab = "Expedition Time (min)")
                          
                          #Boxplot and points without outliers
                          boxplot(dtframe_out$texpedicion, main="Without outliers")
                          plot(1:nrow(dtframe_out), dtframe_out$texpedicion, xlab = "Observations", ylab = "Expedition Time (min)")
                          title(paste(unique(dataframe$ServicioSentido),unique(dataframe$PeriodoTSExpedicion), sep = "-"), outer=TRUE)
                          
                          dev.off()
                          
                        })
  
  
  
}







