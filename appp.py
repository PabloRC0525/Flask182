from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="COnsultorio"

app.secret_key='mysecretkey'
mysql= MySQL(app)

#Declaramos una ruta
#ruta Index http://localhost:5000
#ruta se compone de nombre y funcion
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    VRFC = request.form['txtRFC']
    VPass = request.form['txtPass']
    
    # Conectamos a la base de datos
    CS = mysql.connection.cursor()
    
    # Verificar las credenciales en la base de datos
    consulta = "SELECT RFC FROM admin WHERE RFC = %s AND contraseña = %s"
    CS.execute(consulta, (VRFC, VPass, ))
    resultado = CS.fetchone()
    Rol = "select Rol from admin where RFC = %s AND contraseña = %s"
    
    # Verificar si las credenciales son válidas
    if resultado is not None:
        # Las credenciales son válidas, redirigir al menú principal
        CS.execute(Rol, (VRFC, VPass))
        rol_resultado = CS.fetchone()

        if rol_resultado is not None and rol_resultado[0] == "Administrador":
            # El usuario es administrador, redirigir al menú de administrador
            return render_template('Menuadmin.html')
        else:
            # El usuario no es administrador, redirigir al menú principal
            return render_template('Menu.html')
    else:
        # Las credenciales son inválidas, redirigir a la página de inicio de sesión con un mensaje de error
        flash('RFC o contraseña incorrectos. Intente nuevamente.')
        return redirect(url_for('index'))


@app.route('/menu', methods=['GET'])
def menu():
    return render_template('Menu.html')

@app.route('/menuadmin', methods=['GET'])
def menuadmin():
    return render_template('Menuadmin.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        VRFC = request.form['txtRFC']
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VCed = request.form['txtCed']
        VCorr = request.form['txtCorr']
        VRol = request.form['txtRol']
        VPass = request.form['txtPass']
        
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO admin (RFC, Nombre, Apellidopa, Apellidoma, Cedula, Correo, Rol, Contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (VRFC, VNom, VAP, VAM, VCed, VCorr, VRol, VPass))
        mysql.connection.commit()
        flash('Médico agregado correctamente')
        return redirect(url_for('menuadmin'))

    return render_template('Admin.html')

@app.route('/regpaciente', methods=['GET','POST'])
def regpaciente():
    if request.method == 'POST':
        VMed = request.form['txtMed']
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VNac = request.form['txtNac']
        VEnf = request.form['txtEnf']
        VAlr = request.form['txtAlr']
        VAnt = request.form['txtAnt']
        
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO registro_paciente (Medico_id, Nombre, Apellidopa, Apellidoma, Fecha_Nacimiento, Enfermedades, Alergias, Antecedentes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (VMed, VNom, VAP, VAM, VNac, VEnf, VAlr, VAnt))
        mysql.connection.commit()
        flash('Paciente registrado correctamente')
        return redirect(url_for('menu'))
    
    return render_template('RegPaciente.html')



@app.route('/ced')
def ced():
    # Código para procesar la página 'Admin'
    return render_template('Citas_exp_Diagn.html')
@app.route('/citas')
def citas():
    # Código para procesar la página 'Admin'
    return render_template('Citas.html')
#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=5000,debug=True)