
from flask import Flask, render_template, request, jsonify
from utils import calcular_ruta_y_restricciones

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json()
    origen = data["origen"]
    destino = data["destino"]
    restricciones = data["restricciones"]
    vehiculo = data["vehiculo"]

    ruta_geojson, restricciones_calculadas = calcular_ruta_y_restricciones(
        origen, destino, restricciones, vehiculo
    )

    return jsonify({
        "route": ruta_geojson,
        "restricciones": restricciones_calculadas
    })

if __name__ == "__main__":
    app.run(debug=True)
