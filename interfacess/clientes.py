import tkinter as tk
from tkinter import ttk,font
from tkinter import *
from ControladorBD import *

controlador = ControladorBD()
fecha_actual = datetime.datetime.now()

def Log():
    btnReg.pack_forget()
    btnLog.pack_forget()
    lblIdLi.pack()
    txtIdLi.pack()
    lblContraLi.pack()
    txtContraLi.pack()
    btnLi.pack()
    btnRegresar.pack(side=tk.RIGHT)

    
def Reg():
    btnReg.pack_forget()
    btnLog.pack_forget()
    lblId.pack()
    txtId.pack()
    lblNom.pack()
    txtNom.pack()
    lblApPat.pack()
    txtApPat.pack()
    lblApMat.pack()
    txtApMat.pack()
    lblCor.pack()
    txtCor.pack()
    lblCon.pack()
    txtCon.pack()
    lblOcup.pack()
    txtOcup.pack()
    btnGuardar.pack()
    btnRegresar.pack(side=tk.RIGHT)
    
def regresar():
    btnReg.pack()
    btnLog.pack()
    lblId.pack_forget()
    txtId.pack_forget()
    lblNom.pack_forget()
    txtNom.pack_forget()
    lblApPat.pack_forget()
    txtApPat.pack_forget()
    lblApMat.pack_forget()
    txtApMat.pack_forget()
    lblCor.pack_forget()
    txtCor.pack_forget()
    lblOcup.pack_forget()
    txtOcup.pack_forget()
    btnGuardar.pack_forget()
    lblIdLi.pack_forget()
    txtIdLi.pack_forget()
    lblContraLi.pack_forget()
    txtContraLi.pack_forget()
    btnLi.pack_forget()
    lblCon.pack_forget()
    txtCon.pack_forget()
    btnRegresar.pack_forget()
    
    
def IniciarSes():
    if controlador.LogIn(varIdLi.get(), varContraLi.get()):
        valor = txtIdLi.get()
        txtIdLi.delete("0", "end") 
        txtContraLi.delete("0", "end")
        panel.forget(0)
        panel.add (pestana2, text='Menu')
        panel.add (pestana3, text='Pedidos')
        global valorpedidos
        valorpedidos = valor
        
        
        
def Registrarte():
    if controlador.guardarUsuario(varId.get(),varNom.get(),varApPat.get(),varApMat.get(),varCor.get(),varCon.get(),varOcup.get()):
        txtId.delete("0", "end") 
        txtNom.delete("0", "end") 
        txtApPat.delete("0", "end") 
        txtApMat.delete("0", "end") 
        txtCor.delete("0", "end") 
        txtCon.delete("0", "end") 
        txtOcup.delete("0", "end") 



def pedidos():
    if controlador.Pedidos(fecha_actual,valorpedidos,preciodef):
        productos_comprados.clear()
        actualizar_etiqueta()
        actualizar_etiqueta_precio_total()
        



               

            
Ventana= Tk()
Ventana.title("CRUD de Usuarios")
Ventana.geometry("1120x450")

panel=ttk.Notebook (Ventana)
panel.pack(fill='both', expand='yes')
pestana1=ttk.Frame (panel)
pestana2=ttk.Frame (panel)
pestana3=ttk.Frame (panel)

panel.add (pestana1, text='Iniciar sesión')
#panel.add (pestana1, text='Crear cuenta')
fuente = font.Font(family='Helvetica', size=12, weight='bold')
titulo = Label(pestana1, text="Bienvenido a KafeApp", fg="blue", font=fuente)
titulo.pack()

#Pestaña 1
btnLog = Button(pestana1, text='Iniciar Sesión',command=Log)
btnLog.pack()
btnReg = Button(pestana1, text='Registrarte',command=Reg)
btnReg.pack()


varIdLi = tk.StringVar()
lblIdLi = Label(pestana1, text="ID: ")
txtIdLi = Entry(pestana1, textvariable=varIdLi)
varContraLi = tk.StringVar()
lblContraLi = Label(pestana1, text="Contraseña: ")
txtContraLi = Entry(pestana1, textvariable=varContraLi)
btnLi = Button(pestana1, text='Iniciar Sesión',command=IniciarSes)
btnRegresar=Button(pestana1, text="Regresar",command=regresar)


varId = tk.StringVar()
lblId = Label(pestana1, text="ID: ")
txtId = Entry(pestana1, textvariable=varId)
varNom = tk.StringVar()
lblNom = Label(pestana1, text="Nombre: ")
txtNom = Entry(pestana1, textvariable=varNom)
varApPat = tk.StringVar()
lblApPat = Label(pestana1, text="Apellido Paterno: ")
txtApPat = Entry(pestana1, textvariable=varApPat)
varApMat = tk.StringVar()
lblApMat = Label(pestana1, text="Apellido Materno: ")
txtApMat = Entry(pestana1, textvariable=varApMat)
varCor = tk.StringVar()
lblCor = Label(pestana1, text="Correo: ")
txtCor = Entry(pestana1, textvariable=varCor)
varCon = tk.StringVar()
lblCon = Label(pestana1, text="Contraseña: ")
txtCon = Entry(pestana1, textvariable=varCon)

