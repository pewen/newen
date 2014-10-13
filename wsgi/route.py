from flask import Flask, render_template, redirect, url_for, request, Response

#Para leer el archivo que subo
from werkzeug import secure_filename
#Para pasar el archivo a dataframe
from pandas import read_csv

from scipy import stats
from estadistica import file_path, r_analisis

#Path principal
path = '/home/franco/Desktop/Proyectos/Pewen/Vientos/vientos/wsgi/'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route("/get_file")
def get_file():
    f = open(path + 'data/datos3.csv', 'r')
    generator = f.readlines()

    return Response(generator,
                       mimetype="text/csv",
                       headers={"Content-Disposition":
                                    "attachment;filename=datos.csv"})

@app.route('/analisis', methods = ['GET', 'POST'])
def analisis():

  if request.method == 'POST':
  	# Get the FileStorage instance from request
    file = request.files['file']
    #Analisis estadistico
    new_path = file_path(file, path)
    df_anio, df_meses, histo_breaks, histo_counts = r_analisis(new_path)
    
    shape = df_anio['shape_year'][1]
    scale = df_anio['scale_year'][1]
    distribution = stats.exponweib(1, shape, loc = 0, scale = scale)

    y = distribution.pdf(histo_counts['mids'])
    
    data = []
    for i in range(8):
        data.append(df_meses[[i]].values.tolist())
    data.append(histo_breaks[[0]].values.tolist())
    for i in range(3):
        data.append(histo_counts[[i]].values.tolist())
    data.append(y.tolist())
    
    # Render template with file info
    return render_template('analisis.html', data = data)
            
  return render_template('upload.html')

if __name__ == "__main__":
    app.debug = True
    app.run()