# ZEUS
## RPi3 With Plex Media Server & Transmission Server

---

### 1. Get latest minibian & Flash it

 * Minibian : https://minibianpi.wordpress.com
 * Win32DiskImager : http://sourceforge.net/projects/win32diskimager/files/latest/download

---

### 2. Raspberry Pi first run

 * http://www.htpcguides.com/lightweight-raspbian-distro-minibian-initial-setup/
 
```
username: root
password: raspberry
```

 **1) Change your root password**
```
passwd
```
 **2) Install some basics**
```
apt-get update
apt-get install nano sudo rpi-update raspi-config usbutils dosfstools -y
apt-get remove initramfs-tools -y
``` 
 **3) Expand SD Filesystem**
```
raspi-config
 => 1 Expand Filesystem
 => OK
 => Finish
 => Reboot
 
```
 **4) Overclock** *(currently unavailable RPi3)*
```
raspi-config
 => 7 Overclock
 => warning, just press Enter
 => choose wisely !
 => OK
 => Finish
 => Reboot
```
 **5) Update Raspberry Pi Firmware**
```
rpi-update
 => Reboot
apt-get upgrade -y
apt-get dist-upgrade -y
 => Reboot
```
 **6) Change local time**
```
dpkg-reconfigure tzdata
```
 **7) Create a user**
 
  Replace `{user}` by the username
```
adduser {user}
usermod -a -G sudo {user}
 => Reboot
 => Log In as {user}
```
---