import time
import os
import subprocess
from flask import Flask, render_template_string
import wifi

app = Flask(__name__)

def check_internet():
    try:
        subprocess.check_call(['ping', '-c', '1', 'google.com'])
        return True
    except subprocess.CalledProcessError:
        return False

def get_available_networks():
    networks = wifi.Cell.all('wlan0')
    return networks

@app.route('/')
def index():
    # if check_internet():
    #     return "Jesteś połączony z internetem!", 200
    # else:
        networks = get_available_networks()
        return render_template_string("""
            <html>
            <head><title>Wybierz sieć Wi-Fi</title></head>
            <body>
                <h1>Brak połączenia z internetem</h1>
                <p>Wybierz jedną z dostępnych sieci Wi-Fi:</p>
                <ul>
                    {% for network in networks %}
                        <li>{{ network.ssid }}</li>
                    {% endfor %}
                </ul>
            </body>
            </html>
        """, networks=networks)

def start_flask_server():
    # Uruchomienie serwera na porcie 80
    app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    start_flask_server()