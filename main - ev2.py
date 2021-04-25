import csv
import os
import datetime
import time
import pandas as pd

respuesta = 1
monto_total = 0.00
clave = 0

columnas = ("Descripción", "Cantidad", "Precio", "Subtotal")
encabezados = ("No. Venta", "Detalles", "Monto", "Fecha")

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

def Lista_A_CSV():
    print("En espera")

def CSV_A_Lista():
    print("En espera")

while (True):
    #CSV_A_Lista()
    
    ruta = os.path.abspath(os.getcwd())
    archivo_trabajo=ruta+"\\ventas_info.csv"
    if os.path.exists(archivo_trabajo):
        with open("ventas_info.csv", "r") as archivo: #El "r" es modo lectura
            lector = csv.reader(archivo, delimiter=',')
            registros = 0

            for clav, deta, mont, fech in lector:
                if registros == 0:
                    encabezados = (clav, deta, mont, fech)
                    registros = registros + 1
                else:
                    clav = int(clav)
                    #deta = list([deta])
                    mont = float(mont)
                    fecha_procesada = datetime.datetime.strptime(fech, "%d/%m/%Y").date()                    
                    ventas_list.append([clav, deta, mont, fecha_procesada])
        archivo.close()
    else:
        with open("datos.csv", "w", newline="") as archivo:
            registrador = csv.writer(archivo)
            registrador.writerow(encabezados)
            archivo.close()
    
    menuPrincipal()
    opcion = input("¿Qué opción deseas?: ")
    respuesta = 1
    if opcion=="1":
        while respuesta == 1:
            desc_articulo = input("\nDescripción articulo: ")
            cant_pzas = int(input("Cantidad de piezas: "))
            precio_venta = float(input("Precio de venta: "))
            estructuraArticulo = {'Nombre':desc_articulo, 'Cantidad':cant_pzas, 'Precio':precio_venta}

            subtotal = cant_pzas * precio_venta
            lista_subtotales.append(subtotal)
            
            detalle.append(estructuraArticulo)
                            
            respuesta = int(input("\n¿Deseas elegir otro articulo? \n (1-Si / 0-No): "))
        
        for x in lista_subtotales:
            monto_total = monto_total + x #monto_total = sum(lista_subtotales)

        id_venta = int(input("\nIngresa el número de venta: "))
        fecha_capturada = input("Ingresa la fecha en que se realiza la venta (dd/mm/aaaa): ")
        fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date() #fecha_actual = datetime.date.today()
        venta = [id_venta,detalle,monto_total,fecha_capturada]
        ventas_list.append(venta)
        print("\nEl monto total es: ${:.2f}" .format(monto_total) + " mxn" + f"\nVenta: #{venta[0]} - Fecha captura: {venta[3]}")
        
        if bool(os.path.isfile("ventas_info.csv")) == True:
            with open ("ventas_info.csv",'a+',newline='') as archivo:
                registros = csv.writer(archivo)
                registros.writerows(ventas_list)
        else:               
            with open ("ventas_info.csv",'w',newline='') as archivo:
                registros = csv.writer(archivo)
                registros.writerow(encabezados)
                registros.writerows(ventas_list)
                
        estructuraArticulo = {}
        lista_subtotales = []
        detalle = []
        venta = []
        #ventas_list = []        
    elif opcion=="2":
        if ventas_list:
            df = pd.read_csv("ventas_info.csv")
            registro = pd.DataFrame(df)
            clave_buscar = int(input("\nDime la clave de la venta que deseas consultar: "))
            
            print(f"{encabezados[0]} \t", end="")
            print(f"{encabezados[1]} \t", end="")
            print(f"{encabezados[2]} \t", end="")
            print(encabezados[3])

            for i in registro.index:
                if registro['No. Venta'][i] == clave_buscar:

                    valor1 = registro['No. Venta'][i]
                    valor2 = registro['Detalles'][i]
                    valor3 = registro['Monto'][i]
                    valor3 = registro['Fecha'][i]
                    print (f"{valor1}\t\t{valor2}\t{valor3}\t{valor3}")
                    print("\n")
                #else:
                    #print("\nNo existen ventas con esa clave")
        else:
            print("No hay registros de ventas para mostrar..")
    elif opcion=="3":
        if ventas_list:
            fecha_capturada = input("\nIngresa la fecha de consulta (dd/mm/aaaa): ")
            fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
            
            print(f"{encabezados[0]} \t", end="")
            print(f"{encabezados[1]} \t", end="")
            print(f"{encabezados[2]} \t", end="")
            print(encabezados[3])
            
            for venta in ventas_list:
                fecha = venta[:][3]
                if fecha == fecha_procesada:
                    print(venta)
                else:
                    print("\nNo hay ventas con esa fecha")
        else:
            print("No hay registros de ventas para mostrar..")
            fecha_capturada = ""
    elif opcion=="4":
        #Lista_A_CSV()

        if bool(os.path.isfile("ventas_info.csv")) == True:
            with open ("ventas_info.csv",'a+',newline='') as archivo:
                registros = csv.writer(archivo)
                registros.writerows(ventas_list)
        else:               
            with open ("ventas_info.csv",'w',newline='') as archivo:
                registros = csv.writer(archivo)
                registros.writerow(encabezados)
                registros.writerows(ventas_list)
        
        print("Saliendo...")
        break
    else:
        print ("\nNo has pulsado ninguna opción correcta...\nPulsa una tecla para continuar.")
