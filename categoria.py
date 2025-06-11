from db import obtener_conexion_db

def insertar_categoria(Nombre_Categoria):
    conexion = obtener_conexion_db()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO CATEGORIA_PRODUCTO(Nombre_Categoria) VALUES (%s)",
        (Nombre_Categoria,))
    conexion.commit()
    conexion.close()

def obtener_categorias(query):
    conexion = obtener_conexion_db()
    categorias = []
    with conexion.cursor() as cursor:
        cursor.execute(query)
        categorias = cursor.fetchall()
    conexion.close()
    return categorias