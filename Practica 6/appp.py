from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from functools import wraps
from flask_bcrypt import Bcrypt 
app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "COnsultorio"

app.secret_key = 'mysecretkey'
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el correo electrónico está almacenado en la sesión
        if 'RFC' not in session:
            # Redirigir al inicio de sesión si no ha iniciado sesión
            flash('Debe iniciar sesión para acceder a esta página.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

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
    
    
    if resultado is not None:
        Rol = "select Rol from admin where RFC = %s AND contraseña = %s"
        CS.execute(Rol, (VRFC, VPass))
        rol_resultado = CS.fetchone()

        if rol_resultado is not None and rol_resultado[0] == "Administrador":
            session['RFC'] = VRFC
            return render_template('Menuadmin.html')
        else:
            session['RFC'] = VRFC
            return render_template('Menu.html')
    else:
        flash('RFC o contraseña incorrectos. Intente nuevamente.')
        return redirect(url_for('index'))

@app.route('/menu', methods=['GET'])
@login_required
def menu():
    return render_template('Menu.html')

@app.route('/menuadmin', methods=['GET'])
@login_required
def menuadmin():
    return render_template('Menuadmin.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
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
@login_required
def regpaciente():
    user_id = session.get('RFC')
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
    CS.execute('SELECT RFC, concat(Nombre, " ", Apellidopa, " ",Apellidoma) as Nombrec FROM admin where RFC = %s',(user_id,))
    medicos = CS.fetchall()
    return render_template('RegPaciente.html', medicos=medicos)

@app.route('/receta/<id>', methods=['GET'])
def receta(id):
    user_id = session.get('RFC')
    CS = mysql.connection.cursor()
    CS.execute('''
        SELECT ed.Id_exp,
            CONCAT(rp.Nombre, " ", rp.Apellidopa, " ", rp.Apellidoma),
            CONCAT(m.Nombre, " ", m.Apellidopa, " ", m.Apellidoma),
            ed.Fecha, ed.Peso, ed.Altura, ed.Temperatura, ed.Latidos, ed.Oxigeno, ed.Edad, ed.Sintomas, ed.DX, ed.Tratamiento
        FROM exploracion_diagnostico ed
        JOIN registro_paciente rp ON ed.Id_paciente = rp.Id_paciente
        JOIN admin m ON ed.Medico_id = m.RFC
        WHERE ed.Id_exp=%s and m.RFC = %s
    ''', (id,user_id,))
    medicos = CS.fetchall()

    return render_template('Receta.html', medicos=medicos)

@app.route('/ced', methods=['GET', 'POST'])
@login_required
def ced():
    user_id=session.get('RFC')
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
        CS.execute('INSERT INTO exploracion_diagnostico (Id_paciente, Medico_id, Fecha, Peso, Altura, Temperatura, Latidos, Oxigeno, Edad, Sintomas, DX, Tratamiento) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (VPacID, user_id, VNom, VPes, VAP, VAM, VNac, VEnf, VED, VAlr, VAnt, VTrat))
        mysql.connection.commit()
        flash('Se ha registrado la consulta')
        return redirect(url_for('cons_cit'))
    CS = mysql.connection.cursor()
    CS.execute('SELECT Id_paciente, concat(Nombre, " ", Apellidopa, " ",Apellidoma) as Nombrec FROM registro_paciente')
    pacientes = CS.fetchall()
    return render_template('Citas_Exp_Diagn.html', pacientes=pacientes)


@app.route('/cons_med', methods=['GET', 'POST'])
@login_required
def cons_med():
    if request.method == 'POST':
        VBusc = request.form['busc']
        
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT RFC, concat (Nombre," ", Apellidopa," ", ApellidoMa), Cedula, Correo, Rol FROM admin')

        else:
            cursorBU.execute('SELECT RFC, concat (Nombre," ", Apellidopa," ", ApellidoMa), Cedula, Correo, Rol FROM admin  WHERE Nombre = %s', (VBusc,))
        consBP = cursorBU.fetchall() 
        if consBP is not None:
            return render_template('MEDICOS.html', medicos=consBP)
        else:
            return render_template('MEDICOS.html')
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT RFC, concat (Nombre," ", Apellidopa," ", ApellidoMa), Cedula, Correo, Rol FROM admin')
    consBU = cursorBU.fetchall()
    return render_template('MEDICOS.html', medicos=consBU)
@app.route('/visualizarActcm/<string:id>')
@login_required
def visualizarm(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('select * from admin where RFC = %s', (id,))
    visualisarDatos = cursorVis.fetchone()
    return render_template('act.html', UpdUsuario = visualisarDatos)



@app.route('/actualizarm/<id>', methods=['POST'])
@login_required
def actualizarm(id):
    if request.method == 'POST':
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VCed = request.form['txtCed']
        VCorr = request.form['txtCorr']
        VRol = request.form['txtRol']
        cursorUpd = mysql.connection.cursor()
        cursorUpd.execute('update admin set Nombre = %s, Apellidopa = %s, Apellidoma = %s, Cedula = %s, Correo = %s, Rol = %s where RFC = %s', (VNom, VAP, VAM, VCed, VCorr, VRol, id,))
        mysql.connection.commit()
    flash ('El medico se actualizo correctamente.')
    return redirect(url_for('cons_med'))

@app.route("/confirmacion/<id>")
@login_required
def eliminar(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from admin where RFC = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('elm.html', usuario=consuUsuario)

@app.route("/eliminar/<id>", methods=['POST'])
@login_required
def eliminarBD(id):
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from registro_paciente where Medico_id = %s', (id,))
    mysql.connection.commit()
    
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from admin where RFC = %s', (id,))
    mysql.connection.commit()
    flash('Se elimino el medico con RFC'+ id)
    return redirect(url_for('cons_med'))

@app.route('/cons_pac', methods=['GET', 'POST'])
@login_required
def cons_pac():
    user_id = session.get('RFC')
    if request.method == 'POST':
        VBusc = request.form['busc']
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT Id_paciente, CONCAT(Nombre, " ", Apellidopa, " ", Apellidoma), Fecha_nacimiento, Enfermedades, Alergias, Antecedentes_familiares FROM registro_paciente where Medico_id =%s',(user_id,))

        else:
            cursorBU.execute('SELECT Id_paciente, CONCAT(Nombre, " ", Apellidopa, " ", Apellidoma), Fecha_nacimiento, Enfermedades, Alergias, Antecedentes_familiares FROM registro_paciente where Medico_id =%s and Nombre = %s',(user_id, VBusc,))
        consBP = cursorBU.fetchall() 
        if consBP is not None:
            return render_template('PACIENTESS.html', medicos=consBP)
        else:
            return render_template('PACIENTESS.html')       
    CS = mysql.connection.cursor()
    CS.execute('SELECT Id_paciente, CONCAT(Nombre, " ", Apellidopa, " ", Apellidoma), Fecha_nacimiento, Enfermedades, Alergias, Antecedentes_familiares FROM registro_paciente where Medico_id=%s',(user_id,))
    medicos = CS.fetchall()
    
    return render_template('PACIENTESS.html', medicos=medicos)

@app.route('/cons_cit', methods=['GET', 'POST'])
@login_required
def cons_cit():
    user_id = session.get('RFC')

    if request.method == 'POST':
        VBusc = request.form['busc']
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('''
        SELECT
    ed.Id_exp,
    CONCAT(rp.Nombre, " ", rp.Apellidopa, " ", rp.Apellidoma) AS Nombre_Completo_Paciente,
    ed.Fecha
    FROM
    exploracion_diagnostico ed
    JOIN
    registro_paciente rp ON ed.Id_paciente = rp.Id_paciente
    WHERE ed.Medico_id  = %s
    ''',(user_id,))

        else:
            cursorBU.execute('''
        SELECT
    ed.Id_exp,
    CONCAT(rp.Nombre, " ", rp.Apellidopa, " ", rp.Apellidoma) AS Nombre_Completo_Paciente,
    ed.Fecha
    FROM
    exploracion_diagnostico ed
    JOIN
    registro_paciente rp ON ed.Id_paciente = rp.Id_paciente
    WHERE rp.Nombre =%s and ed.Medico_id  = %s
    ''',(VBusc, user_id, ))
        consBP = cursorBU.fetchall() 
        if consBP is not None:
            return render_template('Citas.html', medicos=consBP)
        else:
            return render_template('Citas.html')       
    query = '''
        SELECT
    ed.Id_exp,
    CONCAT(rp.Nombre, " ", rp.Apellidopa, " ", rp.Apellidoma) AS Nombre_Completo_Paciente,
    ed.Fecha
    FROM
    exploracion_diagnostico ed
    JOIN
    registro_paciente rp ON ed.Id_paciente = rp.Id_paciente
    WHERE ed.Medico_id  = %s
    '''

    CS = mysql.connection.cursor()
    CS.execute(query, (user_id,))
    medicos = CS.fetchall()

    return render_template('Citas.html', medicos=medicos)

@app.route('/cerrar')
def cerrar():
    # Eliminar el correo electrónico del usuario de la sesión
    session.pop('RFC', None)
    # Redirigir al usuario a la página de inicio de sesión
    return redirect(url_for('index'))

@app.route('/visualizarActcp/<string:id>')
@login_required
def visualizarp(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('select * from registro_paciente where Id_paciente = %s', (id,))
    visualisarDatos = cursorVis.fetchone()
    return render_template('actp.html', UpdUsuario = visualisarDatos)



@app.route('/actualizarp/<id>', methods=['POST'])
@login_required
def actualizarp(id):
    if request.method == 'POST':
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VNac = request.form['txtNac']
        VEnf = request.form['txtEnf']
        VAlr = request.form['txtAlg']
        VAnt = request.form['txtAnt']
        cursorUpd = mysql.connection.cursor()
        cursorUpd.execute('update registro_paciente set Nombre = %s, Apellidopa = %s, Apellidoma = %s, Fecha_nacimiento = %s, Enfermedades = %s, Alergias = %s, Antecedentes_familiares = %s where  Id_paciente = %s', ( VNom, VAP, VAM, VNac, VEnf, VAlr, VAnt, id,))
        mysql.connection.commit()
    flash ('El Paciente se actualizo correctamente.')
    return redirect(url_for('cons_pac'))

@app.route("/confirmacionp/<id>")
@login_required
def eliminarpp(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from registro_paciente where Id_paciente = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('elmp.html', usuario=consuUsuario)

@app.route("/eliminarp/<id>", methods=['POST'])
@login_required
def eliminarp(id):
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from registro_paciente where Id_paciente = %s', (id,))
    mysql.connection.commit()

    flash('Se elimino el Paciente')
    return redirect(url_for('cons_pac'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)