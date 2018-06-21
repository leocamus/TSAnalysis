### Utilities

## 0. Basics

# Function to load libraries and install packages, if necessary
getLibrary <- function(lib) {
  if(!lib %in% rownames(installed.packages())){
    install.packages(lib, repos = "http://cran.us.r-project.org")
    }
  library(as.character(lib), character.only = TRUE)
}

## 1. Paths.
getLibrary("here")
repo_path <- here::here()
data_dir <- file.path(dirname(dirname(repo_path)),"03_datos")

SSHDir = file.path(data_dir,"01_SSH")
TRXPPUDir = file.path(data_dir,"02_TRXPPU")
busesTorniqueteDir = file.path(data_dir,"03_BUSESTORNIQUETE")
DTPMDir = file.path(data_dir,"04_DTPM")
SummaryDir = file.path(data_dir,"05_SUMMARY")
RFADir = file.path(data_dir,"06_RFA")
DTPM_TRXDir = file.path(data_dir,"08_DTPM_TRX")

