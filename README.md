# WiFi Setup Portal for Raspberry Pi

This is a simple web-based interface that allows you to connect your Raspberry Pi to a Wi-Fi network. It checks if the Pi is connected to a network and if not, shows a portal to select a Wi-Fi network and enter the password.

## Prerequisites

Make sure you have the following installed on your Raspberry Pi:

- Python 3
- `pip3` (Python package manager)

## Installation

1. Install required dependencies:

```bash
sudo apt update
sudo apt install python3-pip python3-dev wireless-tools
```

2. Install Python libraries:

```sudo pip3 install flask wifi```

## Running the Application

1. Clone or download the repository to your Raspberry Pi.

2. Navigate to the project folder and run the application:

`sudo python3 app.py`

The web portal will be available at http://<your-pi-ip>:80

## Setting up Autostart using systemd
To ensure the application starts automatically on boot using systemd, follow these steps:

1. Create a new systemd service file:
`sudo nano /etc/systemd/system/wifi-setup.service`

2. Add the following content to the file:

```[Unit]
Description=WiFi Setup Portal
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/project/app.py
WorkingDirectory=/path/to/your/project
User=change-to-yours
Group=pi
Restart=always

[Install]
WantedBy=multi-user.target```

Make sure to replace /path/to/your/project/ with the actual path to your project directory.

3. Enable and start the service:
```sudo systemctl daemon-reload
sudo systemctl enable wifi-setup.service
sudo systemctl start wifi-setup.service```
4. Check the status of the service:
`sudo systemctl status wifi-setup.service`

Your application will now automatically start on boot and be available on port 80.

## Notes
The portal will be available on port 80, and you can access it via any device connected to the Raspberry Pi's network.
If the Pi is already connected to a network, it will display a "Connected" message.
