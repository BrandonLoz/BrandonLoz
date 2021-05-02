import sys
import datetime
import sqlite3

try:
    with sqlite3.connect("Cosmetiqueria.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conexion:
        mi_cursor = conexion.cursor()
        mi_cursor.execute("CREATE TABLE articulos (id_articulo INTEGER PRIMARY KEY, descripcion TEXT, precio NUMERIC NOT NULL, existencia NUMERIC);")
        print("Tabla creada")
except sqlite3.Error as e:
    print(e)
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conexion):
        conexion.close()
        print("Se ha cerrado la conexión")
    


