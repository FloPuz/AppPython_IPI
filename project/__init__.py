import sqlite3

import click
from flask import current_app, g


# db logic code
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("data.db")
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
    with app.app_context():
        with current_app.open_resource("cheesse.sql") as f:
            print("ok")
            db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def create_app():
    init_app(app)
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        user = cursor.execute("""SELECT * from user""").fetchone()
        print(user["login"])
    return app
