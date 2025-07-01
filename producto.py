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


def obtener_productos_con_usuario(id_usuario):
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    sql = """
    SELECT 
        p.Id_Producto, 
        p.Nombre_Producto, 
        p.Precio, 
        u.Nombre,
        c.Nombre_Categoria,
        u.Id_Usuario

    FROM producto p
    JOIN usuario u ON p.Id_Usuario = u.Id_Usuario
    JOIN categoria_producto c ON p.Id_Categoria = c.Id_Categoria
    WHERE p.Id_Usuario = %s
    """
    cursor.execute(sql, (id_usuario,))
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos




def obtener_productos_todos():
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    sql = """
    SELECT 
        p.Nombre_Producto, 
        p.Precio, 
        u.Nombre, 
        c.Nombre_Categoria, 
        u.Id_Usuario
    FROM producto p
    JOIN usuario u ON p.Id_Usuario = u.Id_Usuario
    JOIN Categoria_Producto c ON p.Id_Categoria = c.Id_Categoria
    """
    cursor.execute(sql)
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos


def obtener_productos_por_categoria(id_categoria):
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    sql = """
    SELECT 
        p.Nombre_Producto, 
        p.Precio, 
        u.Nombre, 
        c.Nombre_Categoria, 
        u.Id_Usuario
    FROM producto p
    JOIN usuario u ON p.Id_Usuario = u.Id_Usuario
    JOIN Categoria_Producto c ON p.Id_Categoria = c.Id_Categoria
    WHERE p.Id_Categoria = %s
    """
    cursor.execute(sql, (id_categoria,))
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos



