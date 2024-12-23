import subprocess

def setup_ap():
    subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'])
    subprocess.run(['sudo', 'iwconfig', 'wlan0', 'mode', 'master'])
    subprocess.run(['sudo', 'iwconfig', 'wlan0', 'essid', 'MyRaspberryPiAP'])
    subprocess.run(['sudo', 'ifconfig', 'wlan0', '192.168.100.1'])
    subprocess.run(['sudo', 'dnsmasq', '--interface=wlan0', '--dhcp-range=192.168.100.50,192.168.100.150,255.255.255.0,24h'])
    subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=1'])
    subprocess.run(['sudo', 'iptables', '--table', 'nat', '-A', 'POSTROUTING', '-o', 'eth0', '-j', 'MASQUERADE'])
    subprocess.run(['sudo', 'service', 'iptables', 'save'])
    subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'])
    print("AP started succesfully")

setup_ap()