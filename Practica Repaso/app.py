from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="DB_Fruteria"

app.secret_key='mysecretkey'
mysql= MySQL(app)

#Declaramos una ruta
#ruta Index http://localhost:5000
#ruta se compone de nombre y funcion
@app.route('/')
def index():
    #print(consulta)
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vfruta = request.form['txtFruta']
        Vatemp = request.form['txtTemporada']
        Vpr = request.form['txtPrecio']
        Vst = request.form['txtStock']
        #print(titulo, artista, anio)
        
        #Conectamos y ejecutamos el Insert
        CS = mysql.connection.cursor()
        CS.execute('insert into tbFrutas (fruta,temporada,precio,stock) values (%s,%s,%s,%s)',(Vfruta,Vatemp,Vpr,Vst))
        mysql.connection.commit()
    flash('Fruta Agregada Correctamente :)')
    return redirect(url_for('index'))
@app.route('/frutas')
def frutas():
    curselect = mysql.connection.cursor()
    curselect.execute('select * from tbFrutas')
    consulta= curselect.fetchall()
    return render_template('Frutas.html',listAlbums=consulta)



    


@app.route('/editar/<id>')
def editar(id):
    cureditar = mysql.connection.cursor()
    cureditar.execute('select * from tbFrutas where id = %s',(id,))
    consulId = cureditar.fetchone()
    
    return render_template('editarFruta.html', consulId=consulId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        Vfruta = request.form['txtFruta']
        Vatemp = request.form['txtTemporada']
        Vpr = request.form['txtPrecio']
        Vst = request.form['txtStock']
        
        CS = mysql.connection.cursor()
        CS.execute('update tbFrutas set fruta =%s ,temporada = %s ,precio = %s ,stock = %s where id = %s',(Vfruta,Vatemp,Vpr,Vst,id))
        mysql.connection.commit()
        
    flash('Album Actualizado en BD :)')
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    cureditar = mysql.connection.cursor()
    cureditar.execute('select * from tbFrutas where id = %s',(id,))
    consulId = cureditar.fetchone()
    
    return render_template('eliminarFruta.html', consulId=consulId)

@app.route('/eliminaralb/<id>', methods=['POST'])
def eliminaralb(id):
    if request.method == 'POST':
        
        CS = mysql.connection.cursor()
        CS.execute('delete from tbFrutas  where id = %s',(id,))
        mysql.connection.commit()
        
    flash('Fruta Eliminada en BD :)')
    return redirect(url_for('index'))


@app.route('/consultar')
def consultar():
    return render_template('buscarFruta.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST':
        Vfruta = request.form['txtFrut']
        
        curselect = mysql.connection.cursor()
        if not Vfruta:  # Si no se ingresa ningún nombre de fruta
            curselect.execute('SELECT * FROM tbFrutas')
        else:
            curselect.execute('SELECT * FROM tbFrutas WHERE fruta = %s', (Vfruta,))
        consulta = curselect.fetchall()
    
        if consulta is not None:
            return render_template('buscarFruta.html', frutas=consulta)
        else:
            mensaje = 'No se encontraron resultados para la fruta ingresada.'
            return render_template('buscarFruta.html', mensaje=mensaje)
    
    

#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=2000,debug=True)
