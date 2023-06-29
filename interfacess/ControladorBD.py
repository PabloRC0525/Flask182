from tkinter import messagebox
import sqlite3
import bcrypt

class ControladorBD:
    
    def __init__(self):
        pass
    
    #Metodos para crear conexiones
    def conexionBD(self):
        try:
            conexion= sqlite3.connect("C0:/Users/andy2/OneDrive/Documentos/GitHub/Flask_182/Flask182/interfacess/DBUsuarios.db")
            return conexion
        except sqlite3.OperationalError:
            print("No se pudo conectar a la base de datos")
            0
    #Metodo para guardar usuarios
    def guardarUsuario(self, nom,cor,con):
        #1. usamos una conexion 
        conx=self.conexionBD()
        
        #2. validar parametros Vacios
        
        if(nom=="" or cor=="" or con==""):
            messagebox.showwarning("Aguas","Formulario incompleto")
            conx.close()
        else:
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            
            cursor= conx.cursor()
            
            conH=self.encriptarCon(con)
            
            datos=(nom,cor,conH)
            qrInsert="insert into TBRegistrados (Nombre, Correo, Contra) values (?,?,?)" 
            
            #4.Ejecutamos el insert y cerramos la conexion
            cursor.execute(qrInsert,datos)           
            conx.commit()
            conx.close
            messagebox.showinfo("Exito","Usuario Guardado")
            
    def encriptarCon(self, contra):
        ConPlana= contra
        
        ConPlana = ConPlana.encode() # convertimos a bytes
        
        sal= bcrypt.gensalt()
        conHa = bcrypt.hashpw(ConPlana,sal)
        return conHa
    
    
    def consultarUsuario(self,id):
        
        #1. usamos una conexion 
        conx=self.conexionBD()
        #2. validar parametros Vacios
        
        if(id==""):
            messagebox.showwarning("Aguas","Campo vacío, ponga un id ")
            conx.close()
        else:
            try:
                #3 cursos y query
                cursor=conx.cursor()
                selectquery = "SELECT * FROM TBRegistrados WHERE id="+id
                
                #4.ejecuta y guarda la consulta
                
                cursor.execute(selectquery)
                rsUsuario= cursor.fetchall()
                conx.close()
                return rsUsuario
            except sqlite3.OperationalError:
                print("error consulta")
                
    def Consu(self):
        #1. usamos una conexion 
        conx=self.conexionBD()
        try:
            #3 cursos y query
            cursor=conx.cursor()
            selectquery = "SELECT * FROM TBRegistrados"

            #4.ejecuta y guarda la consulta
            cursor.execute(selectquery)
            rsUsuario = cursor.fetchall()
            conx.close()

            #5. retornar resultados en un while
            results = []
            for row in rsUsuario:
                results.append(row)
            return results

        except sqlite3.OperationalError:
            print("error consulta")


    def ActualizarUsuario(self, id, nom,cor,con):
        #1. usamos una conexion 
        conx=self.conexionBD()
        
        #2. validar parámetros vacíos
        
        if(nom=="" or cor=="" or con==""):
            messagebox.showwarning("Cuidado","No puede dejar campos incompletos, complete todos los campos")
            conx.close()
            return False
        else:
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            cursor= conx.cursor()
            conE=self.encriptarCon(con)
            datosUP=(nom,cor,conE)
            qrUpdate="UPDATE TBRegistrados SET Nombre=?,Correo=?, Contra=? Where id="+id
            
            #4.Ejecutamos el Update y cerramos la conexión
            cursor.execute(qrUpdate,datosUP)           
            conx.commit()
            conx.close
            messagebox.showinfo("Exito","Usuario Actualizado")
            return True
        
        #se retornan true o false para hacer uso de la limpieza de los entry's ya que si no se completo los campos, no se borren, pero si se completo el UPDATE
        #pues se borren y se oculten para evitar bugs, y se mande el mensaje de exito.
    
    def EliminarUser(self,id):
        conx=self.conexionBD()
        #Preguntar si quiere eliminar 
        confirmar = messagebox.askyesno("Eliminar Usuario", "¿Está seguro que desea eliminar este usuario?")
        if confirmar==True:
            try:
                #3 cursos y query
                cursor=conx.cursor()
                DLTQR = "DELETE FROM TBRegistrados WHERE id="+id
                #4.ejecuta y guarda la consulta
                cursor.execute(DLTQR)
                conx.commit()
                conx.close
                return True
            except sqlite3.OperationalError:
                print("error consulta")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario.")
            conx.close
            return False
        #se retornan true o false para hacer la verificación de ocultar los entrys y las etiquetas o mandar error de eliminar usuario por si se presiona que no quiere eliminarlo.
            