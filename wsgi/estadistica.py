#para pasar el datashet de R a pandas.
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import pandas.rpy.common as com
#Lo uso para saber el tiempo en seg y crear un archivo unico
import time
from werkzeug import secure_filename
#Leer y guardar csv
from pandas import read_csv


#Para poder usar funciones de R
base = importr('base')
fitdistrplus = importr('fitdistrplus')
r = robjects.r

def file_path(file, path):
	time_now = str(time.time())
	(time_sec, a) = time_now.split('.')
	
	filename = secure_filename(file.filename)
	(name, ext) = filename.split('.')
	
	new_path = path + 'data/' + name + '--' + time_sec + '.' + ext
	df = read_csv(file, header = 0)
	df.to_csv(new_path, header = True, index = False)
	
	return(new_path)
	
def r_analisis(path):
    r('''
        regresion <- function(path) {
            myData <- read.csv(path, header = TRUE)
            names(myData)[1] <- "Fecha"
            names(myData)[2] <- "VelViento"
            myData$time <-strptime(myData$Fecha, "%d-%m-%Y %H:%M")

            fit_year <- fitdist(myData$VelViento, "weibull")

            shape <- c()
            scale <- c()
            error_shape <- c()
            error_scale <- c()
            vel_min <- c()
            vel_max <- c()
            vel_prom <- c()

            for(i in 0:11){

              fit <- fitdist(myData$VelViento[myData$time$mon == i], "weibull") 
              shape <- c(shape, fit$estimate[1])
              scale <- c(scale, fit$estimate[2])
              error_shape <- c(error_shape, fit$sd[1])
              error_scale <- c(error_scale, fit$sd[2])
              vel_min <- c(vel_min, min(myData$VelViento[myData$time$mon == i]))
              vel_max <- c(vel_max, max(myData$VelViento[myData$time$mon == i]))
              vel_prom <- c(vel_prom, mean(myData$VelViento[myData$time$mon == i]))
            }

            mes <- c(1:12)

            dt_meses <<- data.frame(mes, shape, scale, error_shape, 
                                  error_scale, vel_max, vel_min, vel_prom)

            shape_year <- c(fit_year$estimate[1], fit_year$sd[1])
            scale_year <- c(fit_year$estimate[2],fit_year$sd[2])

            dt_anio <<- data.frame(shape_year, scale_year)
            
            his <<- hist(myData$VelViento, plot = FALSE)
            histo_breaks <<- data.frame(breaks = his$breaks)
            histo_counts <<- data.frame(counts = his$counts, density = his$density, mids = his$mids)
        }
    ''')
    
    r_regresion = r['regresion']
    r_regresion(path)
    
    df_meses = com.load_data('dt_meses')
    df_anio = com.load_data('dt_anio')
    histo_breaks = com.load_data('histo_breaks')
    histo_counts = com.load_data('histo_counts')

    return(df_anio, df_meses, histo_breaks, histo_counts)