varOcup = tk.StringVar()
lblOcup = Label(pestana1, text="Ocupación: ")
txtOcup = Entry(pestana1, textvariable=varOcup)
btnGuardar = Button(pestana1, text='Guardar Usuario',command=Registrarte)

#Pestaña 2

columns = ('Id','Nombre', 'Descripción', 'Precio', 'Categoria')
tree = ttk.Treeview(pestana2, columns=columns, show='headings')
tree.heading("Id", text="Id")
tree.heading("Nombre", text="Nombre")
tree.heading("Descripción", text="Descripción")
tree.heading("Precio", text="Precio")
tree.heading("Categoria", text="Categoría")
tree.pack()

#Pestaña 3

columns3 = ('Id','Fecha', 'Precio', 'Total')
tree3 = ttk.Treeview(pestana3, columns=columns3, show='headings')
tree3.heading("Id", text="Id")
tree3.heading("Fecha", text="Fecha")
tree3.heading("Precio", text="Precio")
tree3.heading("Total", text="Total")
tree3.pack()



def comprar():
    # Obtener el registro seleccionado en el treeview
    item = tree.focus()
    # Obtener los valores de las columnas "Nombre" y "Precio" del registro seleccionado
    values = tree.item(item, 'values')
    nombre = values[1]
    precio = values[3]
    # Almacenar el nombre y el precio en la lista de productos comprados
    productos_comprados.append((nombre, precio))
    # Actualizar la etiqueta con la lista de productos comprados
    actualizar_etiqueta()
    actualizar_etiqueta_precio_total()

# Función para actualizar la etiqueta con la lista de productos comprados
def actualizar_etiqueta():
    texto = ''
    for producto in productos_comprados:
        texto += producto[0] + ' - $' + str(producto[1]) + '\n'
    etiqueta.config(text=texto)

# Lista para almacenar los productos comprados
productos_comprados = []
# Etiqueta para mostrar la lista de productos comprados
etiqueta = tk.Label(pestana2, text='')
etiqueta.pack(side="left")

# Función que se ejecuta al hacer clic en el botón de "eliminar"
def eliminar():
    # Obtener el registro seleccionado en el treeview
    item = tree.focus()
    # Eliminar el producto de la lista de productos comprados si está presente
    values = tree.item(item, 'values')
    nombre = values[1]
    for i, producto in enumerate(productos_comprados):
        if producto[0] == nombre:
            del productos_comprados[i]
            break
    # Actualizar la etiqueta con la lista de productos comprados
    actualizar_etiqueta()
    actualizar_etiqueta_precio_total()


etiqueta_precio_total = ttk.Label(pestana2, text='Precio total: $0.00')
etiqueta_precio_total.pack()

def actualizar_etiqueta_precio_total():
    # Calcular el precio total de los productos comprados
    precios = [float(producto[1]) for producto in productos_comprados]
    precio_total = sum(precios)
    # Actualizar el texto de la etiqueta
    etiqueta_precio_total.config(text='Precio total: ${:.2f}'.format(precio_total))
    global preciodef
    preciodef = precio_total
    if preciodef!=0:
        btnPagar.pack()
    else:
        btnPagar.pack_forget()


btnPedir = Button(pestana2, text='Seleccionar',command=comprar)
btnrlim = Button(pestana2, text='Eliminar',command=eliminar)
btnPagar = Button(pestana2, text='Pagar!',command=pedidos)

def actualizar(event):
    ConsultarPed(event)
    ConsultarProd(event)


def ConsultarProd(event):
    # verificar si la pestaña seleccionada es la pestaña de Consultar usuarios
    current_tab = event.widget.tab('current')['text']
    if current_tab == 'Menu':
        
        for row in tree.get_children():
            tree.delete(row)
        a=controlador.ProdClient()
        while a:
            row = a.pop(0)  
            #aqui se insertan los datos del ciclo en el tree por filas.
            tree.insert('', tk.END, values=(row))   
#investigue esta opcion que ejecuta la función cada que se cambia a la pestaña indicada arriba.
panel.bind('<<NotebookTabChanged>>', actualizar)


def ConsultarPed(event):
    # verificar si la pestaña seleccionada es la pestaña de Consultar usuarios
    current_tab1 = event.widget.tab('current')['text']
    if current_tab1 == 'Pedidos':
        
        for row1 in tree3.get_children():
            tree3.delete(row1)
        lista=controlador.PedClientes(valorpedidos)
        while lista:
            row1 = lista.pop(0)  
            #aqui se insertan los datos del ciclo en el tree por filas.
            tree3.insert('', tk.END, values=(row1))   
#investigue esta opcion que ejecuta la función cada que se cambia a la pestaña indicada arriba.
panel.bind('<<NotebookTabChanged>>', actualizar)






# función que muestra el botón de actualizar
def Mostrarboton(event):
    #hace uso del if un treeview esta seleccionado, muestra el botón
    if tree.selection():
        # si hay elementos seleccionados, mostrar el botón
        btnPedir.pack()
        btnrlim.pack()
        
    else:
        # si no hay elementos seleccionados, ocultar el botón
        btnPedir.pack_forget()
        btnrlim.pack_forget()
        btnPagar.pack_forget()

# vincular la función al evento <<TreeviewSelect>>
tree.bind('<<TreeviewSelect>>', Mostrarboton)

Ventana.mainloop()