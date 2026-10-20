# python_mysql.py  (ARCHIVO PRINCIPAL / PUNTO DE ENTRADA del programa)
# -----------------------------------------------------------------------------
# Es el programa que se ejecuta: python python_mysql.py
# Responsabilidades:
#   1) Construir la interfaz gráfica (Tkinter) del formulario.
#   2) Conectar los botones de la interfaz con las funciones CRUD de CClientes.
#   3) Mantener actualizada la tabla (Treeview) con los datos de MySQL.
# Flujo: Interfaz (aquí) -> clientes.py (CRUD) -> connection.py (MySQL).
# -----------------------------------------------------------------------------

import tkinter as tk
#Importar los modulos restantes de tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from clientes import *
from connection import *
# Importamos Tkinter (para la ventana) y los módulos del propio proyecto.
# Tkinter es la biblioteca gráfica por defecto de Python para crear ventanas.

class FormularioClientes:
    # Clase "fantasma": declara las variables globales de la interfaz.
    # NO se usa como objeto (nadie hace FormularioClientes()); solo sirve para
    # declarar los identificadores antes de usarlos en las funciones.
    # Lo común en Tkinter es hacer esto dentro de las funciones, no en una clase.
    global win
    win = None
    global groupBox
    groupBox = None
    global textBoxId
    textBoxId = None
    global textBoxNombres
    textBoxNombre = None
    global textBoxApellidos
    textBoxApellidos = None
    global combo
    combo = None
    global textBoxTelefono
    textBoxTelefono = None
    global tree
    tree = None
    # "None" significa "todavía no existe". Estas variables se van a llenar
    # cuando la función formulario() cree los widgets.
    # Se usan variables GLOBALES porque varias funciones (guardar, modificar,
    # eliminar, seleccionar...) necesitan acceder a los MISMO widgets.

def actualizarTreeview():
    # Vuelve a cargar TODOS los registros de MySQL dentro de la tabla.
    # Se llama después de cada operación (guardar/modificar/eliminar) para
    # que la interfaz siempre refleje el estado real de la base de datos.
    global tree
    try:
        # 1) Borrar todo lo que haya en la tabla (los renglones viejos).
        #    get_children() devuelve las filas; el "*" las despliega como
        #    argumentos. "tree.delete(*lista)" borra todas de una vez.
        tree.delete(*tree.get_children())

        # 2) Obtener los nuevos datos que queremos mostrar
        datos = CClientes.mostrarClientes()

        # 3) Insertar los datos en el treeview
        #    row es cada tupla como (id, nombres, apellidos, sexo).
        #    tree.insert("", "end", values=row) agrega una fila al final.
        #    Nota: se llama a mostrarClientes() dos veces; basta guardarlo en
        #    "datos" e iterar sobre "datos".
        for row in CClientes.mostrarClientes():
            tree.insert("", "end", values=row)

    except ValueError as error:
        print("Error al actualizar la tabla {}".format(error))


def guardarRegistros():
    # Se ejecuta al presionar el botón "Guardar".
    # Lee los Entry (cuadros de texto) y el Combobox (sexo), los envía a
    # CClientes.ingresarClientes() y refresca la tabla.
    global textBoxNombres, textBoxApellidos, combo, textBoxTelefono, groupBox

    try:
        #verificar si los widgets estan inicializados
        # Si aún no existen (formulario no creado), salimos antes de fallar.
        if textBoxNombres is None or textBoxApellidos is None or combo is None or textBoxTelefono is None:
            print("Los widgets no estan inicializados")
            return

        # 1) Recuperar lo que escribió el usuario en cada campo.
        #    .get() devuelve el texto actual de un Entry / Combobox.
        nombres = textBoxNombres.get()
        apellidos = textBoxApellidos.get()
        sexo = combo.get()
        tel = textBoxTelefono.get()
        # 2) Llamar a la capa CRUD pasándole los datos (INSERT INTO usuarios).
        CClientes.ingresarClientes(nombres, apellidos, sexo, tel)
        # 3) Ventanita de confirmación ("Información" es el título).
        messagebox.showinfo("Información", "Los datos se ingresaron correctamente")

        #Llamamos a la función de actualizar treeview
        actualizarTreeview()

        #Limpiamos las textBox
        # delete(0, END) borra desde el inicio hasta el final del cuadro.
        textBoxNombres.delete(0, END)
        textBoxApellidos.delete(0, END)
        textBoxTelefono.delete(0, END)

    except ValueError as error:
        print("Error al guardar los datos: {}".format(error))

