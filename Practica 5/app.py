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
    curselect = mysql.connection.cursor()
    curselect.execute('select * from albums')
    consulta= curselect.fetchall()
    #print(consulta)
    return render_template('index.html',listAlbums=consulta)

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

@app.route('/editar/<id>')
def editar(id):
    cureditar = mysql.connection.cursor()
    cureditar.execute('select * from albums where id = %s',(id,))
    consulId = cureditar.fetchone()
    
    return render_template('editarAlbum.html', consulId=consulId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vanio = request.form['txtAnio']
        
        CS = mysql.connection.cursor()
        CS.execute('update albums set titulo = %s, artista = %s, anio = %s where id = %s',(Vtitulo,Vartista,Vanio,id))
        mysql.connection.commit()
        
    flash('Album Actualizado en BD :)')
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    cureditar = mysql.connection.cursor()
    cureditar.execute('select * from albums where id = %s',(id,))
    consulId = cureditar.fetchone()
    
    return render_template('eliminarAlbum.html', consulId=consulId)

@app.route('/eliminaralb/<id>', methods=['POST'])
def eliminaralb(id):
    if request.method == 'POST':
        
        CS = mysql.connection.cursor()
        CS.execute('delete from albums  where id = %s',(id,))
        mysql.connection.commit()
        
    flash('Album Eliminado en BD :)')
    return redirect(url_for('index'))
#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=5000,debug=True)

