from flask import Flask, render_template,request, redirect, url_for, flash
from flask_mysqldb import MySQL


# Inicializacion del servidor Flask 
app= Flask(__name__)

#configuracion para la conexion a BD
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= ""
app.config['MYSQL_DB']= "dbflask"

app.secret_key='mysecretkey'

mysql= MySQL(app)
#Declaracion de ruta 

#ruta Index o ruta principal  http://localhost:5000
# ruta se compone de nombre y funcion 
@app.route('/')
def index():
    curSelect = mysql.connection.cursor()
    curSelect.execute('select * from albums')
    consulta = curSelect.fetchall()
    #print(consulta)
    
    return render_template('index.html', listAlbums = consulta)

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vanio = request.form['txtAnio']
        #print(titulo, artista, anio)
        cs = mysql.connection.cursor()
        cs.execute('insert into albums (titulo, artista, anio) values(%s,%s,%s)', (Vtitulo,Vartista, Vanio))    
        mysql.connection.commit()
        
    flash('Album agregado correctamente :)')
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('select * from albums where id= %s', (id,))
    consulId = curEditar.fetchone()
    return render_template('EditarAlbum.html', album = consulId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vanio = request.form['txtAnio']
        
        curAct = mysql.connection.cursor()
        curAct.execute('update albums set titulo=%s, artista=%s, anio=%s where id=%s', (Vtitulo, Vartista, Vanio, id))
        mysql.connection.commit()
        
    flash('Album actualizado en BD :)')
    return redirect(url_for('index'))


@app.route('/borrar/<id>')
def borrar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('select * from albums where id= %s', (id,))
    consulId = curEditar.fetchone()
    return render_template('EliminarAlbum.html', album = consulId)

@app.route('/eliminar/<id>', methods=['POST'])
def eliminar(id):
    if request.method == 'POST':
        curEli = mysql.connection.cursor()
        curEli.execute('delete from albums where id=%s', (id,))
        mysql.connection.commit()
        flash('El álbum ha sido eliminado :)')
    return redirect(url_for('index'))

#Ejecucion
if __name__ == '__main__':
    app.run(port=3000, debug=True)
    app 