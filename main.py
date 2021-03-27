import csv
import os

respuesta = 1
monto_total = 0.00
clave = 0

columnas = ("Desc", "Cant", "Precio", "Sub")
registro = []
detalle = []
ventas_dic = {}

def menuPrincipal():
    print("_______________________________")
    print("\n*** Cosméticos True:BEAUTY! ***")
    print("\n        Menú principal       ")
    print("   [1] Registrar una venta.")
    print("   [2] Consultar una venta.")
    print("   [3] Salir.")
    print("_______________________________")
    print(" ")

while (True):
    menuPrincipal()
    opcion = input("¿Qué opción deseas?: ")
    respuesta = 1
    if opcion=="1":
        while respuesta == 1:
            registro = []

            desc_articulo = input("\nDescripción articulo: ")
            cant_pzas = int(input("Cantidad de piezas: "))
            precio_venta = float(input("Precio de venta: "))
            subtotal = cant_pzas * precio_venta
            registro.append(desc_articulo)
            registro.append(cant_pzas)
            registro.append(precio_venta)
            registro.append(subtotal)
            detalle.append(registro)

            respuesta = int(input("\n¿Deseas elegir otro articulo? \n (1-Si / 0-No): "))
        
        clave = max(ventas_dic, default = 0) + 1
        for elemento in detalle:
            monto_total = monto_total + elemento[3] #monto_total = monto_total + sum(elemento[3] for elemento in detalle)
        print("\nEl monto total es: ${:.2f}" .format(monto_total) + " mxn")
        ventas_dic[clave] = [detalle] #Veredicto final omitir el monto total #ventas_dic[clave] = [detalle, monto_total]
    
        registro = []
        monto_total = 0.0
        detalle = []
    elif opcion=="2":
        if ventas_dic:
            clave_buscar = int(input("\nDime la clave de la venta que deseas consultar: "))
            if clave_buscar in ventas_dic.keys():
                print("Venta encontrada...")
                print(f"\nDetalles de venta: #{clave_buscar}\n")
                venta_encontrada = ventas_dic.get(clave_buscar) #venta_encontrada = list(ventas_dic[clave_buscar]) #print(ventas_dic[clave_buscar])
                num = 0
                print("     " + columnas[0] + "  " + columnas[1] + "  " + columnas[2] + "  " + columnas[3])
                for conjunto in venta_encontrada:
                    for articulo in conjunto:
                        num = num + 1
                        print(f"{num}- {articulo}")
                        monto_total = monto_total + articulo[3]
                print("\nMonto total fue: ${:.2f}" .format(monto_total) + " mxn")
            else:
                print("\nNo hay registros con esa clave")
        else:
            print("No hay registros de ventas para mostrar..")
    elif opcion=="3":
        print("Saliendo...")
        break
    else:
        print ("\nNo has pulsado ninguna opción correcta...\nPulsa una tecla para continuar.")
