from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Base de datos simulada
capitulos = {
    1: {"nombre": "Temporada 1 (2019) - Capítulo 1: El mandaloriano (The Mandalorian)", "estado": "disponible", "expira": None},
    2: {"nombre": "Temporada 1 (2019) - Capítulo 2: El niño (The Child)", "estado": "disponible", "expira": None},
    3: {"nombre": "Temporada 1 (2019) - Capítulo 3: El pecado (The Sin)", "estado": "disponible", "expira": None},
    4: {"nombre": "Temporada 1 (2019) - Capítulo 4: Santuario (Sanctuary)", "estado": "disponible", "expira": None},
    5: {"nombre": "Temporada 1 (2019) - Capítulo 5: El pistolero (The Gunslinger)", "estado": "disponible", "expira": None},
    6: {"nombre": "Temporada 1 (2019) - Capítulo 6: El prisionero (The Prisoner)", "estado": "disponible", "expira": None},
    7: {"nombre": "Temporada 1 (2019) - Capítulo 7: El ajuste de cuentas (The Reckoning)", "estado": "disponible", "expira": None},
    8: {"nombre": "Temporada 1 (2019) - Capítulo 8: Redención (Redemption)", "estado": "disponible", "expira": None},
    9: {"nombre": "Temporada 2 (2020) - Capítulo 9: El mariscal (The Marshal)", "estado": "disponible", "expira": None},
    10: {"nombre": "Temporada 2 (2020) - Capítulo 10: La pasajera (The Passenger)", "estado": "disponible", "expira": None},
    11: {"nombre": "Temporada 2 (2020) - Capítulo 11: La heredera (The Heiress)", "estado": "disponible", "expira": None},
    12: {"nombre": "Temporada 2 (2020) - Capítulo 12: El asedio (The Siege)", "estado": "disponible", "expira": None},
    13: {"nombre": "Temporada 2 (2020) - Capítulo 13: La Jedi (The Jedi)", "estado": "disponible", "expira": None},
    14: {"nombre": "Temporada 2 (2020) - Capítulo 14: La tragedia (The Tragedy)", "estado": "disponible", "expira": None},
    15: {"nombre": "Temporada 2 (2020) - Capítulo 15: El creyente (The Believer)", "estado": "disponible", "expira": None},
    16: {"nombre": "Temporada 2 (2020) - Capítulo 16: El rescate (The Rescue)", "estado": "disponible", "expira": None},
    17: {"nombre": "Temporada 3 (2023) - Capítulo 17: El apóstata (The Apostate)", "estado": "disponible", "expira": None},
    18: {"nombre": "Temporada 3 (2023) - Capítulo 18: Las minas de Mandalore (The Mines of Mandalore)", "estado": "disponible", "expira": None},
    19: {"nombre": "Temporada 3 (2023) - Capítulo 19: El converso (The Convert)", "estado": "disponible", "expira": None},
    20: {"nombre": "Temporada 3 (2023) - Capítulo 20: El huérfano (The Foundling)", "estado": "disponible", "expira": None},
    21: {"nombre": "Temporada 3 (2023) - Capítulo 21: El pirata (The Pirate)", "estado": "disponible", "expira": None},
    22: {"nombre": "Temporada 3 (2023) - Capítulo 22: Pistoleros a sueldo (Guns for Hire)", "estado": "disponible", "expira": None},
    23: {"nombre": "Temporada 3 (2023) - Capítulo 23: Los espías (The Spies)", "estado": "disponible", "expira": None},
    24: {"nombre": "Temporada 3 (2023) - Capítulo 24: El regreso (The Return)", "estado": "disponible", "expira": None},
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