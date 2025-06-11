from db import obtener_conexion_db
from werkzeug.security import generate_password_hash,check_password_hash

def insertar_Usuario(Nombre, Dni, Telefono, Id_Rol, Nombre_E, Email, password, Descripcion, Estado_usuario):
    conexion = obtener_conexion_db()
    with conexion.cursor() as cursor:
        
        cursor.execute("SELECT * FROM Usuario WHERE Dni = %s", (Dni,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            conexion.close()
            return "DNI ya registrado"  
        
        password_hasheada = generate_password_hash(password)

        
        cursor.execute("""
            INSERT INTO Usuario(Nombre, Dni, Telefono, Id_Rol, Nombre_E, Email, password, Descripcion, Estado_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (Nombre, Dni, Telefono, Id_Rol, Nombre_E, Email, password_hasheada, Descripcion, Estado_usuario))
        
        conexion.commit()
    conexion.close()
    return "Usuario registrado correctamente"

def login_usuario(Dni, password):
    conexion = obtener_conexion_db()
    with conexion.cursor() as cursor:
        # JOIN para obtener el nombre del rol desde la tabla Rol
        cursor.execute("""
            SELECT u.Id_Usuario, u.Nombre, u.Dni, u.Telefono, r.Nombre_rol, 
                u.Nombre_E, u.Email, u.Password, u.Descripcion
            FROM Usuario u
            JOIN Rol r ON u.Id_Rol = r.Id_Rol
            WHERE u.Dni = %s
        """, (Dni,))
        
        usuario = cursor.fetchone()

        if not usuario:
            conexion.close()
            return {"success": False, "message": "DNI no registrado"}

        hashed_password = usuario[7]  # Columna Password
        if check_password_hash(hashed_password, password):
            datos_usuario = {
                "id": usuario[0],          # Id_Usuario
                "nombre": usuario[1],      # Nombre
                "Dni": usuario[2],         # Dni
                "telefono": usuario[3],    # Telefono
                "rol": usuario[4],         # ✅ Nombre_rol
                "empresa": usuario[5],     # Nombre_E
                "email": usuario[6],       # Email
                "descripcion": usuario[8]  # Descripcion
            }
            conexion.close()
            return {"success": True, "message": "Login exitoso", "usuario": datos_usuario}
        else:
            conexion.close()
            return {"success": False, "message": "Contraseña incorrecta"}