def modificarRegistros():
    # Se ejecuta al presionar el botón "Actualizar".
    # Igual que guardar, pero llama a modificarClientes() (UPDATE) y usa el id
    # que el usuario tiene puesto en el cuadro "Id".
    global textBoxId, textBoxNombres, textBoxApellidos, combo, textBoxTelefono, groupBox

    try:
        #verificar si los widgets estan inicializados
        if textBoxId is None or textBoxNombres is None or textBoxApellidos is None or combo is None or textBoxTelefono is None:
            print("Los widgets no estan inicializados")
            return

        # 1) El id identifica QUÉ registro vamos a modificar.
        idUsuario = textBoxId.get()
        nombres = textBoxNombres.get()
        apellidos = textBoxApellidos.get()
        sexo = combo.get()
        tel = textBoxTelefono.get()
        # 2) UPDATE usuarios SET ... WHERE id = idUsuario
        CClientes.modificarClientes(idUsuario, nombres, apellidos, sexo, tel)
        messagebox.showinfo("Información", "Los datos se actualizaron correctamente")

        #Llamamos a la función de actualizar treeview
        actualizarTreeview()

        #Limpiamos las textBox
        textBoxId.delete(0, END)
        textBoxNombres.delete(0, END)
        textBoxApellidos.delete(0, END)
        textBoxTelefono.delete(0, END)

    except ValueError as error:
        print("Error al modificar los datos: {}".format(error))

def eliminarRegistros():
    # Se ejecuta al presionar el botón "Eliminar".
    # Solo necesita el id; borra el registro de la BD (DELETE) y refresca.
    global textBoxId, textBoxNombres, textBoxApellidos, texBoxTelefono

    try:
        #verificar si los widgets estan inicializados
        if textBoxId is None:
            print("Los widgets no estan inicializados")
            return

        # 1) Leer el id que el usuario dejó en el cuadro.
        idUsuario = textBoxId.get()

        # 2) DELETE FROM usuarios WHERE id = idUsuario
        CClientes.eliminarClientes(idUsuario)
        messagebox.showinfo("Información", "Los datos se eliminaron correctamente")

        #Llamamos a la función de actualizar treeview
        actualizarTreeview()

        #Limpiamos las textBox
        textBoxId.delete(0, END)
        textBoxNombres.delete(0, END)
        textBoxApellidos.delete(0, END)
        textBoxTelefono.delete(0, END)

    except ValueError as error:
        print("Error al eliminar los datos: {}".format(error))

def seleccionarRegistro(event):
    # Se ejecuta cuando el usuario hace clic en una fila de la tabla (evento
    # "<<TreeviewSelect>>"). Rellena los Entry de arriba con los datos de la
    # fila seleccionada, para poder editarlos o eliminarlos.
    # "event" es el objeto de evento que Tkinter pasa automáticamente.
    try:
        # 1) focus() dice qué fila está seleccionada ahora mismo.
        itemSeleccionado = tree.focus()

        # 2) Si realmente hay una fila seleccionada...
        if itemSeleccionado:
            # 3) tree.item(item)["values"] devuelve la tupla de esa fila,
            #    ejemplo: ('3', 'Erik', 'Jarquin', 'Masculino').
            values = tree.item(itemSeleccionado)["values"]

            # 4) Copiar cada valor dentro de su Entry correspondiente.
            #    Primero se borra lo anterior y luego se inserta el nuevo.
            textBoxId.delete(0, END)
            textBoxId.insert(0, values[0])
            textBoxNombres.delete(0, END)
            textBoxNombres.insert(0, values[1])
            textBoxApellidos.delete(0, END)
            textBoxApellidos.insert(0, values[2])
            # 5) En el Combobox, .set() cambia el valor mostrado.
            combo.set(values[3])
            textBoxTelefono.delete(0, END)
            textBoxTelefono.insert(0, [4])


    except ValueError as error:
        print("Error al seleccionar los datos {}".format(error))

