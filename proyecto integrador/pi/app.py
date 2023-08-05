from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Base de datos temporal (se reemplazará con una base de datos real)
users_db = {}


@app.route('/')
def index():
    return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario de registro
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        matricula = request.form['matricula']
        correo_electronico = request.form['correo_electronico']
        contraseña = request.form['contraseña']

        # Guardar los datos del usuario en la base de datos temporal
        users_db[correo_electronico] = {
            'nombre': nombre,
            'apellido_paterno': apellido_paterno,
            'apellido_materno': apellido_materno,
            'matricula': matricula,
            'contraseña': contraseña
        }

        # Redirigir al usuario a la página de inicio de sesión
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario de inicio de sesión
        correo_electronico = request.form['correo_electronico']
        contraseña = request.form['contraseña']

        # Verificar si el usuario existe en la base de datos temporal
        if correo_electronico in users_db and users_db[correo_electronico]['contraseña'] == contraseña:
            # Aquí deberías implementar la lógica para manejar la sesión del usuario
            return f'Bienvenido, {users_db[correo_electronico]["nombre"]}!'
        else:
            return 'Credenciales inválidas. Inténtalo nuevamente.'

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
