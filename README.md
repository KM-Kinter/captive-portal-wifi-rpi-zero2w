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

## Set up autostart

To make the application run on startup:

1. Open the crontab configuration:

`crontab -e`

2. Add the following line to the end of the file:

`@reboot /usr/bin/python3 /path/to/your/project/wifi_checkup.py &`

Replace /path/to/your/project/ with the actual path to your project.

Save and exit (Ctrl+X, then press Y and Enter).
Now, your Raspberry Pi will start the Wi-Fi setup portal automatically every time it boots up.

## Notes
The portal will be available on port 80, and you can access it via any device connected to the Raspberry Pi's network.
If the Pi is already connected to a network, it will display a "Connected" message.