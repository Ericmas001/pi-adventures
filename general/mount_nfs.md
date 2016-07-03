### References:

 * [Setting up an NFS Client](http://www.tldp.org/HOWTO/NFS-HOWTO/client.html)
 * [Mounting WD My Cloud to Ubuntu 13.10 folder](http://www.blogs.digitalworlds.net/softwarenotes/?p=284)
 * [Setting up an NFS Server and Client on Debian Wheezy](https://www.howtoforge.com/install_nfs_server_and_client_on_debian_wheezy)

### Required:

 * General: [Setup-sudoedit](https://github.com/Ericmas001/pi-adventures/blob/master/general/sudoedit.md)

***

### Install nfs-common package 
`sudo apt-get install nfs-common` 

### Get avaliable folders for mounting 
`showmount -e 192.168.1.21` 

### Mounting a nfs folder to your local computer folder 
```
sudo mount -o rw,soft,intr,nfsvers=3 192.168.1.21:/media/wdmycloud/shares /shared
```

### Automatic mount

`sudoedit /etc/fstab`

```
192.168.1.21:/media/wdmycloud/shares     /shared      nfs       rw,soft,intr,rsize=8192,wsize=8192,addr=192.168.1.21      0     0
```