import sqlite3
import sys
from sqlite3 import Error
import datetime
import csv
import openpyxl
import re
import pandas as pd

try:
    with sqlite3.connect('notas.db') as conn:
        mi_cursor = conn.cursor()
        
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id_cliente INTEGER PRIMARY KEY, \
        nombre_cliente TEXT NOT NULL, \
        RFC_cliente TEXT NOT NULL, \
        correo_cliente TEXT NOT NULL, \
        estado_cliente TEXT NOT NULL);")
        
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS servicios (id_servicio INTEGER PRIMARY KEY, \
        nombre_servicio TEXT NOT NULL, \
        costo_servicio REAL NOT NULL, \
        estado_servicio TEXT NOT NULL);")
        
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS notas (id_nota INTEGER PRIMARY KEY, \
        fecha_nota timestamp, \
        id_cliente INTEGER NOT NULL, \
        monto_a_pagar REAL NOT NULL, \
        estado_nota TEXT NOT NULL, \
        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente));")
        
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS detalles_notas (id_detalle INTEGER PRIMARY KEY, \
        id_nota INTEGER NOT NULL, \
        id_servicio INTEGER NOT NULL, \
        FOREIGN KEY(id_nota) REFERENCES notas(id_nota), \
        FOREIGN KEY(id_servicio) REFERENCES servicios(id_servicio));")  
except sqlite3.Error as e:
    print(e)
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conn):
        conn.close()
        
