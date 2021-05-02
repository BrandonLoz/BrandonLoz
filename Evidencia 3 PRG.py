import sys
import datetime
import time
import sqlite3
from sqlite3 import Error
import pandas as pd

respuesta = 1
monto_total = 0.00
clave = 0

columnas = ("Descripción", "Cantidad", "Precio", "Subtotal")
encabezados = ("No. Venta", "Detalles", "Monto", "Fecha")
art_encabezados = ("Clave", "Articulo", "Precio", "Existencia")

ventas_dic = {}
ventas_items = []

detalle = []
lista_subtotales = []
ventas_list = []

estructuraVenta = dict()

def menuPrincipal():
    print("_______________________________")
    print("\n*** Cosméticos True:BEAUTY! ***")
    print("\n        Menú principal       ")
    print("   [1] Registrar una venta.")
    print("   [2] Consultar una venta.")
    print("   [3] Obtener un reporte de ventas para una fecha en específico.")
    print("   [4] Salir.")
    print("_______________________________")
    print(" ")

while (True):
    menuPrincipal()
    opcion = input("¿Qué opción deseas?: ")
    respuesta = 1
    if opcion=="1":
        while respuesta == 1:
            print("\nCatálogo - Piezas existentes: ")
            try:
                with sqlite3.connect("Cosmetiquería.db") as conn:
                    mi_cursor = conn.cursor()
                    mi_cursor.execute("SELECT id_articulo, descripcion, precio FROM articulos WHERE existencia > 0;")
                    articulos = mi_cursor.fetchall()

                    print(f"{art_encabezados[0]} \t", end="")
                    print(f"{art_encabezados[1]} \t", end="")
                    print(art_encabezados[2])

                    for sku, nombre, precio in articulos:
                        print(f"{sku}\t", end="")
                        print(f"{nombre}\t", end="")
                        print("${:.2f}" .format(precio) + " mxn") #print("${:.2f}" .format(precio) + " mxn\t")
            except Error as e:
                print (e)
            except:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                conn.close()

            cant_datos = int(input("\n¿Cuántos articulos se registrarán?: "))
            for dato in range(cant_datos):
                desc_articulo = input("\nDescripción articulo: ")
                cant_pzas = int(input("Cantidad de piezas: "))
                precio_venta = float(input("Precio de venta: "))

                subtotal = cant_pzas * precio_venta
                lista_subtotales.append(subtotal)

                #estructuraArticulo = {'Nombre':desc_articulo, 'Cantidad':cant_pzas, 'Precio':precio_venta}
                #detalle.append(estructuraArticulo)

                #Probar con lista sobre lista para comprobar, la de arriba no funciona y probar el tipo de dato float
                registro = [desc_articulo, cant_pzas, precio_venta]
                detalle.append(registro)

                monto_total = sum(lista_subtotales)

                folio = int(input("\nIngresa el número de venta: "))
                fecha_capturada = input("Ingresa la fecha en que se realiza la venta (dd/mm/aaaa): ")
                fecha_capturada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date() #fecha_actual = datetime.date.today()
                venta = [folio,detalle,monto_total,fecha_capturada]

                ventas_list.append(venta)
                print("\nEl monto total es: ${:.2f}" .format(monto_total) + " mxn" + f"\nVenta: #{venta[0]} - Fecha captura: {venta[3]}")
            try:
                with sqlite3.connect("Cosmetiquería.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                    mi_cursor = conn.cursor()
                    fecha_procesada = datetime.datetime.combine(fecha_capturada, datetime.datetime.min.time())
                    venta_detalle = str(detalle).replace('[','').replace(']','')
                    valores = {"folio":folio, "detalles":venta_detalle, "monto":monto_total, "fecha_procesada":fecha_procesada}
                    mi_cursor.execute("INSERT INTO ventas VALUES(:folio,:detalles,:monto,:fecha_procesada);", valores)
                    print("Registro agregado exitosamente")
            except Error as e:
                print (e)
            except:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                conn.close()
                respuesta = int(input("\n¿Deseas elegir otro articulo? \n (1-Si / 0-No): "))
                estructuraArticulo = {}
                valores = {}
                lista_subtotales = []
                detalle = []
                venta = []
        #ventas_list = []
    elif opcion=="2":
        clave_buscar = int(input("\nDime la clave de la venta que deseas consultar: "))
        try:
            with sqlite3.connect("Cosmetiquería.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                mi_cursor = conn.cursor()
                criterios = {"folio":clave_buscar}
                mi_cursor.execute("SELECT * FROM ventas WHERE folio = :folio;", criterios)
                venta = mi_cursor.fetchall()
                print(f"{encabezados[0]} \t", end="")
                print(f"{encabezados[1]} \t", end="")
                print(f"{encabezados[2]} \t", end="")
                print(encabezados[3])

                for folio, detalles, monto, fecha_registro in venta:
                    print(f"{folio}\t", end="")
                    print(f"{detalles}\t", end="")
                    print("${:.2f}" .format(monto) + " mxn\t", end="")
                    print(fecha_registro)
        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            
    elif opcion=="3":
        fecha_capturada = input("\nIngresa la fecha de llamada (dd/mm/aaaa): ")
        fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
        try:
            with sqlite3.connect("Cosmetiquería.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn: #se crea la conexion
                mi_cursor = conn.cursor() #se crea el cursor
                criterios = {"fecha":fecha_procesada}
                mi_cursor.execute("SELECT * FROM ventas WHERE fecha = :fecha_capturada",criterios)
                venta = mi_cursor.fetchall()
                
                for folio, nombre, monto, fecha_capturada in venta:
                    print(f"Folio ={folio}")
                    print(f"Detalles = {detalles}")
                    print(f"Monto = {monto}")
                    print(f"Fecha = {fecha_capturada}")
                
        except sqlite3.Error as e:
            print (e)
            
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
                print("Se ha cerrado la conexión")
    elif opcion=="4":
        print("Saliendo...")
        break
    
    else:
        print ("\nNo has pulsado ninguna opción correcta...\nPulsa una tecla para continuar.")
