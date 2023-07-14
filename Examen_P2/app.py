from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="DB_Floreria"

app.secret_key='mysecretkey'
mysql= MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vflor = request.form['txtFlor']
        VCant = request.form['txtCant']
        VPr = request.form['txtPrecio']

        CS = mysql.connection.cursor()
        CS.execute('insert into tbFlores (Nombre,Cantidad,Precio) values (%s,%s,%s)',(Vflor,VCant,VPr))
        mysql.connection.commit()
    flash('Flor Agregada Correctamente :)')
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    cureditar = mysql.connection.cursor()
    cureditar.execute('select * from tbFlores where id = %s',(id,))
    consulId = cureditar.fetchone()
    
    return render_template('editarFlor.html', consulId=consulId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        VFlor = request.form['txtFlor']
        VCant = request.form['txtCant']
        VPrec = request.form['txtPrec']
        
        CS = mysql.connection.cursor()
        CS.execute('update tbFlores set Nombre =%s ,Cantidad = %s ,Precio = %s where id = %s',(VFlor,VCant,VPrec,id))
        mysql.connection.commit()
        
    flash('Flor Actualizada en BD :)')
    return redirect(url_for('buscar'))

@app.route('/buscar', methods=['POST', 'GET'])
def buscar():
    
    if request.method == 'POST':
        VBusc = request.form['txtFlor']
        
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT * FROM tbFlores')
        else:
            cursorBU.execute('SELECT * FROM tbFlores WHERE Nombre = %s', (VBusc,))
        consBP = cursorBU.fetchall()
        
        if consBP is not None:
            return render_template('buscarFlor.html', Flores=consBP)
        else:
            mensaje = 'No se encontraron resultados.'
            return render_template('buscarFrlor.html', mensaje=mensaje)
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT * FROM tbFlores')
    consBP = cursorBU.fetchall()
    return render_template('buscarFlor.html', Frutas=consBP)
    
    



    
    

#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=2000,debug=True)
