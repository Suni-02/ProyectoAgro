from flask import Flask, render_template,request,redirect, session, flash
from categoria import insertar_categoria, obtener_categorias
from producto import insertar_producto, obtener_productos_con_usuario
from categoria import insertar_categoria
from rol import insertar_rol,obtener_rol
from usuario import insertar_Usuario, login_usuario
from pedido import insertar_pedido
from db import obtener_conexion_db
app = Flask(__name__)
app.secret_key = "grupoAgro" 
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register')
def register():
    roles = obtener_rol("SELECT * FROM ROL")
    return render_template("register.html", roles=roles)

@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    nombre = request.form["Nombre"]
    dni = request.form["Dni"]
    telefono = request.form["Telefono"]
    id_rol = request.form["Rol"]
    nombre_e = request.form["Nombre_E"]
    email = request.form["Email"]
    password = request.form["password"]
    descripcion = request.form["descripcion"]
    estado_usuario = 1

    resultado = insertar_Usuario(nombre, dni, telefono, id_rol, nombre_e, email, password, descripcion, estado_usuario)
    if resultado["success"]:
        flash(resultado["message"], "success")
        return redirect("/login")
    else:
        flash(resultado["message"], "danger")
        return redirect("/register")

    
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        Dni = request.form["Dni"]
        password = request.form["password"]
        
        resultado = login_usuario(Dni, password)

        if resultado["success"]:
            session["usuario_id"] = resultado["usuario"]["id"]
            session["nombre"] = resultado["usuario"]["nombre"]
            session["telefono"] = resultado["usuario"]["telefono"]
            session["rol"] = resultado["usuario"]["rol"]
            session["empresa"] = resultado["usuario"]["empresa"]
            session["email"] = resultado["usuario"]["email"]
            session["descripcion"] = resultado["usuario"]["descripcion"]
            flash("Inicio de sesión exitoso", "success")
            return redirect("/perfil")
        else:
            flash(resultado["message"], "danger")

    return render_template("login.html")

@app.route('/perfil_publico/<int:id_usuario>')
def perfil_publico(id_usuario):
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    sql = """
        SELECT Nombre, Telefono, Nombre_E, Email, Descripcion, r.Nombre_rol
        FROM usuario u
        JOIN rol r ON u.Id_Rol = r.Id_Rol
        WHERE Id_Usuario = %s
    """
    cursor.execute(sql, (id_usuario,))
    datos = cursor.fetchone()
    cursor.close()
    conexion.close()

    if datos:
        usuario = {
            "nombre": datos[0],
            "telefono": datos[1],
            "empresa": datos[2],
            "email": datos[3],
            "descripcion": datos[4],
            "rol": datos[5]
        }
        return render_template("perfil_publico.html", usuario=usuario)
    else:
        flash("Usuario no encontrado", "warning")
        return redirect("/")

@app.route('/categoria')
def categoria():
    return render_template("categoria.html")

@app.route('/ver_categorias')
def ver_categorias():
    categorias = obtener_categorias()  # Obtenemos los datos desde la base
    return render_template("ver_categorias.html", categorias=categorias)


@app.route("/nueva_categoria", methods=["POST"])
def nueva_categoria():
    nombre = request.form["Nombre_Categoria"]  # Obtiene el valor del input
    insertar_categoria(nombre)  # Llama tu función
    return redirect("/categoria") 

@app.route('/perfil')
def perfil():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión primero", "warning")
        return redirect("/login")

    datos_usuario = {
        "id": session["usuario_id"],
        "nombre": session["nombre"],
        "telefono": session["telefono"],
        "rol": session["rol"],
        "empresa": session["empresa"],
        "email": session["email"],
        "descripcion": session["descripcion"]
    }

    return render_template("perfil.html", usuario=datos_usuario)

@app.route('/productos')
def mostrar_productos():
    if "usuario_id" not in session:
        flash("Debes registrarte o iniciar sesión para ver los productos", "warning")
        return redirect("/login")
    
    id_usuario = session["usuario_id"]
    productos = obtener_productos_con_usuario(id_usuario)
    return render_template("productos.html", productos=productos)



@app.route('/crear_producto')
def crear_producto():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para crear productos", "warning")
        return redirect("/login")
    
    from categoria import obtener_categorias  # Lo traemos aquí para evitar dependencia circular si la hay
    categorias = obtener_categorias("SELECT * FROM Categoria_Producto")
    return render_template("crear_producto.html", categorias=categorias)


@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para guardar productos", "warning")
        return redirect("/login")
    
    nombre = request.form['nombre_producto']
    precio = request.form['precio']
    id_categoria = request.form['id_categoria']
    id_usuario = session['usuario_id']

    insertar_producto(nombre, precio, id_categoria, id_usuario)
    flash("Producto guardado exitosamente", "success")
    return redirect("/productos")  # o a donde quieras redirigir


