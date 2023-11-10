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