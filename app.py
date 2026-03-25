from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Base de datos simulada
capitulos = {
    1: {"nombre": "Capítulo 1: El Mandalorian", "estado": "disponible", "expira": None},
    2: {"nombre": "Capítulo 2: El Niño", "estado": "disponible", "expira": None},
    3: {"nombre": "Capítulo 3: El Pecado", "estado": "disponible", "expira": None},
}

def actualizar_estados():
    """Limpia reservas o alquileres expirados"""
    ahora = datetime.now()
    for cap_id, data in capitulos.items():
        if data["expira"] and ahora > data["expira"]:
            data["estado"] = "disponible"
            data["expira"] = None

@app.route('/')
def index():
    actualizar_estados()
    return render_template('index.html', capitulos=capitulos)

@app.route('/alquilar/<int:cap_id>', methods=['POST'])
def alquilar(cap_id):
    actualizar_estados()
    if capitulos[cap_id]["estado"] == "disponible":
        capitulos[cap_id]["estado"] = "reservado"
        # Reservado por 4 minutos
        capitulos[cap_id]["expira"] = datetime.now() + timedelta(minutes=4)
        return jsonify({"msg": "Reservado por 4 min"}), 200
    return jsonify({"msg": "No disponible"}), 400

@app.route('/confirmar', methods=['POST'])
def confirmar():
    data = request.json
    cap_id = int(data.get('id'))
    precio = data.get('precio')
    
    if cap_id in capitulos and capitulos[cap_id]["estado"] == "reservado":
        capitulos[cap_id]["estado"] = "alquilado"
        # Alquilado por 24 horas
        capitulos[cap_id]["expira"] = datetime.now() + timedelta(hours=24)
        return jsonify({"msg": f"Pago de ${precio} confirmado. Alquilado por 24hs"}), 200
    return jsonify({"msg": "Error en confirmación"}), 400

if __name__ == '__main__':
    app.run(debug=True)