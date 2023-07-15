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
<<<<<<< HEAD
    curSelect = mysql.connection.cursor()
    curSelect.execute('select * from albums')
    consulta = curSelect.fetchall()
    #print(consulta)
    
    return render_template('index.html', listAlbums = consulta)
=======
    curselect = mysql.connection.cursor()
    curselect.execute('select * from albums')
    consulta= curselect.fetchall()
    #print(consulta)
    return render_template('index.html',listAlbums=consulta)
>>>>>>> bdef582b99df0870b13c58f952af519aa754554f

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

<<<<<<< HEAD

@app.route('/eliminar')
def eliminar():
    return "Se elimino"

#Ejecucion
if __name__ == '__main__':
    app.run(port=5000, debug=True)
=======
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

>>>>>>> bdef582b99df0870b13c58f952af519aa754554f
