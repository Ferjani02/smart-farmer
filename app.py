from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import threading
import time

ZONES = ["zone_1", "zone_2", "zone_3", "zone_4"]
WATER_USAGE = {zone: 0 for zone in ZONES}
MODES = {zone: "ia" for zone in ZONES}
REMAINING_TIME = {zone: 0 for zone in ZONES}
OLIVE_AGES = {zone: 5 for zone in ZONES}

app = Flask(__name__)
CORS(app)

SENSOR_DATA = {zone: {"temperature": 25, "humidite": 50, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for zone in ZONES}

def simulate_sensor_data(zone):
    return {
        "temperature": round(random.uniform(20, 35), 1),
        "humidite": round(random.uniform(40, 80), 1),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def update_sensor_data():
    while True:
        for zone in ZONES:
            SENSOR_DATA[zone] = simulate_sensor_data(zone)
            if REMAINING_TIME[zone] > 0:
                REMAINING_TIME[zone] = max(0, REMAINING_TIME[zone] - 600)  # 10 minutes = 600 sec
        time.sleep(600)  # 600 secondes = 10 minutes

threading.Thread(target=update_sensor_data, daemon=True).start()

def get_irrigation_rule(temperature, humidite, age):
    if age <= 2: base_water = 7
    elif age <= 5: base_water = 20
    elif age <= 10: base_water = 35
    else: base_water = 50
    duree = 30 + max(0, (temperature - 25) * 2) + max(0, (50 - humidite) * 1.5)
    quantite = base_water * (1 + max(0, (temperature - 25) * 0.02) + max(0, (50 - humidite) * 0.01))
    duree = min(max(duree, 10), 120)
    quantite = min(max(quantite, 2), 100)
    return int(duree), round(quantite, 2)

@app.route('/')
def index():
    return render_template('index.html', zones=ZONES, sensor_data=SENSOR_DATA, water_usage=WATER_USAGE, remaining_time=REMAINING_TIME, modes=MODES, olive_ages=OLIVE_AGES)

@app.route('/api/irrigate/<zone>', methods=['POST'])
def api_irrigate(zone):
    if zone not in ZONES:
        return jsonify({"error": "Zone inconnue"}), 400
    data = request.json
    age = data.get('age', OLIVE_AGES.get(zone, 5))
    capteurs = SENSOR_DATA[zone]
    mode = MODES.get(zone, "ia")
    # Calcul IA de la durée et de la quantité d’eau
    duree_ia, quantite_ia = get_irrigation_rule(capteurs['temperature'], capteurs['humidite'], age)
    if mode == "ia":
        duree = duree_ia
        quantite = quantite_ia
    else:  # mode manuel
        duree = int(data.get('duree', duree_ia))
        # Adaptation de la quantité d’eau selon la durée choisie
        quantite = quantite_ia * (duree / duree_ia)
    WATER_USAGE[zone] += quantite
    REMAINING_TIME[zone] = duree * 60
    return jsonify({
        "msg": f"Irrigation de la zone {zone} lancée pour {duree} minutes",
        "duree": duree,
        "quantite_eau": quantite,
        "quantite_ia": quantite_ia,
        "duree_ia": duree_ia,
        "total_eau_zone": WATER_USAGE[zone],
        "temps_restant_sec": REMAINING_TIME[zone]
    })

@app.route('/api/set_mode/<zone>', methods=['POST'])
def api_set_mode(zone):
    new_mode = request.json.get('mode')
    if new_mode in ["ia", "manuel"]:
        MODES[zone] = new_mode
        return jsonify({"msg": f"Mode de la zone {zone} changé en {new_mode}"})
    else:
        return jsonify({"error": "Mode inconnu"}), 400

@app.route('/api/set_age/<zone>', methods=['POST'])
def api_set_age(zone):
    new_age = int(request.json.get('age', 5))
    OLIVE_AGES[zone] = new_age
    return jsonify({"msg": f"Âge de la zone {zone} mis à jour à {new_age} ans"})

@app.route('/api/sensor_data')
def api_sensor_data():
    return jsonify(SENSOR_DATA)

@app.route('/api/water_usage')
def api_water_usage():
    return jsonify({"water_usage": WATER_USAGE, "remaining_time": REMAINING_TIME})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
