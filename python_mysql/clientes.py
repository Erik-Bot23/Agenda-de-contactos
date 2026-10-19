# clientes.py
# -----------------------------------------------------------------------------
# Capa de "operaciones de negocio" sobre la tabla "usuarios".
# Define la clase CClientes con las 4 operaciones básicas CRUD:
#   C = Create (crear)      -> ingresarClientes()
#   R = Read   (leer)       -> mostrarClientes()
#   U = Update (actualizar) -> modificarClientes()
#   D = Delete (eliminar)   -> eliminarClientes()

#    BUG #3 CORREGIDO:
#    Antes este archivo usaba mysql.connector sin importarlo y "funcionaba por
#    casualidad" porque connection.py lo importaba antes (y "from connection
#    import *" arrastraba la variable). Ahora cada archivo declara sus propias
#    dependencias, que es la forma correcta y no rompe si cambia connection.py.
# -----------------------------------------------------------------------------
import mysql.connector
from connection import *
# Importa todo lo público de connection.py, incluida la clase CConnection,
# que usamos abajo para pedir conexiones a la base de datos.
#

class CClientes:
    # Clase con las operaciones CRUD de la tabla "usuarios".

    def mostrarClientes():
        # R = READ. Devuelve todos los registros de la tabla "usuarios".
        try:
            # 1) Pedimos una conexión nueva a la BD.
            cone = CConnection.connectionBaseDeDatos()
            # 2) PROTECCIÓN (relacionada con el bug #2): si no hay MySQL, la
            #    conexión vale None y la siguiente línea (cone.cursor()) haría
            #    reventar el programa. Antes solo se mostraba el error en
            #    consola y el programa seguía y explotaba. Ahora cancelamos la
            #    operación con un aviso claro.
            if cone is None:
                print("No se pudo conectar a la base de datos. Operación cancelada.")
                return []
            # 3) El cursor es el objeto que ejecuta SQL y guarda el resultado.
            cursor = cone.cursor()
            # 4) Ejecutamos la consulta: selecciona todas las columnas de la tabla.
            cursor.execute("select * from usuarios;")
            # 5) fetchall() trae TODAS las filas como una lista de tuplas.
            #    Ejemplo: [(1, 'Erik', 'Jarquin', 'Masculino'), (2, ... )]
            miResultado = cursor.fetchall()
            # 6) "commit" confirma los cambios. En un SELECT no cambia nada,
            #    así que esta línea es redundante aquí (sobra, pero no daña).
            cone.commit()
            # 7) Cerramos la conexión para no dejar recursos abiertos.
            cone.close()
            # 8) Devolvemos la lista de registros a quien la pidió.
            return miResultado

        except mysql.connector.Error as error:
            # Si la consulta falla (tabla no existe, BD caída...), mostramos el error
            # y devolvemos una lista vacía para que la interfaz no se rompa.
            print("Error al mostrar los datos {}".format(error))
            return []

    def ingresarClientes(nombres, apellidos, sexo):
        # C = CREATE. Inserta un nuevo cliente en la tabla "usuarios".
        # Recibe 3 parámetros: los datos que escribió el usuario en el formulario.
        try:
            cone = CConnection.connectionBaseDeDatos()
            # PROTECCIÓN: mismas explicación que en mostrarClientes().
            # Con None en "cone", la app se detiene aquí sin reventar.
            if cone is None:
                print("No se pudo conectar a la base de datos. Operación cancelada.")
                return
            cursor = cone.cursor()
            # 1) Sentencia SQL con marcadores de posición "%s".
            #    El "null" ocupa el auto_increment de la columna "id".
            sql = "insert into usuarios values (null,%s,%s,%s);"
            # 2) Los valores que sustituirán a cada "%s", en el mismo orden.
            #    La variable valores tiene que ser una tupla.
            #    Como minima expresion es: (valor,) la coma hace que sea una tupla.
            #    Las tuplas son listas inmutables, eso quiere decir que no se puede modificar.
            valores = (nombres, apellidos, sexo)
            # 3) Ejecutamos la sentencia con sus valores.
            #    Pasar los valores aparte (NO pegarlos al texto SQL) es lo
            #    correcto: evita la inyección SQL y los errores de comillas.
            #
            #    peligroso:  f"insert ... values (null, '{nombres}', ...)"
            #    correcto:   cursor.execute(sql, valores)
            cursor.execute(sql, valores)
            # 4) En INSERT/UPDATE/DELETE SÍ hace falta commit() para guardar
            #    los cambios de forma definitiva en la base de datos.
            cone.commit()
            # 5) rowcount dice cuántas filas se vieron afectadas (aquí: 1).
            print(cursor.rowcount,"Registro ingresado")
            cone.close()

        except mysql.connector.Error as error:
            print("Error al ingresar en la base de datos {}".format(error))

    def modificarClientes(id, nombres, apellidos, sexo):
        # U = UPDATE. Actualiza los datos de un cliente ya existente.
        # Identifica el registro por "id" y reemplaza nombres, apellidos y sexo.
        try:
            cone = CConnection.connectionBaseDeDatos()
            # PROTECCIÓN: mismas explicación que en mostrarClientes().
            if cone is None:
                print("No se pudo conectar a la base de datos. Operación cancelada.")
                return
            cursor = cone.cursor()
            # 1) UPDATE ... SET ... WHERE ...  -> cambia SOLO la fila cuyo id coincida.
            #    Se usa "usuarios.id" para despejar a qué tabla/columna nos referimos.
            sql = "update usuarios set usuarios.nombres = %s, usuarios.apellidos = %s, usuarios.sexo = %s where usuarios.id = %s;"
            # 2) El orden de la tupla debe coincidir con el orden de los %s:
            #    nombres, apellidos, sexo ... y al final el id (el filtro).
            valores = (nombres, apellidos, sexo, id)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount,"Registro actualizado")
            cone.close()

        except mysql.connector.Error as error:
            print("Error al actualizar en la base de datos {}".format(error))

    def eliminarClientes(id):
        # D = DELETE. Borra el cliente cuyo "id" coincida.
        try:
            cone = CConnection.connectionBaseDeDatos()
            # PROTECCIÓN: mismas explicación que en mostrarClientes().
            if cone is None:
                print("No se pudo conectar a la base de datos. Operación cancelada.")
                return
            cursor = cone.cursor()
            # 1) La sentencia de borrado: filtra por id para no borrar toda la tabla.
            sql = "delete from usuarios where usuarios.id = %s;"
            # 2) Tupla de UN solo elemento. La coma final es OBLIGATORIA para que
            #    Python la considere tupla; sin la coma sería solo el número "id".
            valores = (id,)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount,"Registro eliminado")
            cone.close()

        except mysql.connector.Error as error:
            print("Error al eliminar en la base de datos {}".format(error))