@app.route('/editar_producto/<int:id_producto>', methods=["GET", "POST"])
def editar_producto(id_producto):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para editar productos", "warning")
        return redirect("/login")
    
    from categoria import obtener_categorias
    
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    
    if request.method == "POST":
        nombre = request.form["nombre_producto"]
        precio = request.form["precio"]
        id_categoria = request.form["id_categoria"]
        
        sql = """
        UPDATE producto
        SET Nombre_Producto=%s, Precio=%s, Id_Categoria=%s
        WHERE Id_Producto=%s
        """
        valores = (nombre, precio, id_categoria, id_producto)
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        
        flash("Producto actualizado exitosamente", "success")
        return redirect("/productos")
    else:
        # obtener datos del producto
        sql = """
        SELECT Nombre_Producto, Precio, Id_Categoria
        FROM producto
        WHERE Id_Producto=%s
        """
        cursor.execute(sql, (id_producto,))
        producto = cursor.fetchone()
        categorias = obtener_categorias("SELECT * FROM Categoria_Producto")
        cursor.close()
        conexion.close()
        
        return render_template("editar_producto.html", producto=producto, categorias=categorias, id_producto=id_producto)

@app.route('/eliminar_producto/<int:id_producto>')
def eliminar_producto(id_producto):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para eliminar productos", "warning")
        return redirect("/login")
    
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    sql = "DELETE FROM producto WHERE Id_Producto=%s"
    cursor.execute(sql, (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    flash("Producto eliminado correctamente", "info")
    return redirect("/productos")


@app.route('/productos_comprador', methods=['GET', 'POST'])
def productos_comprador():
    from producto import obtener_productos_todos, obtener_productos_por_categoria
    from categoria import obtener_categorias
    
    categorias = obtener_categorias("SELECT * FROM Categoria_Producto")

    if request.method == "POST":
        id_categoria = request.form.get("id_categoria")
        
        # Si no seleccionaron nada o eligen "todas"
        if not id_categoria or id_categoria == "":
            productos = obtener_productos_todos()
        else:
            productos = obtener_productos_por_categoria(id_categoria)
    else:
        productos = obtener_productos_todos()
    
    return render_template("productos_comprador.html", productos=productos, categorias=categorias)







@app.route('/rol')
def rol():
    return render_template("rol.html")

@app.route("/nuevo_rol", methods=["POST"])
def nuevo_rol():
    nombre = request.form["Nombre_rol"]  # Obtiene el valor del input
    insertar_rol(nombre)  # Llama tu función
    return redirect("/rol") 

@app.route("/logout")
def logout():
    session.clear()  # Elimina todos los datos de sesión
    flash("Sesión cerrada correctamente", "info")
    return redirect("/login")  # Redirige al login u otra ruta


# --------------------
# RUTA: crear_pedido
# --------------------
@app.route("/crear_pedido", methods=["GET", "POST"])
def crear_pedido():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para crear pedidos", "warning")
        return redirect("/login")

    if session["rol"] != "Granjeros":
        flash("Solo los granjeros pueden crear pedidos", "danger")
        return redirect("/")

    if request.method == "POST":
        id_granjero = session["usuario_id"]
        id_empresa = request.form["id_empresa"]

        conexion = obtener_conexion_db()
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO Pedido (Id_Granjero, Id_Empresa, Fecha_Pedido, Total_Pedido)
                VALUES (%s, %s, NOW(), 0)
            """
            cursor.execute(sql, (id_granjero, id_empresa))
            id_pedido = cursor.lastrowid
            conexion.commit()
        conexion.close()

        flash("Pedido creado correctamente. Ahora agrega los productos.", "success")
        return redirect(f"/agregar_detalle_pedido/{id_pedido}")

    return render_template("crear_pedido.html")


# --------------------
# RUTA: agregar_detalle_pedido
# --------------------
@app.route("/agregar_detalle_pedido/<int:id_pedido>", methods=["GET", "POST"])
def agregar_detalle_pedido(id_pedido):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión primero", "warning")
        return redirect("/login")

    id_granjero = session["usuario_id"]

    conexion = obtener_conexion_db()
    cursor = conexion.cursor()

    if request.method == "POST":
        ids_productos = request.form.getlist("id_producto[]")
        cantidades = request.form.getlist("cantidad[]")

        for id_prod, cant in zip(ids_productos, cantidades):
            if id_prod and cant:
                cantidad = int(cant)
                cursor.execute("SELECT Precio FROM Producto WHERE Id_Producto=%s", (id_prod,))
                precio_unitario = cursor.fetchone()[0]
                precio_total_producto = precio_unitario * cantidad

                try:
                    cursor.execute("""
                        INSERT INTO Detalle_Pedido (Id_Pedido, Id_Producto, Cantidad, Precio)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE Cantidad=VALUES(Cantidad), Precio=VALUES(Precio)
                    """, (id_pedido, id_prod, cantidad, precio_total_producto))
                    conexion.commit()
                except Exception as e:
                    flash(f"Error al agregar detalle: {e}", "danger")

        # actualizar total
        cursor.execute("""
            SELECT SUM(Precio)
            FROM Detalle_Pedido
            WHERE Id_Pedido=%s
        """, (id_pedido,))
        total_actualizado = cursor.fetchone()[0] or 0

        cursor.execute("""
            UPDATE Pedido
            SET Total_Pedido = %s
            WHERE Id_Pedido = %s
        """, (total_actualizado, id_pedido))
        conexion.commit()

        # si se presionó el botón Finalizar
        if request.form.get("finalizar"):
            flash("Pedido finalizado correctamente", "success")
            return redirect("/pedidos_granjero")

        # si no, sigue agregando productos
        flash("Productos agregados correctamente", "success")
        return redirect(f"/agregar_detalle_pedido/{id_pedido}")

    # productos disponibles
    cursor.execute("""
        SELECT Id_Producto, Nombre_Producto
        FROM Producto
        WHERE Id_Usuario=%s
    """, (id_granjero,))
    productos = cursor.fetchall()

    # productos ya agregados
    cursor.execute("""
        SELECT d.Id_Producto, p.Nombre_Producto, d.Cantidad, d.Precio
        FROM Detalle_Pedido d
        JOIN Producto p ON d.Id_Producto = p.Id_Producto
        WHERE d.Id_Pedido=%s
    """, (id_pedido,))
    detalles = cursor.fetchall()

    cursor.execute("""
        SELECT Total_Pedido
        FROM Pedido
        WHERE Id_Pedido=%s
    """, (id_pedido,))
    total_pedido = cursor.fetchone()[0] or 0

    cursor.close()
    conexion.close()

    return render_template("agregar_detalle_pedido.html", productos=productos, detalles=detalles, id_pedido=id_pedido, total_pedido=total_pedido)

# --------------------
# RUTA: pedidos_empresa
# --------------------
@app.route('/pedidos_empresa')
def pedidos_empresa():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para ver tus pedidos", "warning")
        return redirect("/login")
    
    if session["rol"] != "Empresa":
        flash("Solo las empresas pueden ver esta lista", "danger")
        return redirect("/")

    id_empresa = session["usuario_id"]

    conexion = obtener_conexion_db()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT p.Id_Pedido, p.Total_Pedido, u.Nombre AS nombre_granjero
        FROM Pedido p
        JOIN usuario u ON p.Id_Granjero = u.Id_Usuario
        WHERE p.Id_Empresa = %s
    """, (id_empresa,))
    
    pedidos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("pedidos_empresa.html", pedidos=pedidos)

# --------------------
# RUTA: pedidos_granjero
# --------------------
@app.route('/pedidos_granjero')
def pedidos_granjero():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para ver tus pedidos", "warning")
        return redirect("/login")
    
    if session["rol"] != "Granjeros":
        flash("Solo los granjeros pueden ver esta lista", "danger")
        return redirect("/")

    id_granjero = session["usuario_id"]

    conexion = obtener_conexion_db()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT p.Id_Pedido, p.Total_Pedido, u.Nombre_E AS nombre_empresa
        FROM Pedido p
        JOIN usuario u ON p.Id_Empresa = u.Id_Usuario
        WHERE p.Id_Granjero = %s
    """, (id_granjero,))
    
    pedidos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("pedidos_granjero.html", pedidos=pedidos)

@app.route('/detalle_pedido/<int:id_pedido>')
def detalle_pedido(id_pedido):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect("/login")
    
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT d.Id_Producto, p.Nombre_Producto, d.Cantidad, d.Precio
        FROM Detalle_Pedido d
        JOIN Producto p ON d.Id_Producto = p.Id_Producto
        WHERE d.Id_Pedido = %s
    """, (id_pedido,))
    
    detalles = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return render_template("detalle_pedido.html", detalles=detalles, id_pedido=id_pedido)

@app.route('/detalle_pedido_granjero/<int:id_pedido>')
def detalle_pedido_granjero(id_pedido):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect("/login")
    
    if session["rol"] != "Granjeros":
        flash("No tienes permiso para ver este detalle", "danger")
        return redirect("/")
    
    conexion = obtener_conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT d.Id_Producto, p.Nombre_Producto, d.Cantidad, d.Precio
        FROM Detalle_Pedido d
        JOIN Producto p ON d.Id_Producto = p.Id_Producto
        WHERE d.Id_Pedido = %s
    """, (id_pedido,))
    
    detalles = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return render_template("detalle_pedido_granjero.html", detalles=detalles, id_pedido=id_pedido)


app.run(debug= True)