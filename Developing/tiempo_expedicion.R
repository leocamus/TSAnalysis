
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

  #Expedition time analysis
  #Adding expedition time to negative values
  dframe_neg <- dframe[which(dframe$texpedicion < 0),]
  
  dframe_neg$ti_0 <- hms("23:59:59") - hms(dframe_neg$ti)
  dframe_neg$tf_1 <- hms(dframe_neg$tf) - hms("00:00:00")
  dframe_neg$texp_corr <- dframe_neg$ti_0 + dframe_neg$tf_1
  
  dframe$texpedicion[which(dframe$texpedicion < 0)] <- period_to_seconds(dframe_neg$texp_corr)/60
                                                                                                                          
  #Boxplot
  boxplot_texp <- boxplot.stats(dframe$texpedicion, coef = 3)
  
  #Saving table
  

  
}







