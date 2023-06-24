from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbflask"

app.secret_key='mysecretkey'
mysql= MySQL(app)

#Declaramos una ruta
#ruta Index http://localhost:5000
#ruta se compone de nombre y funcion
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/menu')
def eliminar():
    return ""

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vanio = request.form['txtAnio']
        #print(titulo, artista, anio)
        
        #Conectamos y ejecutamos el Insert
        CS = mysql.connection.cursor()
        CS.execute('insert into albums (titulo,artista,anio) values (%s,%s,%s)',(Vtitulo,Vartista,Vanio))
        mysql.connection.commit()
    flash('Album Agregado Correctamente :)')
    return redirect(url_for('index'))

@app.route('/eliminar')
def eliminar():
    return "Se eliminó el album en la BD"
#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=5000,debug=True)