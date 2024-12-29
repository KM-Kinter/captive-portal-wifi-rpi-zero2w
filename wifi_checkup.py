from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)

def is_connected():
    wlan0_ip = subprocess.getoutput("ip addr show wlan0 | grep inet")
    eth0_ip = subprocess.getoutput("ip addr show eth0 | grep inet")
    
    if wlan0_ip or eth0_ip:
        return True
    else:
        return False

def connect_to_wifi(ssid, password):
    config = f"""
    network={{
        ssid="{ssid}"
        psk="{password}"
    }}
    """
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as file:
        file.write(config)
    
    subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "reconnect"])

@app.route('/', methods=['GET', 'POST'])
def index():
    if is_connected():
        return render_template('status.html', status="Connected to a network!")
    else:
        if request.method == 'POST':
            ssid = request.form['ssid']
            password = request.form['password']
            if ssid and password:
                connect_to_wifi(ssid, password)
                return redirect(url_for('index'))
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)