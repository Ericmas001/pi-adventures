### References

 * [SETTING WIFI UP VIA THE COMMAND LINE](http://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)

### Required:

 * General: [Setup-sudoedit](https://github.com/Ericmas001/pi-adventures/blob/master/general/sudoedit.md)

***

# GETTING WIFI NETWORK DETAILS

Scan for WiFi networks

```
sudo iwlist wlan0 scan
```

`ESSID:"testing"` is the name of the WiFi network.

# ADDING THE NETWORK DETAILS TO THE RASPBERRY PI

The ESSID (ssid) for the network in this case is `testing` and the password is `testingPassword`

Open the wpa-supplicant configuration file

```
sudoedit /etc/wpa_supplicant/wpa_supplicant.conf
```

Go to the bottom of the file and add the following:

```
network={
    ssid="testing"
    psk="testingPassword"
}
```

# Testing the result

Manually restart the interface 

```
sudo ifdown wlan0 
sudo ifup wlan0
```
You can verify if it has successfully connected using `ifconfig wlan0`. If the *inet addr* field has an address beside it, the Pi has connected to the network. If not, check your password and ESSID are correct.
