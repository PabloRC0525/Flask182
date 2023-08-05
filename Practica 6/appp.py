from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "COnsultorio"

app.secret_key = 'mysecretkey'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    VRFC = request.form['txtRFC']
    VPass = request.form['txtPass']
    
    CS = mysql.connection.cursor()
    consulta = "SELECT RFC FROM admin WHERE RFC = %s AND contraseña = %s"
    CS.execute(consulta, (VRFC, VPass))
    resultado = CS.fetchone()
    Rol = "select Rol from admin where RFC = %s AND contraseña = %s"
    
    if resultado is not None:
        CS.execute(Rol, (VRFC, VPass))
        rol_resultado = CS.fetchone()

        if rol_resultado is not None and rol_resultado[0] == "Administrador":
            return render_template('Menuadmin.html')
        else:
            return render_template('Menu.html')
    else:
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
        return redirect(url_for('admin'))

    return render_template('Admin.html')

@app.route('/regpaciente', methods=['GET', 'POST'])
def regpaciente():
    if request.method == 'POST':
        VMed = request.form['txtMd']
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VNac = request.form['txtNac']
        VEnf = request.form['txtEnf']
        VAlr = request.form['txtAlg']
        VAnt = request.form['txtAnt']
        CS = mysql.connection.cursor()
        CS.execute(
            'INSERT INTO registro_paciente (Medico_id, Nombre, Apellidopa, Apellidoma, Fecha_Nacimiento, Enfermedades, Alergias, Antecedentes_familiares) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (VMed, VNom, VAP, VAM, VNac, VEnf, VAlr, VAnt))
        mysql.connection.commit()
        flash('Paciente registrado correctamente')
        return redirect(url_for('regpaciente'))

    CS = mysql.connection.cursor()
    CS.execute('SELECT ID, concat(Nombre, " ", Apellidopa, " ",Apellidoma) as Nombrec FROM admin')
    medicos = CS.fetchall()
    return render_template('RegPaciente.html', medicos=medicos)

@app.route('/ced', methods=['GET', 'POST'])
def ced():
    if request.method == 'POST':
        VPacID = request.form['txtID']
        VNom = request.form['txtDat']
        VPes = request.form['txtPes']
        VAP = request.form['txtAlt']
        VAM = request.form['txtTem']
        VNac = request.form['txtLPM']
        VEnf = request.form['txtOX']
        VED = request.form['txtED']
        VAlr = request.form['txtSint']
        VAnt = request.form['txtDig']
        VTrat = request.form['txtTrat']

        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO exploracion_diagnostico (Id_paciente, Fecha, Peso, Altura, Temperatura, Latidos, Oxigeno, Edad, Sintomas, DX, Tratamiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (VPacID, VNom, VPes, VAP, VAM, VNac, VEnf, VED, VAlr, VAnt, VTrat))
        mysql.connection.commit()
        flash('Se ha registrado la consulta')
        return redirect(url_for('ced'))
    CS = mysql.connection.cursor()
    CS.execute('SELECT Id_paciente, concat(Nombre, " ", Apellidopa, " ",Apellidoma) as Nombrec FROM registro_paciente')
    pacientes = CS.fetchall()
    return render_template('Citas_Exp_Diagn.html', pacientes=pacientes)

@app.route('/citas')
def citas():
    return render_template('Citas.html')

@app.route('/cons_med')
def cons_med():
    return render_template('MEDICOS.html')

@app.route('/cons_pac', methods=['GET', 'POST'])
def cons_pac():
    if request.method == 'POST':
        # Aquí puedes agregar la lógica para consultar pacientes según los checkboxes seleccionados
        pass
        
    CS = mysql.connection.cursor()
    CS.execute('SELECT ID, concat(Nombre, " ", Apellidopa, " ",Apellidoma) as Nombrec FROM admin')
    medicos = CS.fetchall()
    return render_template('PACIENTESS.html', medicos=medicos)

if __name__ == '__main__':
    app.run(port=5000, debug=True)