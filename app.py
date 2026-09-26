from flask import Flask, render_template, request, jsonify
import subprocess
import socket
import psutil
import platform
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Stockage des PC connectés
connected_pcs = {}

def get_local_ip():
    """Récupère l'adresse IP locale"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def scan_network():
    """Scan le réseau local pour trouver les PC"""
    global connected_pcs
    
    # Simuler un scan réseau (dans l'application réelle, tu devrais utiliser nmap)
    try:
        # Ici tu peux implémenter une vraie détection de réseau
        # Pour le moment, on simule avec des données fictives
        connected_pcs = {
            "pc1": {
                "name": "PC-Maison",
                "ip": get_local_ip(),
                "status": "connected",
                "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "platform": platform.system()
            },
            "pc2": {
                "name": "PC-Travail",
                "ip": "192.168.1.101",
                "status": "connected",
                "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "platform": platform.system()
            }
        }
    except Exception as e:
        print(f"Erreur lors du scan réseau : {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pcs')
def get_pcs():
    """Renvoie la liste des PC connectés"""
    # Scan régulier du réseau
    scan_network()
    
    # Retourner les PC dans un format JSON
    return jsonify({
        "pcs": connected_pcs,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/connect/<pc_id>')
def connect_pc(pc_id):
    """Connecte à un PC spécifique"""
    if pc_id in connected_pcs:
        return jsonify({
            "status": "success",
            "message": f"Connexion en cours vers {connected_pcs[pc_id]['name']}",
            "ip": connected_pcs[pc_id]['ip']
        })
    else:
        return jsonify({
            "status": "error",
            "message": "PC non trouvé"
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
