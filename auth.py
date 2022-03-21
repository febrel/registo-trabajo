import functools
from flask import Blueprint
from flask import (flash, g, render_template, request, url_for, session, redirect)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

# Todas las funciones con todas las rutas esta va ser la ruta /auth
bp = Blueprint("auth",__name__, url_prefix="/auth")

@bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        cedula = request.form["cedula"]
        nombres = request.form["nombres"]
        correo = request.form["correo"]
        username = request.form["username"]
        password = request.form["password"]

        # invoco DB
        db,c = get_db()
        error = None

        c.execute("SELECT id FROM usuarios WHERE usuario = %s", (username,))

        # Para mensaje error
        if not username:
            error = "Username es requerido"
        if not password:

            error = "Password es requerido"
        elif c.fetchone() is not None:
            error = "Usuario {} se encuentra registrado".format(username)

        # Validar que no tengamos ningun error
        if error is None:
            c.execute("INSERT INTO usuarios(cedula, nombres, correo, usuario, password, estado) VALUES (%s, %s, %s, %s, %s, %s)",(cedula, nombres, correo, username, generate_password_hash(password),1)) # Encripta
            db.commit()
            return redirect(url_for("auth.login"))# Llamamos a login

        flash(error)
    return render_template("register.html")


@bp.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None

        # Logica para buscar
        c.execute("SELECT * FROM usuarios WHERE usuario = %s", (username,)) # Al ser tupla se pone ,
        user = c.fetchone()

        print(user)

        if user is None:
            error = "El usuario y/o contraseña invalida"
        # Si no es la misma contraseña
        elif not check_password_hash(user[5], password):
            error = "El usuario y/o contraseña invalida"

        # Caso contrario si es todo valido
        if error is None:
            session.clear()
            # Crear variable de ssesion
            session["id"] = user[0] # Le damos el id de usuario
            return redirect(url_for("todo.contenido"))

        flash(error)

    return render_template("index.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("id")
    # Si no lo encuentra esta sin acceso
    if user_id is None:
        g.user = None
    else:
        # Invoco DB y realizo operacion
        db, c  = get_db()
        c.execute("SELECT * FROM usuarios WHERE id= %s", (user_id,))
        g.user = c.fetchone() # Devuelve solo el primer elemento que encuentre


# Crear para proteger las rutas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


# Crea para cerrar sesion
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))