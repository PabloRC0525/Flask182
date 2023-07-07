from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'DB_Fruteria.db'

# Crear la base de datos y la tabla
def create_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tbFrutas
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                fruta TEXT,
                temporada TEXT,
                precio REAL,
                stock INTEGER)''')
    conn.commit()
    conn.close()

# Ruta principal - Mostrar formulario para ingresar datos
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para agregar datos a la tabla
@app.route('/agregar', methods=['POST'])
def agregar():
    fruta = request.form['fruta']
    temporada = request.form['temporada']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tbFrutas (fruta, temporada, precio, stock) VALUES (?, ?, ?, ?)",
              (fruta, temporada, precio, stock))
    conn.commit()
    conn.close()
    
    return redirect('/consulta')

# Ruta para mostrar los registros de la tabla con opciones de eliminar y editar
@app.route('/consulta')
def consulta():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tbFrutas")
    registros = c.fetchall()
    conn.close()
    
    return render_template('consulta.html', registros=registros)

# Ruta para buscar frutas por nombre
@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form['nombre']
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tbFrutas WHERE fruta LIKE ?", ('%' + nombre + '%',))
    resultados = c.fetchall()
    conn.close()
    
    return render_template('busqueda.html', resultados=resultados)

# Ruta para eliminar un registro de la tabla
@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tbFrutas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect('/consulta')

# Ruta para editar un registro de la tabla

@app.route('/editar/<int:id>', methods=['GET'])
def mostrar_formulario_edicion(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tbFrutas WHERE id = ?", (id,))
    registro = c.fetchone()
    conn.close()

    return render_template('edicion.html', registro=registro)

# Ruta para actualizar un registro en la tabla
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_registro(id):
    fruta = request.form['fruta']
    temporada = request.form['temporada']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tbFrutas SET fruta=?, temporada=?, precio=?, stock=? WHERE id=?",
              (fruta, temporada, precio, stock, id))
    conn.commit()
    conn.close()
    
    return redirect('/consulta')

# Ruta para realizar una consulta de frutas por nombre
@app.route('/consulta_nombre', methods=['POST'])
def consulta_nombre():
    nombre = request.form['nombre']

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tbFrutas WHERE fruta LIKE ?", ('%' + nombre + '%',))
    resultados = c.fetchall()
    conn.close()

    return render_template('resultado_consulta.html', resultados=resultados)


if __name__ == '__main__':
    create_database()
    app.run()