def imprimir_nota(id_nota):
    with sqlite3.connect('notas.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        mi_cursor = conn.cursor()
        mi_cursor.execute("SELECT n.id_nota, n.fecha_nota, c.nombre_cliente, c.RFC_cliente, c.correo_cliente,n.monto_a_pagar, dn.id_servicio, s.nombre_servicio, s.costo_servicio\
            FROM notas n\
            INNER JOIN clientes c ON n.id_cliente = c.id_cliente\
            INNER JOIN detalles_notas dn ON n.id_nota = dn.id_nota\
            INNER JOIN servicios s ON dn.id_servicio = s.id_servicio\
            WHERE n.id_nota = ?", (id_nota,))

        resultados = mi_cursor.fetchall()

        id_nota, fecha_nota, nombre_cliente, RFC_cliente, correo_cliente, monto_a_pagar = resultados[0][:6]

        print(f"ID Nota: {id_nota}")
        print(f"Fecha de Nota: {fecha_nota.strftime('%d-%m-%Y')}")
        print(f"Cliente: {nombre_cliente}")
        print(f"RFC: {RFC_cliente}")
        print(f"Correo: {correo_cliente}")
        print("*" * 60)

        print(f"{'ID Servicio':<15} {'Nombre del Servicio':<25} {'Costo':<10}")
        print("-" * 50)

        for resultado in resultados:
            id_servicio, nombre_servicio, costo_servicio = resultado[6:]
            print(f"{id_servicio:<15} {nombre_servicio:<25} {costo_servicio:<10.2f}")

        print(f"Monto a Pagar: {monto_a_pagar:.2f}")
id_nota = 1
fecha_actual =datetime.datetime.now()
patron_fecha = r"^\d{2}-\d{2}-\d{4}$"

while True:
    print("""
    ╔══════════════════════╗
    ║   Menu Principal     ║
    ╠══════════════════════╣
    ║ 1. Notas             ║
    ║ 2. Clientes          ║
    ║ 3. Servicios         ║
    ║ 4. Estadísticas      ║ 
    ║ 5. Salir             ║ 
    ╚══════════════════════╝
    """)
    menu_principal = input("Ingrese una opción: ")
    if menu_principal == "1":
        while True:
            print("""
            ╔════════════════════════════╗
            ║           NOTAS            ║
            ╠════════════════════════════╢
            ║ 1. Registrar una nota      ║
            ║ 2. Cancelar una nota       ║
            ║ 3. Recuperar una nota      ║
            ║ 4. Consultas y reportes    ║
            ║ 5. Volver al menú principal║
            ╚════════════════════════════╝
            """)
            menu_notas = input("Ingrese una opción del menú de Notas: ")
            if menu_notas == "1":
                try:
                    with sqlite3.connect('notas.db') as conn:
                        mi_cursor = conn.cursor()
                        mi_cursor.execute("SELECT id_cliente, nombre_cliente FROM clientes WHERE estado_cliente = 'ACTIVO'")
                        clientes_registrados = mi_cursor.fetchall()
                        print("\nMenú de Clientes:")
                        if  clientes_registrados:
                            print("ID Cliente | Nombre Cliente")
                            print("-" * 26)  

                            for id_cliente, nombre_cliente in clientes_registrados:
                                id_cliente_str = str(id_cliente).rjust(10)
                                nombre_cliente = nombre_cliente.ljust(15)
                                print(f"{id_cliente_str} | {nombre_cliente}")
                            else:
                                print("*"*40)
                        else:
                            print("\nNO hay Clientes desponibles...\n")   
                        mi_cursor.execute("SELECT id_servicio, nombre_servicio, costo_servicio FROM servicios WHERE estado_servicio = 'ACTIVO'")
                        servicio_registrados = mi_cursor.fetchall()
                        print("\nMenú de Servicios:")
                        if servicio_registrados:
                            print(f"{'ID Servicio':<10} | {'Nombre de Servicio':<30} | {'Costo de Servicio':<15}")
                            print("-" * 70)

                            for id_servicio, nombre_servicio, costo_servicio in servicio_registrados:
                                id_servicio_str = str(id_servicio).rjust(11)
                                nombre_servicio = nombre_servicio.ljust(30)
                                costo_servicio = f'{costo_servicio:.2f}'.ljust(15)
                                print(f"{id_servicio_str} | {nombre_servicio} | {costo_servicio}")
                        else:
                            print("NO hay Servicios disponibles")
                        
                        patron_fecha = r"^\d{2}-\d{2}-\d{4}$"
                        
                        pregunta = input("\nDesea una nota? (ENTER PARA SALIR / [S] para seguir a delante)").strip().upper()
                        if pregunta =="":
                            break
                        
                        while True:
                            
                            fecha_ingresada_str = input("\nFecha de la nota (dd-mm-aaaa): ").strip()
                            
                            if not fecha_ingresada_str:
                                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
                            elif not re.match(patron_fecha, fecha_ingresada_str):
                                print("FORMATO DE FECHA INCORRECTO. DEBE SER DD-MM-AAAA")
                            else:
                                try:
                                    fecha_ingresada = datetime.datetime.strptime(fecha_ingresada_str, "%d-%m-%Y")
                                    if fecha_ingresada > fecha_actual:
                                        print("LA FECHA NO DEBE SER POSTERIOR A LA FECHA ACTUAL DEL SISTEMA")
                                    else:
                                        break
                                except ValueError:
                                    print("LA FECHA NO ES VÁLIDA/NO EXISTE. INTENTE DENUEVO.")
                        while True:
                            id_cliente = input("\nID del cliente: ").strip()
                            
                            if not id_cliente.isdigit():
                                print("El ID del cliente debe ser un número. Intente nuevamente.")
                            else:
                                mi_cursor.execute("SELECT nombre_cliente FROM clientes WHERE id_cliente = ? AND estado_cliente = 'ACTIVO'", (id_cliente,))
                                cliente_existente = mi_cursor.fetchone()
                                if cliente_existente:
                                    break
                                else:
                                    print("El cliente con ese ID no existe en la base de datos. Intente nuevamente.")
                        while True:
                            mi_cursor.execute("SELECT COUNT(*) FROM notas WHERE id_nota = ?", (id_nota,))
                            cuenta = mi_cursor.fetchone()[0]
                            if cuenta == 0:
                                break
                            else:
                                id_nota += 1
                                
                        estado = "ACTIVO"
                        monto_a_pagar = 0.0
                        cantidad_servicio = 0
                        while True:
                            id_servicio = input("\nIngrese el ID_servicio agregar / ( 0 para terminar la captura.): ").strip()
                            if not id_servicio:
                                print("EL DATO NO PUEDE OMITIRSE. INTENTE NUEVAMENTE.")
                                continue
                            elif id_servicio == "0":
                                if cantidad_servicio>0:
                                    break
                                else:
                                    print("La nota tiene que tener por lo menos un servicio. Intente nuevamente")
                            else:
                                mi_cursor.execute("SELECT nombre_servicio,costo_servicio FROM servicios WHERE id_servicio = ? AND estado_servicio = 'ACTIVO'", (id_servicio,))
                                servicio_encontrado = mi_cursor.fetchone()
                                if servicio_encontrado:
                                    cantidad_servicio+=1
                                    nombre_servicio, costo_servicio = servicio_encontrado
                                    monto_a_pagar += costo_servicio
                                    mi_cursor.execute("INSERT INTO detalles_notas (id_nota, id_servicio) VALUES (?, ?)", (id_nota, id_servicio))
                                    print("Servicio agregado con éxito")
                                    continue
                                else:
                                    print("El Servicio con ese ID no existe en la base de datos. Intente nuevamente.")
                        valores = (id_nota,fecha_ingresada,id_cliente,monto_a_pagar,estado)
                        mi_cursor.execute("INSERT INTO notas VALUES (?,?,?,?,?)",valores)
                        print("\nNota creada con éxito.")
                except sqlite3.Error as e:
                    print(e)
                except Exception as ex:
                    print(f"Se produjo el siguiente error: {ex}")
                imprimir_nota(id_nota)
            elif menu_notas == "2":
                pass
            elif menu_notas == "3":
                pass
            elif menu_notas == "4":
                pass
            elif menu_notas == "5":
                print("Fuera del menú de notas.")
                break
            else:
                print("OPCIÓN NO VALIDA. INTENTE NUEVAMENTE.")
    elif menu_principal == "2":
        pass
    elif menu_principal == "3":
        pass
    elif menu_principal == "4":
        pass
    elif menu_principal == "5":
        pass
    else:
        print("OPCIÓN NO VALIDA. INTENTE NUEVAMENTE.")