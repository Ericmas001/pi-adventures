### References

 * [Change hostname or Server name of a Linux Machine](http://www.debianadmin.com/change-hostname-or-server-name-of-a-linux-machine.html)

### Required:

 * General: [Setup-sudoedit](https://github.com/Ericmas001/pi-adventures/blob/master/general/sudoedit.md)

***

Debian based systems use the file `/etc/hostname` to read the hostname of the system at boot time and set it up using the init script `/etc/init.d/hostname.sh`

So on a Debian based system we can edit the file `/etc/hostname` and change the name of the system and then run `/etc/init.d/hostname.sh start` to make the change active. The hostname saved in this file (`/etc/hostname`) will be preserved on system reboot (and will be set using the same script we used hostname.sh).
