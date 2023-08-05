import tkinter as tk
from tkinter import ttk, font
from tkinter import *
from ControladorBD import *

controlador = ControladorBD()

def delete():
    if controlador.guardarProducto(varNom.get(), varDesc.get(), varPrecio.get(), varCat.get(), varDisp.get()):
        txtNom.delete("0", "end")
        txtDesc.delete("0", "end")
        txtPrecio.delete("0", "end") 
        txtCat.delete("0", "end") 
        txtDisp.delete("0", "end") 
        panel.forget(3)
        panel.select(0)
    

    
def add():
    txtNom.delete("0", "end")
    txtDesc.delete("0", "end")
    txtPrecio.delete("0", "end") 
    txtCat.delete("0", "end") 
    txtDisp.delete("0", "end") 
    panel.add (pestana4, text='Agregar')
    panel.select(3)
    btnactu.pack_forget()
    btnDelete.pack_forget()
    btna.pack()
    
def modificar():
    panel.add (pestana4, text='Modificar')
    btnactu.pack()
    btnDelete.pack()
    btna.pack_forget()
    txtId.delete("0", "end")
    txtNom.delete("0", "end")
    txtDesc.delete("0", "end")
    txtPrecio.delete("0", "end") 
    txtCat.delete("0", "end") 
    txtDisp.delete("0", "end") 
    
    selected = tree.selection()[0]
    # obtener los valores del elemento seleccionado
    values = tree.item(selected)['values']
    txtId.insert(0, values[0])
    txtNom.insert(0, values[1])
    txtDesc.insert(0, values[2])
    txtPrecio.insert(0, values[3]) 
    txtCat.insert(0, values[4])
    txtDisp.insert(0, values[5])
    panel.select(3)

def UPD():
    if controlador.ActualizarProducto(varIdUp.get(),varNom.get(), varDesc.get(), varPrecio.get(), varCat.get(), varDisp.get()):
        txtId.delete("0", "end")
        txtNom.delete("0", "end")
        txtDesc.delete("0", "end")
        txtPrecio.delete("0", "end") 
        txtCat.delete("0", "end") 
        txtDisp.delete("0", "end") 
        panel.forget(3)
        panel.select(0)
        
        
def DeleteProd():
    if controlador.EliminarProducto(varIdUp.get()):
        txtId.delete("0", "end")
        txtNom.delete("0", "end")
        txtDesc.delete("0", "end")
        txtPrecio.delete("0", "end") 
        txtCat.delete("0", "end") 
        txtDisp.delete("0", "end") 
        panel.forget(3)
        panel.select(0)

Ventana= Tk()
Ventana.title("Administradores")
Ventana.geometry("1300x400")

panel=ttk.Notebook (Ventana)
panel.pack(fill='both', expand='yes')
pestana1=ttk.Frame (panel)
pestana2=ttk.Frame (panel)
pestana3=ttk.Frame (panel)
pestana4=ttk.Frame (panel)

panel.add (pestana1, text='Menu')
panel.add (pestana2, text='Pedidos')
panel.add (pestana3, text='Clientes')

fuente = font.Font(family='Helvetica', size=12, weight='bold')

# Pestaña 1: Consultar Productos
TituloCons=Label(pestana1,text="Consultar Productos", fg="blue").pack()
#Creación del treeview

