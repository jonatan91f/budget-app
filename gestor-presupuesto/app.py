from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"ingresos": [], "gastos": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    data = load_data()
    total_ingresos = sum(item["cantidad"] for item in data["ingresos"])
    total_gastos = sum(item["cantidad"] for item in data["gastos"])
    balance = total_ingresos - total_gastos
    return render_template("index.html", ingresos=data["ingresos"], gastos=data["gastos"], total_ingresos=total_ingresos, total_gastos=total_gastos, balance=balance)

@app.route("/agregar", methods=["POST"])
def agregar():
    tipo = request.form.get("tipo")
    descripcion = request.form.get("descripcion")
    cantidad = float(request.form.get("cantidad"))

    data = load_data()
    data[tipo].append({"descripcion": descripcion, "cantidad": cantidad})
    save_data(data)
    flash("Registro agregado correctamente")
    return redirect(url_for("index"))

@app.route("/eliminar/<tipo>/<int:index>")
def eliminar(tipo, index):
    data = load_data()
    if 0 <= index < len(data[tipo]):
        data[tipo].pop(index)
        save_data(data)
        flash("Registro eliminado")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
