# connection.py
# -----------------------------------------------------------------------------
# Este módulo solo tiene UNA responsabilidad: crear la conexión a MySQL.
# Es la "capa de acceso a datos" del proyecto: clientes.py la usa para
# ejecutar sus consultas y python_mysql.py la usa para levantar la interfaz.
# -----------------------------------------------------------------------------

import mysql.connector
# Importamos la librería "mysql-connector-python".
# Esta librería es el puente entre Python y MySQL: permite abrir conexiones,
# crear cursores y ejecutar sentencias SQL desde código Python.

class CConnection:
    # Clase contenedora de la conexión a la base de datos.
    # Se escribe "CConnection" siguiendo la convención del proyecto
    # (prefijo "C" = Clase, como CClientes).
    # No se instancia; sus métodos se llaman de forma estática, es decir:
    #   CConnection.connectionBaseDeDatos()

    def connectionBaseDeDatos():
        # Método que abre y devuelve una conexión a la base de datos "clientesdb".
        # Idea clave: cada operación (listar, insertar, actualizar, borrar) pide
        # su propia conexión, hace su trabajo y la cierra al final.
        # Así evitamos dejar conexiones abiertas sin usar.

        try:
            # 1) Intentar conectarnos a MySQL con los datos de acceso.
            #    Parámetros de mysql.connector.connect:
            #      user      -> usuario de MySQL (normalmente "root")
            #      password  -> contraseña del usuario
            #      host      -> "127.0.0.1" = localhost (la máquina local)
            #      database  -> nombre de la BD a la que entramos ("clientesdb")
            #      port      -> puerto por defecto de MySQL (3306)
            conexion = mysql.connector.connect(user="root", password="erik123",host="127.0.0.1",database="clientesdb",port="3306")
            print("Conexión correcta")
            return conexion
            # Si todo salió bien, devolvemos el objeto "conexion" a quien lo pidió.

        except mysql.connector.Error as error:
            # 2) Si algo falla (BD caída, contraseña mala, puerto equivocado...),
            #    capturamos el error de MySQL y lo mostramos en consola.

            #    ✅ BUG #2 CORREGIDO:
            #    Antes esta línea era "return conexion", pero si la conexión
            #    FALLÓ la variable "conexion" nunca se creó y Python lanzaba un
            #    segundo error (UnboundLocalError). Ahora devolvemos "None":
            #    significa "no hay conexión" y los métodos de clientes.py ya
            #    saben cómo detectarlo antes de seguir trabajando.
            print("Error al conectarte a la base de datos: {}".format(error))
            return None

#    NOTA SOBRE BUG #1 (YA CORREGIDO):
#    Antes existía aquí una línea suelta que ejecutaba connectionBaseDeDatos()
#    en el momento de importar el módulo (porque "from connection import *"
#    ejecuta todo el archivo). Eso abría una conexión "fantasma" que nunca se
#    guardaba ni se cerraba y, si MySQL no estaba disponible, rompía toda la
#    aplicación al arrancar. Se eliminó: ahora la conexión solo se abre cuando
#    un método la pide (bajo demanda).