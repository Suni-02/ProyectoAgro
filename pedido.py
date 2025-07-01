from db import obtener_conexion_db
from datetime import datetime


def insertar_pedido(id_granjero, id_empresa, total_pedido):
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO Pedido(Id_Granjero, Id_Empresa, Fecha_Pedido, Total_Pedido)
        VALUES (%s, %s, NOW(), %s)
    """, (id_granjero, id_empresa, total_pedido))
    conexion.commit()
    id_pedido = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_pedido


