# Minibian Initial Setup
## RPi2 & RPi3 with minibian jessie

---

### 1. Get latest minibian & Flash it

 * Minibian : https://minibianpi.wordpress.com
 * Win32DiskImager : http://sourceforge.net/projects/win32diskimager/files/latest/download

---

### 2. Initial part with screen and keyboard

 * http://www.htpcguides.com/lightweight-raspbian-distro-minibian-initial-setup/
 * https://github.com/Ericmas001/debian-helper/wiki/%5BSnippet%5D-Setup-sudoedit
 * https://github.com/Ericmas001/debian-helper/wiki/%5BSnippet%5D-Change-from-DHCP-to-Static-IP
 
```
username: root
password: raspberry
```

 **1) Change your root password**
```
 > passwd
```
 **2) Install some basics**
```
 > apt-get update
 > apt-get install nano sudo rpi-update raspi-config usbutils dosfstools -y
 > apt-get remove initramfs-tools -y
``` 
 **3) Expand SD Filesystem**
```
 > raspi-config
 ==> 1 Expand Filesystem
 ==> OK
 ==> Finish
 ==> Reboot
 
```
 **4) Overclock** *(currently unavailable on RPi3)*
```
 > raspi-config
 ==> 7 Overclock
 ==> warning, just press Enter
 ==> choose wisely !
 ==> OK
 ==> Finish
 ==> Reboot
```
 **5) Update Raspberry Pi Firmware**
```
 > rpi-update
 ==> Reboot
 > apt-get upgrade -y
 > apt-get dist-upgrade -y
 ==> Reboot
```
 **6) Change local time**
```
dpkg-reconfigure tzdata
```
 **7) Create a user**
 
  Replace `{user}` by the username
```
 > adduser {user}
 > usermod -a -G sudo {user}
 ==> Reboot
 ==> Log In as {user}
```
 **8) Setup sudoedit**
 
  us keyboard: [ALT Gr] + [¸] = ~. (rightmost on qwerty row)
```
 > nano ~/.bashrc
```
```
EDITOR=/bin/nano
```
 **9) Change from DHCP to Static IP**
 
  Replace `{NetworkId}` by something between [1-254]
  Replace `{RpiId}` by something between [1-254]
  
```
 > sudoedit /etc/network/interfaces 
```
```
iface eth0 inet static
     address 192.168.{NetworkId}.{RpiId}
     network 192.168.{NetworkId}.0
     netmask 255.255.255.0
     broadcast 192.168.{NetworkId}.255
     gateway 192.168.{NetworkId}.1
```
 **10) Change hostname**
 
  Replace `{Hostname}` by something that contains only the ASCII letters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9', and the hyphen ('-'). It cannot start with a digit or with a hyphen, and must not end with a hyphen.
```
 > sudo raspi-config
 ==> Option 9: Advanced Options
 ==> Option A2: Hostname
 ==> {Hostname}
```
---