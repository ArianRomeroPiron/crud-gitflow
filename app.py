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


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    with get_conn() as conn:
        if request.method == "POST":
            conn.execute(
                "UPDATE tareas SET titulo=?, descripcion=?, completada=? WHERE id=?",
                (request.form["titulo"], request.form.get("descripcion", ""),
                 1 if request.form.get("completada") else 0, id),
            )
            return redirect(url_for("index"))
        t = conn.execute("SELECT * FROM tareas WHERE id=?", (id,)).fetchone()
    return render_template("editar.html", t=t)


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    with get_conn() as conn:
        conn.execute("DELETE FROM tareas WHERE id=?", (id,))
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
