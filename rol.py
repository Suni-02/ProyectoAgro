from db import obtener_conexion_db

def insertar_rol(Nombre_rol):
    conexion = obtener_conexion_db()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Rol(Nombre_rol) VALUES (%s)",
        (Nombre_rol,))
    conexion.commit()
    conexion.close()

def obtener_rol(query):
    conexion = obtener_conexion_db()
    rols = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        rols = cursor.fetchall()
    conexion.close()
    return rols