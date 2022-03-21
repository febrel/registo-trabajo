import mysql.connector
import click # Ejucutar comandos en terminal
from flask import current_app, g # Mantiene aplicacion que estamos ejecutando, almacenamos usuario dentro de g
from flask.cli import with_appcontext # Accedemos variables


def get_db():
    if "db" not in g:
        g.db =mysql.connector.connect(
            host = current_app.config["DATABASE_HOST"],
            user = current_app.config["DATABASE_USER"],
            password = current_app.config["DATABASE_PASSWORD"],
            database = current_app.config["DATABASE"],
        )

        g.c = g.db.cursor( )

    return g.db, g.c #Obtenemos base datos, cursor

def close_db(e = None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db() # Trae y almacena en las variables del metodo de DB

    # Para ejecutar todas las intrucciones
    for i in instructions:
        c.execute(i)

def init_db_command():
    init_db()
    click.echo("Basa datos inicializada")

# Le pasamos app
def init_app(app):
    app.teardown_appcontext(close_db)