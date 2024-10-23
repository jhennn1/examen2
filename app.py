from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clavesecreta" 


@app.route("/")
def index():
    productos = session.get("productos", [])
    return render_template("listado.html", productos=productos)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form.get("cantidad") )
        precio= float(request.form.get("precio") )
        fecha = request.form["fecha"]
        categoria= request.form["categoria"]

        # Obtener lista de productos seleccionados
        gestionar = request.form.getlist("gestionar[]")

        productos = session.get("productos", [])
        productos.append({
            "nombre": nombre,
            "cantidad": cantidad,
            "precio":precio,
            "fecha": fecha,
            "categoria":categoria,

            # Unir la lista de los productos en una cadena
            "gestionar": "; ".join(gestionar)
        })
        session["productos"] = productos
        return redirect(url_for("index"))
    return render_template("registro.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    productos = session.get("productos", [])
    if id < 0 or id >= len(productos):
        return redirect(url_for("index"))

    if request.method == "POST":
        productos[id]["nombre"] = request.form["nombre"]
        productos[id]["cantidad"] = request.form["cantidad"]
        productos[id]["precio"] = request.form["precio"]
        productos[id]["fecha"] = request.form["fecha"]
        productos[id]["categoria"] = request.form["categoria"]
        productos[id]["gestionar"] = "; ".join(
            request.form.getlist("gestionar[]"))
        session["productos"] = productos
        return redirect(url_for("index"))

    productos = productos[id]


    # Pasar el contacto a la plantilla
    return render_template("editar.html", contacto=productos, id=id)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    productos = session.get("productos", [])
    if id < 0 or id >= len(productos):
        return redirect(url_for("index"))
    del productos[id]
    session["productos"] = productos
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)