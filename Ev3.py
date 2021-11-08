import sys
import datetime
import sqlite3
from sqlite3 import Error

from collections import namedtuple
datos =("fecha","Descripcion", "Cantidad", "Precio", "total")


switch = True
diccionario_ventas={}
lista_ventas=[]
Detalle = namedtuple("venta", ("fecha","Descripcion", "Cantidad", "Precio", "total"))
total2= 0
i=0

try:
    with sqlite3.connect("Evidencia.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Ventas (folio INT, fecha TIMESTAMP NOT NULL, descripcion TEXT NOT NULL,cantidad NUMERIC, precio NUMERIC, total NUMERIC );")
        print("Tabla creada exitosamente")
except Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

while switch:

    print("--------------MENU REGISTRO DE VENTAS-----------")
    print("¿Qué desea realizar?")
    print("1: Registrar una venta ")
    print("2: Consultar una venta por folio")
    print("3: Genererar Reporte")
    print("4: Salir del programa")
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        masasrticulos = True
        

        folio = int(input("Ingrese su folio: "))
        if not folio in diccionario_ventas.keys():
            fecha = input("Ingrese la fecha: ")
            while masasrticulos:
            #folio2=input("ingresa el ID del articulo: ")
                descripcion=input("Ingrese la descripcion: ")
                fol=folio
                cantidad=int(input("Ingrese la cantidad: "))
                precio=int(input("Ingrese el precio: "))
                resp=str(input("¿Desea agregar otro producto? Si/No: ")).upper()
                if resp != "SI":
                    masasrticulos=False
        
                iva=(precio*cantidad)*0.16
                total=(precio*cantidad)+iva
                total2= total2 + total
                Venta_Registrada=Detalle(fecha,descripcion,cantidad,precio,total)
                lista_ventas.append(Venta_Registrada)
                print("El total con iva incluido es: ",total2)
                try:
                     with sqlite3.connect("Evidencia.db") as conn: #Puente
                         mi_cursor=conn.cursor()
                         mi_cursor.execute('INSERT INTO Ventas VALUES(?,?,?,?,?,?);',(fol,fecha,descripcion,cantidad,precio,total,))
                         print("Registro agregado exitosamente")
                except Error as e:
                       print (e)
                except Exception:
                     print(f"Se produjo el siguiente error: {sys.exc_info()[0]}") 
        
        else:

            print("Esta venta ya está registrada, intente de nuevo. ")
        diccionario_ventas[folio] = lista_ventas

    elif opcion == "2":
        clave_buscar = int(input("Ingresa el folio de la compra que realizaste: "))
        try:
            with sqlite3.connect("Evidencia.db") as conn:
                c=conn.cursor()
                c.execute("SELECT DISTINCT fecha, descripcion, cantidad, precio, total FROM Ventas WHERE folio = ?",(clave_buscar,))
                registros = c.fetchall()
                print("FECHA\t\tDESCRIPCION\t\tCANTIDAD\t\tPRECIO\t\tTOTAL")
                print("-----------------------------------------------------------------------------------------")
                for fecha, descripcion, cantidad, precio, total in registros:
                    print(f"{fecha}\t{descripcion}\t\t\t{cantidad}\t\t\t{precio}\t\t{total}")

        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

    elif opcion == "3":
        fecha_reporte = input("Ingrese La Fecha (dd/mm/aaaa): \n")
        fecha_consulta = datetime.datetime.strptime(fecha_reporte, "%d/%m/%Y").date()
        try:
            with sqlite3.connect("Evidencia.db") as conn:
                c = conn.cursor()
                criterio = {"fecha":fecha_consulta}
                c.execute("SELECT DISTINCT fecha, descripcion, cantidad, precio, total FROM Ventas WHERE fecha = ?", (fecha_reporte,))
                registros = c.fetchall()
                print("FECHA\t\tDESCRIPCION\t\tCANTIDAD\t\tPRECIO\t\tTOTAL")
                print("-----------------------------------------------------------------------------------------")
                for fecha, descripcion, cantidad, precio, total in registros:
                    print(f"{fecha}\t{descripcion}\t\t\t{cantidad}\t\t\t{precio}\t\t{total}")
                    
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

    elif opcion == "4":

        print("Saldrás del sistema!")
        
        switch = False
        
    else:

        print("Esa opción no es válida")