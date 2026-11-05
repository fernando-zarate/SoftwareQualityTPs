import json
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / "usuarios.json"


def cargar_usuarios():
    try:
        with USERS_FILE.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (OSError, json.JSONDecodeError):
        return []


def guardar_usuarios(usuarios):
    with USERS_FILE.open("w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    usuarios = cargar_usuarios()
    return render_template("index.html", total_inscriptos=len(usuarios))


@app.route("/inscripcion", methods=["POST"])
def inscripcion():
    usuarios = cargar_usuarios()

    nuevo_usuario = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "dni": request.form["dni"].strip(),
        "legajo": request.form["legajo"].strip(),
        "email": request.form["email"].strip(),
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)


    return render_template(
        "index.html",
        mensaje="¡Inscripción realizada correctamente!",
        total_inscriptos=len(usuarios),
    )


if __name__ == "__main__":
    app.run(debug=True)
