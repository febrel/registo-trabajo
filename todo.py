
from werkzeug.exceptions import abort # Cuando intente hacer un registro que no le pertenece
from db import get_db
from auth import login_required
from flask import (Blueprint, flash, g, render_template, request, url_for, session, redirect)

# Todas las funciones con todas las rutas esta va ser la ruta /todo

bp = Blueprint('todo', __name__)

@bp.route('/contenido')
@login_required
def contenido():
    # Buscar a base datos, todos los todo que el ha realizado
    db, c = get_db()
    # Es muy importante el orden para el index

    c.execute("SELECT r.day, r.time, u.usuario, r.ubicacion FROM usuarios u, registros r WHERE r.id_usuarios = r.id AND u.usuario =%s",(g.user[4],))
    todos = c.fetchall()

    print(todos)

    return render_template("registros.html", todos= todos)

# # Para crear todo
# @bp.route('/create', methods=['GET','POST'])
# @login_required
# def create():
#     if request.method == "POST":
#         description = request.form["description"]
#         error = None

#         if not description:
#             error = "Descripcion es requerida"

#         if error is not None:
#             flash(error)
#         else:

#             db, c = get_db()
#             c.execute('INSERT INTO todo (descripcion, complete, created_by ) VALUES (%s, %s, %s)' , (description, False, g.user[0]))

#             db.commit()
#             return redirect(url_for("todo.index"))
#     return render_template("todo/create.html")


# def get_todo(id):
#     db, c = get_db()
#     c.execute(" SELECT t.id_todo, t.descripcion, t.complete, t.created_by, t.created_at, u.username FROM todo t JOIN user u ON t.created_by = u.id WHERE t.id_todo= %s ", (id,))
#     todo = c.fetchone()

#     # Condicion si no encuentra nada
#     if todo is None:
#         abort(404, "El todo del id {0} no existe ".format(id))
#     return todo


# # Para modificar todo
# @bp.route('/<int:id>/update', methods=["GET","POST"])
# @login_required
# def update(id):
#     todo = get_todo(id)

#     if request.method == "POST":
#         descripcion = request.form["descripcion"]
#         # Para los checkbox
#         complete = True if request.form.get("completed") == "on" else False
#         error = None

#         # Validaciones
#         if not descripcion:
#             error = "La descripcion es requerida"
#         if error is not  None:
#             flash(error)

#         # Si no existe ningun error vamos actualizar
#         else:
#             db, c = get_db()
#             c.execute("UPDATE todo SET descripcion = %s, complete = %s WHERE id_todo = %s AND created_by=%s", (descripcion, complete, id, g.user[0]))
#             db.commit()
#             return redirect(url_for("todo.index"))

#     return render_template("todo/update.html", todo=todo)

# # Para modificar todo
# @bp.route('/<int:id>/delete', methods=["POST"])
# @login_required
# def delete(id):
#     db, c = get_db()
#     c.execute("DELETE FROM todo WHERE id_todo = %s", (str(id),))
#     db.commit()
#     return redirect(url_for('todo.index'))
