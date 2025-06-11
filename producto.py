from db import obtener_conexion_db
def insertar_producto(nombre, precio, id_categoria, id_usuario):
    connection = obtener_conexion_db()
    cursor = connection.cursor()
    sql = "INSERT INTO producto (Nombre_Producto, Precio, Id_Categoria, Id_Usuario) VALUES (%s, %s, %s, %s)"
    valores = (nombre, precio, id_categoria, id_usuario)
    cursor.execute(sql, valores)
    connection.commit()
    cursor.close()
    connection.close()

from db import obtener_conexion_db

def obtener_productos_con_usuario():
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    sql = """
    SELECT p.Nombre_Producto, p.Precio, u.Nombre
    FROM producto p
    JOIN usuario u ON p.Id_Usuario = u.Id_Usuario
    """
    cursor.execute(sql)
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

