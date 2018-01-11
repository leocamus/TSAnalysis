

#Setting working space
setwd("/Users/diego/Desktop/Evasion/01_analisis/03_datos/01_SSH")


##Function to load libraries and install packages, if necessary
getLibraries <- function(libs) {
  
  for (lib in libs) {
    if(!lib %in% rownames(installed.packages())){install.packages(lib, repos = "http://cran.us.r-project.org")}
    library(as.character(lib), character.only = TRUE)
  }
}

libs <- c("data.table")

getLibraries(libs)

#etapas <- read.csv("2017-03-13.etapas", sep = "|", header = TRUE, nrows = 1000000)
#viajes <- read.csv("2017-03-13.viajes", sep = "|", header = TRUE, nrows = 1000000)

#Loading input files
perfiles <- read.csv("2017-03-13.perfiles", sep = "|", header = TRUE, nrows = 1000001)

#Splitting the data frame into several data frames based on idExpedicion
perfiles$idExpedicion <- factor(perfiles$idExpedicion, levels = unique(perfiles$idExpedicion))

#Sample
expedicion_sample <- subset(perfiles, perfiles$idExpedicion == 0 | perfiles$idExpedicion == 1)

dframe <- data.table(expedicion_sample, key = "idExpedicion")

dframe <- dframe[, list(ServicioSentido = unique(ServicioSentido),
                        Subidastotal = sum(Subidastotal),
                        Bajadastotal = sum(Bajadastotal),
                        Patente = unique(Patente),
                        Hini = unique(Hini),
                        Hfin = unique(Hfin),
                        SubidasExpandidas = sum(SubidasExpandidas),
                        BajadasExpandidas = sum(BajadasExpandidas)), by= idExpedicion]