columns = ('ID', 'Nombre', 'Descripción', 'Precio', 'Categoria', 'Disponibilidad')
tree = ttk.Treeview(pestana1, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Descripción", text="Descripción")
tree.heading("Precio", text="Precio")
tree.heading("Categoria", text="Categoría")
tree.heading("Disponibilidad", text="Disponibilidad")
tree.pack()

btnUpdate=Button(pestana1, text='Actualizar',command=modificar)
#pero se oculta para que se ejecute solamente cuando se presiona un registro(para evitar bugs y errores por los usuarios)
btnUpdate.pack_forget()
BtnAdd = Button(pestana1,text='Nuevo producto',command=add).pack()


# Pestaña 2: Consultar Pedidos
TituloCons=Label(pestana2,text="Consultar Pedidos", fg="blue").pack()
#Creación del treeview

columns2 = ('ID', 'Fecha', 'Estado', 'Total', 'Nombre')
tree2 = ttk.Treeview(pestana2, columns=columns2, show='headings')
tree2.heading("ID", text="ID")
tree2.heading("Fecha", text="Fecha")
tree2.heading("Estado", text="Estado")
tree2.heading("Total", text="Total")
tree2.heading("Nombre", text="Nombre")
tree2.pack()




# Pestaña 3: Consultar Clientes
TituloCons=Label(pestana3,text="Consultar Clientes", fg="blue").pack()
#Creación del treeview

columns1 = ('ID', 'Nombre', 'ApellidoPat', 'ApellidoMat', 'Correo', 'Ocupación')
tree1 = ttk.Treeview(pestana3, columns=columns1, show='headings')
tree1.heading("ID", text="ID")
tree1.heading("Nombre", text="Nombre")
tree1.heading("ApellidoPat", text="Apellido P.")
tree1.heading("ApellidoMat", text="Apellido M.")
tree1.heading("Correo", text="Correo")
tree1.heading("Ocupación", text="Ocupación")
tree1.pack()


#pestaña 4 Modificaciones
titulo = Label(pestana4, text="Agregar Productos", fg="blue", font=fuente)
titulo.pack()

varIdUp=tk.StringVar()
txtId= Entry(pestana4, textvariable=varIdUp)

varNom = tk.StringVar()
lblNom = Label(pestana4, text="Nombre: ")
lblNom.pack()
txtNom = Entry(pestana4, textvariable=varNom)
txtNom.pack()

varDesc = tk.StringVar()
lblDesc = tk.Label(pestana4, text="Descripción: ")
lblDesc.pack()
txtDesc = tk.Entry(pestana4, textvariable=varDesc)
txtDesc.pack()

varPrecio = tk.StringVar()
lblPrecio = tk.Label(pestana4, text="Precio: ")
lblPrecio.pack()
txtPrecio = tk.Entry(pestana4, textvariable=varPrecio)
txtPrecio.pack()



varCat = tk.StringVar()
lblCat = tk.Label(pestana4, text="Categoría: ")
lblCat.pack()
txtCat = tk.Entry(pestana4, textvariable=varCat)
txtCat.pack()

varDisp = tk.StringVar()
lblDisp = tk.Label(pestana4, text="Disponibilidad: ")
lblDisp.pack()
txtDisp = tk.ttk.Combobox(pestana4, textvariable=varDisp,values=["Sí", "No"])
txtDisp.pack()

btna=Button(pestana4,text="Agregar",command=delete)
btnactu=Button(pestana4,bg="blue",fg="white",text="Actualizar",command=UPD)
btnDelete=Button(pestana4,bg="red",fg="white",text="Eliminar!!!",command=DeleteProd)




def actualizar(event):
    ConsultarProd(event)
    ConsultarClientes(event)
    ConsultarPed(event)


def ConsultarProd(event):
    # verificar si la pestaña seleccionada es la pestaña de Consultar usuarios
    current_tab = event.widget.tab('current')['text']
    if current_tab == 'Menu':
        #si es así pues se borran los datos del treeview para evitar que se escriban muchas veces los datos
        for row in tree.get_children():
            tree.delete(row)
        #aqui "a" va a mostrar los registros pero hare uso de un ciclo para mostrar todos los registros.
        a=controlador.ConsultarProd()
        while a:
            row = a.pop(0)  
            #aqui se insertan los datos del ciclo en el tree por filas.
            tree.insert('', tk.END, values=(row))   
#investigue esta opcion que ejecuta la función cada que se cambia a la pestaña indicada arriba.
panel.bind('<<NotebookTabChanged>>', actualizar)



def ConsultarClientes(event):
    # verificar si la pestaña seleccionada es la pestaña de Consultar usuarios
    current_tab = event.widget.tab('current')['text']
    if current_tab == 'Clientes':
        #si es así pues se borran los datos del treeview para evitar que se escriban muchas veces los datos
        for row in tree1.get_children():
            tree1.delete(row)
        #aqui "a" va a mostrar los registros pero hare uso de un ciclo para mostrar todos los registros.
        lista=controlador.MostrarClientes()
        while lista:
            row = lista.pop(0)  
            #aqui se insertan los datos del ciclo en el tree por filas.
            tree1.insert('', tk.END, values=(row))   
#investigue esta opcion que ejecuta la función cada que se cambia a la pestaña indicada arriba.
panel.bind('<<NotebookTabChanged>>', actualizar)


def ConsultarPed(event):
    # verificar si la pestaña seleccionada es la pestaña de Consultar usuarios
    current_tab = event.widget.tab('current')['text']
    if current_tab == 'Pedidos':
        #si es así pues se borran los datos del treeview para evitar que se escriban muchas veces los datos
        for row in tree2.get_children():
            tree2.delete(row)
        #aqui "a" va a mostrar los registros pero hare uso de un ciclo para mostrar todos los registros.
        listap=controlador.MostrarPedidos()
        while listap:
            row = listap.pop(0)  
            #aqui se insertan los datos del ciclo en el tree por filas.
            tree2.insert('', tk.END, values=(row))   
#investigue esta opcion que ejecuta la función cada que se cambia a la pestaña indicada arriba.
panel.bind('<<NotebookTabChanged>>', actualizar)





# función que muestra el botón de actualizar
def Mostrarboton(event):
    #hace uso del if un treeview esta seleccionado, muestra el botón
    if tree.selection():
        # si hay elementos seleccionados, mostrar el botón
        btnUpdate.pack()
    else:
        # si no hay elementos seleccionados, ocultar el botón
        btnUpdate.pack_forget()

# vincular la función al evento <<TreeviewSelect>>
tree.bind('<<TreeviewSelect>>', Mostrarboton)

Ventana.mainloop()