### References

 * [RPi Setting up a static IP in Debian](http://elinux.org/RPi_Setting_up_a_static_IP_in_Debian)

### Required:

 * General: [Setup-sudoedit](https://github.com/Ericmas001/pi-adventures/blob/master/general/sudoedit.md)

***

# Finding the interface

To find the interface you want to change from "dhcp" to "static", run the `ifconfig` command. You should get something like this:

```
eth0      Link encap:Ethernet  HWaddr b8:27:eb:6c:b1:71
          inet addr:192.168.1.103  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1636861 errors:0 dropped:81 overruns:0 frame:0
          TX packets:10546395 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:240270614 (229.1 MiB)  TX bytes:2482928548 (2.3 GiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:539950 errors:0 dropped:0 overruns:0 frame:0
          TX packets:539950 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:109867069 (104.7 MiB)  TX bytes:109867069 (104.7 MiB)

```

In this case, the interesting one is `eth0`.

# Change from DHCP to Static IP

Open the `interfaces` file

```
sudoedit /etc/network/interfaces 
```

In the interfaces file look for a line such as:

```
iface eth0 inet dhcp
```

Replace it with those lines

```
iface eth0 inet static
     address 192.168.1.74
     network 192.168.1.0
     netmask 255.255.255.0
     broadcast 192.168.1.255
     gateway 192.168.1.1
```