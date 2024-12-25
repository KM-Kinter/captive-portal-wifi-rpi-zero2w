import os
import subprocess
import tempfile

def setup_ap(ssid, password, interface="wlan0"):
    subprocess.run(['sudo', 'ifconfig', interface, 'down'], check=True)
    subprocess.run(['sudo', 'ifconfig', interface, '192.168.100.1', 'netmask', '255.255.255.0'], check=True)
    subprocess.run(['sudo', 'ifconfig', interface, 'up'], check=True)

    hostapd_config = f"""
    interface={interface}
    driver=nl80211
    ssid={ssid}
    hw_mode=g
    channel=7
    wmm_enabled=1
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase={password}
    wpa_key_mgmt=WPA-PSK
    rsn_pairwise=CCMP
    """
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as hostapd_conf:
        hostapd_conf.write(hostapd_config)
        hostapd_conf_path = hostapd_conf.name

    dnsmasq_config = f"""
    interface={interface}
    dhcp-range=192.168.100.50,192.168.100.150,255.255.255.0,24h
    """
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as dnsmasq_conf:
        dnsmasq_conf.write(dnsmasq_config)
        dnsmasq_conf_path = dnsmasq_conf.name

    subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=1'], check=True)
    subprocess.run(['sudo', 'iptables', '--table', 'nat', '-A', 'POSTROUTING', '-o', 'eth0', '-j', 'MASQUERADE'], check=True)
    subprocess.run(['sudo', 'iptables', '-A', 'FORWARD', '-i', interface, '-o', 'eth0', '-j', 'ACCEPT'], check=True)
    subprocess.run(['sudo', 'iptables', '-A', 'FORWARD', '-i', 'eth0', '-o', interface, '-m', 'state', '--state', 'ESTABLISHED,RELATED', '-j', 'ACCEPT'], check=True)

    hostapd_process = subprocess.Popen(['sudo', 'hostapd', hostapd_conf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dnsmasq_process = subprocess.Popen(['sudo', 'dnsmasq', '-C', dnsmasq_conf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(f"Access Point running: SSID={ssid}, Password={password}")
    return hostapd_process, dnsmasq_process

if __name__ == "__main__":
    ssid = "MyRaspberryPiAP"
    password = "MySecurePassword"
    setup_ap(ssid, password)