def formulario():
    # Función que CONSTRUYE toda la ventana y todos los widgets (dos zonas:
    # izquierda = formulario de captura, derecha = tabla de registros).
    # Se declaran "global" para que las demás funciones puedan usarlos.
    global win
    global groupBox
    global textBoxId
    global textBoxNombres
    global textBoxApellidos
    global combo
    global textBoxTelefono
    global tree

    try:
        # 1) LA VENTANA PRINCIPAL.
        #    Tk() crea la ventana raíz. Todo lo demás se coloca dentro de ella.
        win = Tk()
        #    Establece el tamaño de la ventana: 1250x300 (ancho x alto píxeles).
        win.geometry("1250x300")
        #    Título que aparece en la barra de la ventana.
        win.title("Formulario de python")

        # 2) ZONA IZQUIERDA: el formulario de captura de datos.
        #    LabelFrame es un contenedor con borde y título ("Datos del personal").
        #    padx/pady = espacio interno entre el borde y los widgets.
        groupBox = LabelFrame(win, text="Datos del personal", padx=5, pady=5)
        #    grid() organiza los widgets por filas y columnas (0,0 = arriba-izq).
        groupBox.grid(row=0,column=0,padx=10,pady=10)

        #Elementos del gruopBox de la izquierda
        # Label = texto fijo ("Id"); width=13 le da un ancho uniforme a los rótulos.
        # UG #4 CORREGIDO: antes se escribió font=("arial,12") con la coma
        #    DENTRO del texto; eso era un texto y no una tupla, así que Tkinter
        #    ignoraba la fuente. La forma correcta es ("arial", 12) en dos valores.
        labelId = Label(groupBox, text="Id", width=13,font=("arial", 12)).grid(row=0,column=0)
        # Entry = cuadro de texto de una sola línea. Aquí se guardará el id.
        textBoxId = Entry(groupBox)
        textBoxId.grid(row=0, column=1)

        labelNombres = Label(groupBox, text="Nombres", width=13,font=("arial", 12)).grid(row=1,column=0)
        textBoxNombres = Entry(groupBox)
        textBoxNombres.grid(row=1, column=1)

        labelApellidos = Label(groupBox, text="Apellidos", width=13,font=("arial", 12)).grid(row=2,column=0)
        textBoxApellidos = Entry(groupBox)
        textBoxApellidos.grid(row=2, column=1)

        # Combobox = lista desplegable. Aquí se elige el sexo.
        labelSexo = Label(groupBox, text="Sexo", width=13,font=("arial", 12)).grid(row=3,column=0)
        # StringVar almacena el texto actual del combobox (podría cambiar).
        seleccionSexo = tk.StringVar()
        # values=["Masculino","Femenino"] = las opciones de la lista.
        combo = ttk.Combobox(groupBox,values=["Masculino","Femenino"], textvariable=seleccionSexo)
        combo.grid(row=3,column=1)
        # Valor por defecto del combobox.
        seleccionSexo.set("Masculino")

        labelTelefono = Label(groupBox, text="Telefono", width=13, font=("arial", 12)).grid(row=4, column=0)
        textBoxTelefono = Entry(groupBox)
        textBoxTelefono.grid(row=4, column=1)

        # Botones de acción. "command" indica QUÉ función se ejecuta al pulsarlo
        # (sin paréntesis: se pasa la referencia a la función, no su resultado).
        Button(groupBox,text="Guardar", width=10, command=guardarRegistros).grid(row=5,column=0)
        Button(groupBox,text="Eliminar", width=10, command=eliminarRegistros).grid(row=5,column=1)
        Button(groupBox,text="Actualizar", width=10, command=modificarRegistros).grid(row=5,column=2)

        # 3) ZONA DERECHA: la tabla que lista los registros de la base de datos.
        #    Reutilizamos la variable groupBox para crear un segundo contenedor.
        groupBox = LabelFrame(win,text="Lista del personal", padx=5,pady=5)
        groupBox.grid(row=0, column=1, padx=5, pady=5)

        # 4) TREEVIEW = la "tabla" de la interfaz.
        #    columns = los títulos de cada columna.
        #    show="headings" muestra solo los encabezados (sin la 1ª col. oculta).
        #    height=5 = número de filas visibles.
        tree = ttk.Treeview(groupBox,columns=("Id","Nombres","Apellifos","Sexo","Telefono"),show="headings",height=5)
        #    Configurar cada columna: anchor=CENTER centra el texto.
        #    "# 1" se refiere a la primera columna, "# 2" a la segunda, etc.
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Id")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Nombres")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Apellidos")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="Sexo")
        tree.column("# 5", anchor=CENTER)
        tree.heading("# 5", text="Telefono")

        # 5) Llenar la tabla con los datos que ya existen en la BD.
        for row in CClientes.mostrarClientes():
            tree.insert("", "end", values=row)

        # 6) Conectar el evento de "clic en una fila" con la función
        #    seleccionarRegistro. Así, al elegir una fila, se rellenan los Entry.
        tree.bind("<<TreeviewSelect>>",seleccionarRegistro)

        # 7) pack() coloca el Treeview (se expande según el contenedor).
        tree.pack()

        # 8) mainloop() ARRANCA la aplicación: mantiene la ventana abierta y
        #    procesa los eventos (clics, teclas...) hasta que se cierre.
        #    Todo el código anterior solo construye la ventana; aquí "se enciende".
        win.mainloop()

    except ValueError as error:
        print("El error al mostrar la interfaz, error: {}".format(error))

if __name__ == "__main__":
    # MEJORA APLICADA: este bloque PROTEGE la entrada principal.
    # "formulario()" solo se ejecuta cuando corremos ESTE archivo directamente
    # (python python_mysql.py). Si otro archivo hace "from python_mysql import *",
    # la ventana NO se abre sola. Antes la llamada estaba suelta en el módulo.
    formulario()