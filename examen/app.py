from flask import Flask, render_template, request, redirect

app = Flask(__name__)
datos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['POST'])
def agregar():
    dato0 = request.form['Id']
    dato1 = request.form['Nombre']
    dato2 = request.form['Cantidad']
    dato3 = request.form['Precio']
    datos.append({'Id': dato0,'Nombre': dato1, 'Cantidad': dato2, 'Precio': dato3})
    return redirect('/lista')

@app.route('/lista')
def lista():
    return render_template('lista.html', datos=datos)

@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    if request.method == 'GET':
        dato = datos[index]
    elif request.method == 'POST':
        dato0 = request.form['Id']
        dato1 = request.form['Nombre']
        dato2 = request.form['Cantidad']
        dato3 = request.form['Precio']
        datos[index] = {'Id': dato0,'Nombre': dato1, 'Cantidad': dato2, 'Precio': dato3}
        return redirect('/editar')
@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def eliminar(index):
    if request.method == 'POST':
        datos.pop(index)
        return redirect('/lista')
    else:
        dato = datos[index]
        
        if __name__ == '__main__':
            app.run()