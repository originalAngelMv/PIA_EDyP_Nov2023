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