import pymysql

def obtener_conexion_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        db='ProyectoAgro2'
        )
