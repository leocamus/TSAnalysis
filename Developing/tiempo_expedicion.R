

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
          "chron",
          "ggplot2",
          "ggpubr",
          "gridExtra")

getLibraries(libs)

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/")

#Creating dataframe
dataframe <- data.frame()

#reading files
route <- as.vector(read.csv(file = "recorridos.csv", sep = ",", header = FALSE)[,])
torn_marip <- read.csv(file = "torniquetes_mariposa.csv", header = TRUE, sep = ";")
torniquete <- read.csv(file = "torniquetes.csv", header = TRUE, sep = ";")
torniquete <- torniquete[,1:2]

#Changing class variable
names(torn_marip)[3] <- "Fecha_mariposa"

torniquete$Instalacion <- as.Date(torniquete$Instalacion)
torn_marip$Fecha_mariposa <- as.Date(torn_marip$Fecha_mariposa)

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/01_SSH")

#Getting files names in the directory
file_name <- list.files()

for (i in file_name) {
  
  #reading files
  perfiles <- read.csv(gzfile(i), sep = "|", header = TRUE)
  
  #Subsetting perfiles by route number
  perfiles <- perfiles[grepl(paste(route, collapse = "|"), perfiles$ServicioSentido),]
  

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
  
  #Adding half hour of the day
  dframe$media_hora <- 2*hour(hms(dframe$ti)) + ifelse(minute(hms(dframe$ti)) < 30,1,2)
  
  #Adding weekday (Staring from Sunday: 0)
  dframe$wday <- wday(dframe$Date)
  dframe$weekday <- weekdays(dframe$Date)
  
  
  #Adding expedition time
  dframe$texpedicion <- period_to_seconds(hms(dframe$tf) - hms(dframe$ti))/60
  
  #Adding expedition time to negative values
  dframe_neg <- dframe[which(dframe$texpedicion < 0),]
  
  dframe_neg$ti_0 <- hms("23:59:59") - hms(dframe_neg$ti)
  dframe_neg$tf_1 <- hms(dframe_neg$tf) - hms("00:00:00")
  dframe_neg$texp_corr <- dframe_neg$ti_0 + dframe_neg$tf_1
  
  dframe$texpedicion[which(dframe$texpedicion < 0)] <- period_to_seconds(dframe_neg$texp_corr)/60
  
  
  
  #Adding turnstile information.
  dframe <- merge(dframe, torn_marip, by= "Patente", all.x = TRUE)
  dframe <- merge(dframe, torniquete, by= "Patente", all.x = TRUE)
  
  
  #Turnstile during the expedition?
  dframe$turnstile[is.na(dframe$Instalacion) & is.na(dframe$Fecha_mariposa)] <- 0
  dframe$turnstile_marip[is.na(dframe$Instalacion) & is.na(dframe$Fecha_mariposa)] <- 0
  
  #Indexes
  ind_na <- which(is.na(dframe$turnstile))

  #Turnstile during the expedition?
  dframe$turnstile[ind_na] <- ifelse(dframe$Date[ind_na] > pmin(dframe$Fecha_mariposa[ind_na],dframe$Instalacion[ind_na],na.rm = TRUE),1,0)
  
  #Turnstile during the expedition? 2017 style
  dframe$turnstile_marip[ind_na] <- ifelse(dframe$Date[ind_na] > dframe$Fecha_mariposa[ind_na],1,0)
  dframe$turnstile_marip[is.na(dframe$turnstile_marip)] <- 0
  
  #Combining days
  dataframe <- rbind(dataframe,dframe)
  
}

#Saving as original dataframe
dataframe_orig <- dataframe

#Changing class
dataframe$weekday <- factor(dataframe$weekday, levels = unique(dataframe$weekday))

#Expedition time analysis
#We split the data into several dataframe by bus line and time period.
expediciones <- split(dataframe, list(dataframe$ServicioSentido, dataframe$PeriodoTSExpedicion))

#Deleting dataframe without data
expediciones <- Filter(function(x) dim(x)[1] > 0, expediciones)



#Boxplot per dataframe
boxplot_exp <- lapply(expediciones, 
                      FUN = function(dataframe){
                        
                        #Subsetting dataframe by turnstile usage
                        dataframe_st <- subset(dataframe, dataframe$turnstile == 0)
                        dataframe_ct <- subset(dataframe, dataframe$turnstile_marip == 1)
                        
                        if(nrow(dataframe_st) > 0 & nrow(dataframe_ct) > 0){
                          
                          #Combining two datasets
                          dataset <- rbind(dataframe_ct,dataframe_st)
                          dataset$categoria <- c(rep("C/T", nrow(dataframe_ct)),rep("S/T",nrow(dataframe_st)))
                          
                          # pdf(file = paste(unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), ".pdf", sep = ""), 10,5)
                          
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
                            theme(legend.position = c(0.095,0.92),
                                  legend.title = element_blank(),
                                  axis.text.x = element_blank()) +
                            coord_cartesian(ylim = c(min(dataframe_ct$texpedicion,dataframe_st$texpedicion), max(dataframe_ct$texpedicion,dataframe_st$texpedicion))) +
                            ggtitle("Dataset")
                          
                          
                          #Plotting
                          grid.arrange(b1, b2, p1, ncol = 3, nrow = 1, widths=c(1,1,2.5), top= paste(unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), sep = ""))
                          
                          # dev.off()
                          
                          
                          
                          
                          #Creating boxplot per day
                          if(length(unique(dataframe_ct$wday)) == 5 & length(unique(dataframe_st$wday)) == 5){
                            
                            # pdf(file = paste("BOX_SEMANA - ",unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), ".pdf", sep = ""), 10,5)
                            
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
                            grid.arrange(b1, b2, ncol = 2, nrow = 1, widths=c(1,1.2), top= paste(unique(dataframe$ServicioSentido),"-",unique(dataframe$PeriodoTSExpedicion), sep = ""))
                            
                            
                            # dev.off()
                            
                          }
                          
                          
                          
                          
                          
                          
                        }
                      })



  #Adding next day
  
  
  #Analyzing by day type
  
  
  #
  
  
  
  
  
                          
                          
                          
                          

          
                          
                          
                          
                          # #Identifying outliers
                          # boxplot_out <- boxplot.stats(dataframe$texpedicion, coef = 1.5)
                          # 
                          # #Identifying extreme values
                          # boxplot_extreme <- boxplot.stats(dataframe$texpedicion, coef = 3)
                          # 
                          # #Deleting outliers and extreme values
                          # dtframe_out <- subset(dataframe, !(dataframe$texpedicion %in% boxplot_out$out))
                          # dtframe_extreme <- subset(dataframe, !(dataframe$texpedicion %in% boxplot_extreme$out))
                          # 
                          # #Boxplot and observations without extreme values
                          # boxplot(dtframe_extreme$texpedicion, main="Without extreme values")
                          # plot(1:nrow(dtframe_extreme), dtframe_extreme$texpedicion, xlab = "Observations", ylab = "Expedition Time (min)")
                          # 
                          # #Boxplot and points without outliers
                          # boxplot(dtframe_out$texpedicion, main="Without outliers")
                          # plot(1:nrow(dtframe_out), dtframe_out$texpedicion, xlab = "Observations", ylab = "Expedition Time (min)")
                          # title(paste(unique(dataframe$ServicioSentido),unique(dataframe$PeriodoTSExpedicion), sep = "-"), outer=TRUE)
                          # 
                          #dev.off()
                          
                        })
  
  
  








