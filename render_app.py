from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Stockage local des PC (sera mis à jour par le Raspberry Pi)
connected_pcs = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pcs')
def get_pcs():
    """Renvoie les PC connectés"""
    # Simuler la récupération depuis le Raspberry Pi
    return jsonify({
        "pcs": connected_pcs,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "render"
    })

@app.route('/api/update-pc', methods=['POST'])
def update_pc():
    """Reçoit les mises à jour des PC depuis le Raspberry Pi"""
    global connected_pcs
    
    data = request.json
    if 'pcs' in data:
        connected_pcs = data['pcs']
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Données invalides"})

@app.route('/api/connect/<pc_id>')
def connect_pc(pc_id):
    """Connecte à un PC spécifique"""
    # Cela redirigera vers le Raspberry Pi ou le PC
    if pc_id in connected_pcs:
        return jsonify({
            "status": "success",
            "message": f"Connexion préparée vers {connected_pcs[pc_id]['name']}",
            "ip": connected_pcs[pc_id]['ip']
        })
    else:
        return jsonify({"status": "error", "message": "PC non trouvé"})

if __name__ == '__main__':
    app.run(debug=True)
