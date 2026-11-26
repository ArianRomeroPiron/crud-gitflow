from flask import Flask, render_template, request, redirect, url_for
from db import get_conn, init_db

app = Flask(__name__)


@app.route("/")
def index():
    with get_conn() as conn:
        tareas = conn.execute("SELECT * FROM tareas ORDER BY id DESC").fetchall()
    return render_template("index.html", tareas=tareas)


@app.route("/crear", methods=["POST"])
def crear():
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)",
            (request.form["titulo"], request.form.get("descripcion", "")),
        )
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
