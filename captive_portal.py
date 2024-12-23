from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

def scan_wifi():
    result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE)
    networks = result.stdout.decode().split('Cell')
    networks_info = []

    for network in networks[1:]:
        essid_start = network.find('ESSID:"') + len('ESSID:"')
        essid_end = network.find('"', essid_start)
        if essid_start != -1 and essid_end != -1:
            ssid = network[essid_start:essid_end]
            networks_info.append(ssid)
    
    return networks_info

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = self.get_wifi_page()
            self.wfile.write(html_content.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()

        ssid = post_data.split("ssid=")[1].split("&")[0]
        password = post_data.split("password=")[1]

        self.connect_to_wifi(ssid, password)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Conncting...</h1></body></html>")

    def get_wifi_page(self):
        networks = scan_wifi()
        wifi_options = "".join([f"<option value='{network}'>{network}</option>" for network in networks])
        return f"""
            <html>
                <head><title>Wi-Fi Setup</title></head>
                <body>
                    <h1>WiFi config</h1>
                    <form action="/connect" method="post">
                        <label for="ssid">Choose network:</label>
                        <select name="ssid" id="ssid">
                            {wifi_options}
                        </select><br><br>

                        <label for="password">Passkey:</label>
                        <input type="password" id="password" name="password" required><br><br>

                        <input type="submit" value="Connect">
                    </form>
                </body>
            </html>
        """

    def connect_to_wifi(self, ssid, password):
        wpa_config_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
        with open(wpa_config_path, 'a') as f:
            f.write(f'\nnetwork={{\n    ssid="{ssid}"\n    psk="{password}"\n}}\n')
        
        subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
        print(f'Connecting to {ssid}...')

def run_server():
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Listening...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
