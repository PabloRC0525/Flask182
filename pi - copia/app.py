# app.py
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

# Crear la base de datos y las tablas si no existen
def crear_tablas():
    conn = sqlite3.connect('cafeteria.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            es_admin INTEGER NOT NULL DEFAULT 0,
            es_penalizado INTEGER NOT NULL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            producto TEXT NOT NULL,
            precio REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            precio_producto REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Función para verificar si un usuario es administrador
def es_administrador():
    if 'usuario_id' in session:
        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()

        cursor.execute('SELECT es_admin FROM usuarios WHERE id=?', (session['usuario_id'],))
        es_admin = cursor.fetchone()[0]

        conn.close()
        return es_admin == 1

    return False

# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id, es_admin FROM usuarios WHERE usuario=? AND contrasena=?', (usuario, contrasena))
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            session['usuario_id'] = resultado[0]
            return redirect(url_for('menu_principal'))
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrectos.")

    return render_template('login.html')

# Dashboard del usuario
@app.route('/usuario', methods=['GET', 'POST'])
def usuario_dashboard():
    if request.method == 'POST':
        producto = request.form['producto']
        precio = float(request.form['precio'])

        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO pedidos (usuario_id, producto, precio) VALUES (?, ?, ?)',
                       (session['usuario_id'], producto, precio))
        conn.commit()

        conn.close()

    conn = sqlite3.connect('cafeteria.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, producto, precio FROM pedidos WHERE usuario_id=?', (session['usuario_id'],))
    carrito = cursor.fetchall()

    conn.close()

    return render_template('usuario.html', carrito=carrito)

# Pago de productos del carrito
@app.route('/usuario/pagar')
def pagar():
    conn = sqlite3.connect('cafeteria.db')
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(precio) FROM pedidos WHERE usuario_id=?', (session['usuario_id'],))
    total = cursor.fetchone()[0]

    if total:
        # Aquí podrías implementar la lógica de procesamiento de pago, por ejemplo, registrar el pago en la base de datos.

        # Luego, puedes vaciar el carrito de compras
        cursor.execute('DELETE FROM pedidos WHERE usuario_id=?', (session['usuario_id'],))
        conn.commit()

        mensaje = "Pago realizado con éxito."
    else:
        mensaje = "El carrito de compras está vacío."

    conn.close()

    return redirect(url_for('usuario_dashboard', mensaje=mensaje))

# Dashboard del administrador
@app.route('/admin')
def admin_dashboard():
    if not es_administrador():
        return redirect(url_for('login'))

    conn = sqlite3.connect('cafeteria.db')
    cursor = conn.cursor()

    cursor.execute('SELECT usuario FROM usuarios WHERE es_penalizado=1')
    usuarios_penalizados = cursor.fetchall()

    cursor.execute('SELECT id, nombre_producto, precio_producto FROM menu')
    menu = cursor.fetchall()

    conn.close()

    return render_template('admin.html', usuarios_penalizados=usuarios_penalizados, menu=menu)

# Agregar nuevo administrador
@app.route('/admin/agregar_admin', methods=['GET', 'POST'])
def agregar_nuevo_administrador():
    if not es_administrador():
        return redirect(url_for('login'))

    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO usuarios (usuario, contrasena, es_admin) VALUES (?, ?, ?)',
                       (usuario, contrasena, 1))
        conn.commit()

        conn.close()

        mensaje = "Nuevo administrador agregado con éxito."
        return redirect(url_for('admin_dashboard', mensaje=mensaje))

    return render_template('agregar_admin.html')

# Agregar nuevo producto al menú
@app.route('/admin/agregar_producto', methods=['GET', 'POST'])
def agregar_nuevo_producto():
    if not es_administrador():
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        precio_producto = float(request.form['precio_producto'])

        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO menu (nombre_producto, precio_producto) VALUES (?, ?)',
                       (nombre_producto, precio_producto))
        conn.commit()

        conn.close()

        mensaje = "Nuevo producto agregado al menú."
        return redirect(url_for('admin_dashboard', mensaje=mensaje))

    return render_template('agregar_producto.html')

# Ruta del menú principal
@app.route('/menu_principal')
def menu_principal():
    if 'usuario_id' in session:
        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()

        cursor.execute('SELECT es_admin FROM usuarios WHERE id=?', (session['usuario_id'],))
        es_admin = cursor.fetchone()[0]

        conn.close()

        return render_template('menu_principal.html', es_admin=es_admin)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    crear_tablas()
    app.run(debug=True)
