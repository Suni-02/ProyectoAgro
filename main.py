from flask import Flask, render_template,request,redirect, session, flash
from categoria import insertar_categoria, obtener_categorias
from producto import insertar_producto, obtener_productos_con_usuario
from categoria import insertar_categoria
from rol import insertar_rol,obtener_rol
from usuario import insertar_Usuario, login_usuario
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
    # Obtener datos del formulario
    nombre = request.form["Nombre"]
    dni = request.form["Dni"]
    telefono = request.form["Telefono"]
    id_rol = request.form["Rol"]  # ID del rol seleccionado
    nombre_e = request.form["Nombre_E"]
    email = request.form["Email"]
    password = request.form["password"]
    descripcion = request.form["descripcion"]
    estado_usuario = 1  # o puedes obtenerlo si lo necesitas dinámico

    # Llama a la función para insertar en la base de datos
    insertar_Usuario(nombre, dni, telefono, id_rol, nombre_e, email, password, descripcion, estado_usuario)

    return redirect("/login")
    
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
    productos = obtener_productos_con_usuario()
    return render_template("productos.html", productos=productos)



@app.route('/crear_producto')
def crear_producto():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para crear productos", "warning")
        return redirect("/crear_producto")
    
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



app.run(debug= True)