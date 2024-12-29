import subprocess
from flask import Flask, render_template, request
import wifi

app = Flask(__name__)

def get_available_networks():
    networks = wifi.Cell.all('wlan0')
    return networks

def connect_to_network(network_name, password):
    cmd = f"sudo nmcli dev wifi connect '{network_name}' password '{password}'"
    subprocess.run(cmd, shell=True)

def is_connected():
    wifi_connected = subprocess.run(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    eth_connected = subprocess.run(['ip', 'link', 'show', 'eth0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return wifi_connected.returncode == 0 or eth_connected.returncode == 0

@app.route('/', methods=['GET', 'POST'])
def home():
    if is_connected():
        return render_template('status.html', status="Connected to a network!")
    
    if request.method == 'POST':
        network_name = request.form['network']
        password = request.form['password']
        connect_to_network(network_name, password)
        return render_template('status.html', status=f"Connecting to {network_name}...")

    networks = get_available_networks()
    return render_template('index.html', networks=networks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)