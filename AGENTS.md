# AGENTS.md — Contexto del proyecto (Agenda de contactos)

## Qué es este proyecto

Aplicación de escritorio en **Python + Tkinter** para gestionar una agenda de clientes
(con formulario y tabla), con **MySQL** como base de datos. Es un proyecto de práctica
con fines didácticos: el código está muy comentado en español para aprender.

- Repositorio: `Agenda-de-contactos`
- Rama activa: `agenda-contactos`
- Ejecución: `python python_mysql/python_mysql.py`
- Python usado en desarrollo: 3.12 / 3.13 (hay `.pyc` de cpython-312)
- Dependencia: `mysql-connector-python` (falta `requirements.txt`)

## Estructura

```
Agenda-de-contactos/
├── AGENTS.md                      # este archivo
├── docs/
│   ├── Como ejecutar el proyecto python_mysql.pdf
│   ├── Como funciona el proyecto python_mysql.pdf
│   └── Mejoras pendientes - Guia de implementacion.pdf
├── python_mysql/
│   ├── python_mysql.py            # Punto de entrada + interfaz Tkinter
│   ├── clientes.py                # Clase CClientes (CRUD sobre la tabla "usuarios")
│   ├── connection.py              # Clase CConnection (abre la conexión a MySQL)
│   ├── Script de la base de datos.sql  # Esquema y datos de ejemplo
│   └── __pycache__/               # (a eliminar del repo; no aporta)
└── get-pip.py                     # (a eliminar; archivo residual, no del proyecto)
```

## Arquitectura en 3 capas

```
python_mysql.py (interfaz)  ->  clientes.py (CRUD)  ->  connection.py (MySQL)
```

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `connection.py` | `CConnection` | `connectionBaseDeDatos()`: abre y devuelve una conexión a `clientesdb`. Devuelve `None` si falla. |
| `clientes.py` | `CClientes` | `mostrarClientes()`, `ingresarClientes()`, `modificarClientes()`, `eliminarClientes()` (R, C, U, D). Cada método pide su propia conexión, hace su trabajo y la cierra. |
| `python_mysql.py` | `FormularioClientes` (clase fantasma, a eliminar) | Construye la ventana (formulario a la izquierda, `ttk.Treeview` a la derecha) y conecta botones con el CRUD. |

## Base de datos

- Nombre: `clientesdb`
- Tabla: `usuarios` (`id` INT AUTO_INCREMENT PK, `nombres` VARCHAR(50), `apellidos` VARCHAR(50), `sexo` VARCHAR(20))
- Conexión actual (hardcodeada, pendiente de mover a `.env`): usuario `root`, host `127.0.0.1`, puerto `3306`.

## Convenciones del código

- Todo el texto (comentarios, mensajes, títulos) en **español**; comentarios muy explicativos.
- Prefijo **`C`** para clases: `CClientes`, `CConnection`.
- Métodos estáticos sin `@staticmethod` (se llaman como `CClientes.mostrarClientes()`).
- Consultas con **parámetros `%s`** en `cursor.execute(sql, valores)` (nunca concatenar strings → anti inyección SQL).
- `commit()` solo en INSERT/UPDATE/DELETE (no en SELECT).
- `print()` para errores/depuración (mejora pendiente: no debe quedar en `connection.py`).
- Variables globales de la interfaz (`win`, `tree`, `texBoxId`, `texBoxNombres`, `texBoxApellidos`, `combo`, `groupBox`) declaradas con `global` en cada función que las usa.

## Estado / mejoras pendientes

El detalle completo (código + explicación) está en
`docs/Mejoras pendientes - Guia de implementacion.pdf`. Resumen:

1. Credenciales en **variables de entorno** (`.env` + `python-dotenv`), no en el código.
2. **`try/finally`** en los métodos CRUD para garantizar `cone.close()`.
3. `actualizarTreeview()`: llamar a `mostrarClientes()` **una sola vez** y guardar en `datos`.
4. Quitar el `commit()` tras el SELECT y los `print()` de `connection.py`.
5. Eliminar la clase fantasma `FormularioClientes` y el archivo `get-pip.py` (ambos están trackeados por git: usar `git rm`).
6. **`messagebox.askyesno`** de confirmación antes de borrar un registro.
7. Crear `.gitignore` que excluya `.env` (credenciales), `__pycache__/` y similares.

## Comandos útiles

```bash
git status                      # estado del repo
git ls-files                    # archivos trackeados (revisar get-pip.py / __pycache__)
python python_mysql/python_mysql.py   # ejecutar la app
```
