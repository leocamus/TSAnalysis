### SETTING THE .here FILE TO A LOCATION - DO NOT CHANGE OR TRY TO RUN THIS ###
## THE .here FILE IS INTENDED TO BE COMMITTED TO TSAnalysis REPO IN ORDER TO BE USED IN OTHER PC'S ##
## I think this isn't really necessary if TSAnalysis.Rproj is used ... ##
library("here")
personal_wd <- getwd()
set_here(personal_wd)