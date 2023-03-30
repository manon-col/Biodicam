#!/bin/bash
# Installation script for setting a raspberry pi as hotspot without routing internet.
# Based on : https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point

# Setting hostapd
echo "Installing hostapd ..."
sudo apt install hostapd
sudo systemctl unmask hostapd
sudo systemctl enable hostapd

echo "Installing dnsmask ..."
sudo apt install dnsmasq

echo "Setting up dhcpd configuration file ..."
sudo sh -c 'echo "interface wlan0" >> /etc/dhcpcd.conf'
sudo sh -c 'echo "    static ip_address=192.168.4.1/24" >> /etc/dhcpcd.conf'
sudo sh -c 'echo "    nohook wpa_supplicant" >> /etc/dhcpcd.conf'

echo "Setting up dnsmask configuration file ..."
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo sh -c 'echo "interface=wlan0 # Listening interface" >> /etc/dnsmasq.conf'
sudo sh -c 'echo "dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h" >> /etc/dnsmasq.conf'
sudo sh -c 'echo "domain=wlan     # Local wireless DNS domain" >> /etc/dnsmasq.conf'
sudo sh -c 'echo "address=/gw.wlan/192.168.4.1" >> /etc/dnsmasq.conf'

sudo rfkill unblock wlan

echo "Setting up hostapd configuration file ..."
sudo sh -c 'echo "country_code=FR" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "interface=wlan0" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "ssid=Econect" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "hw_mode=g" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "channel=7" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "macaddr_acl=0" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "auth_algs=1" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "ignore_broadcast_ssid=0" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "wpa=2" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "wpa_passphrase=biodicam" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "wpa_key_mgmt=WPA-PSK" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "wpa_pairwise=TKIP" >> /etc/hostapd/hostapd.conf'
sudo sh -c 'echo "rsn_pairwise=CCMP" >> /etc/hostapd/hostapd.conf'

echo "Please add '@reboot sleep 15 && sudo systemctl restart dhcpcd' to the crontab before rebooting the pi (edit it with 'crontab -e' and choose nano as editor)" 



