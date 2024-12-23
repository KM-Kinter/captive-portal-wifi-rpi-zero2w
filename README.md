# Captive portal for join WiFi from RPi Zero 2W

## Before start:
run this commands to install needed libraries:

```sudo apt-get update
sudo apt-get install python3-pip
pip3 install flask wifi subprocess
```

## After start:
run `python3 setup_ap.py` to start AP from your device;
next run `python3 captive_portal.py` to start managing captive portal
