from flask import Flask

#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbflask"


#Declaramos una ruta
#ruta Index http://localhost:5000
#ruta se compone de nombre y funcion
@app.route('/')
def index():
    return "Hola mundo"

@app.route('/guardar')
def guardar():
    return "Se guardo el album en la BD"
@app.route('/eliminar')
def eliminar():
    return "Se eliminó el album en la BD"
#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=5000,debug=True)
