from flask import Flask, render_template, jsonify
import subprocess
import socket
import psutil
import platform
import requests
import time
from datetime import datetime
import threading

app = Flask(__name__)

# Liste des PC connectés (synchronisée avec Render)
connected_pcs = {}
render_url = "https://ton-application-render.com/api/update-pc"  # Remplacer par ton URL Render

def get_local_ip():
    """Récupère l'IP locale du Raspberry Pi"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def scan_local_network():
    """Scan le réseau local pour trouver les PC"""
    global connected_pcs
    
    try:
        # Utiliser nmap pour scanner le réseau (si installé)
        # Alternative : simple ping des IPs
        local_ip = get_local_ip()
        base_ip = ".".join(local_ip.split('.')[:-1]) + "."
        
        pcs_found = {}
        
        # Scanner les IP de 1 à 254
        for i in range(1, 255):
            ip = f"{base_ip}{i}"
            try:
                # Test simple avec ping (plus rapide)
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL)
                if result.returncode == 0:
                    pcs_found[f"pc_{i}"] = {
                        "name": f"PC-{i}",
                        "ip": ip,
                        "status": "connected",
                        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "platform": platform.system(),
                        "type": "detected"
                    }
            except Exception:
                continue
        
        # Ajouter le Raspberry Pi lui-même
        pcs_found["raspberry_pi"] = {
            "name": "Raspberry-Pi",
            "ip": local_ip,
            "status": "connected",
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "platform": platform.system(),
            "type": "server"
        }
        
        connected_pcs = pcs_found
        
    except Exception as e:
        print(f"Erreur lors du scan réseau : {e}")

def sync_with_render():
    """Envoie les PC détectés à Render"""
    global connected_pcs
    
    try:
        data = {
            "pcs": connected_pcs,
            "timestamp": datetime.now().isoformat(),
            "server_ip": get_local_ip()
        }
        
        # Envoi aux serveurs Render
        response = requests.post(f"{render_url}/sync", json=data, timeout=10)
        print(f"Sync status: {response.status_code}")
        
    except Exception as e:
        print(f"Erreur de synchronisation avec Render: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pcs')
def get_pcs():
    scan_local_network()
    return jsonify({
        "pcs": connected_pcs,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "server_ip": get_local_ip()
    })

@app.route('/api/connect/<pc_id>')
def connect_pc(pc_id):
    """Fonction pour se connecter à un PC"""
    if pc_id in connected_pcs:
        pc_info = connected_pcs[pc_id]
        return jsonify({
            "status": "success",
            "message": f"Connexion préparée vers {pc_info['name']}",
            "ip": pc_info['ip'],
            "port": 5900  # Port VNC par défaut
        })
    else:
        return jsonify({
            "status": "error",
            "message": "PC non trouvé"
        })

if __name__ == '__main__':
    # Démarrer le scan régulier en arrière-plan
    def periodic_scan():
        while True:
            scan_local_network()
            sync_with_render()
            time.sleep(30)  # Scanner toutes les 30 secondes
    
    # Lancer le scan périodique dans un thread séparé
    scanner_thread = threading.Thread(target=periodic_scan, daemon=True)
    scanner_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
