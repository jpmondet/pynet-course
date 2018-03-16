#Pynet_Netmiko-grep.md

The basic idea is to use Netmiko to dynamically pull configs from network devices and then to pattern search through these files. For example, here I use netmiko-grep to search for the string 'interface' in the running-configs of the members of the 'cisco' group.

$ netmiko-grep 'interface' cisco
pynet_rtr1.txt:interface FastEthernet0
pynet_rtr1.txt:interface FastEthernet1
pynet_rtr1.txt:interface FastEthernet2
pynet_rtr1.txt:interface FastEthernet3
pynet_rtr1.txt:interface FastEthernet4
pynet_rtr1.txt:interface Vlan1
pynet_rtr2.txt:interface FastEthernet0
pynet_rtr2.txt:interface FastEthernet1
pynet_rtr2.txt:interface FastEthernet2
pynet_rtr2.txt:interface FastEthernet3
pynet_rtr2.txt:interface FastEthernet4
pynet_rtr2.txt:interface Vlan1
pynet_rtr2.txt:interface Vlan100 




And here I search for 'span' in the 'arista' group:

$ netmiko-grep 'span' arista
arista_sw1.txt:spanning-tree mode mstp
arista_sw1.txt:   spanning-tree portfast
arista_sw2.txt:spanning-tree mode mstp
arista_sw2.txt:   spanning-tree portfast
arista_sw3.txt:spanning-tree mode mstp
arista_sw3.txt:   spanning-tree portfast
arista_sw4.txt:spanning-tree mode mstp
arista_sw4.txt:   spanning-tree portfast




By default netmiko-grep will operate on the running-config, but it also can execute arbitrary show commands using the '--cmd' argument.

$ netmiko-grep --cmd 'show arp' '10.220.88.1 ' cisco
pynet_rtr1.txt:Internet 10.220.88.1  11 001f.9e92.16fb ARPA FastEthernet4
pynet_rtr2.txt:Internet 10.220.88.1  11 001f.9e92.16fb ARPA FastEthernet4 


Here I execute 'show arp' on the 'cisco' group and search for a pattern of '10.220.88.1 ' in the 'show arp' output.


 
Specifying the device inventory
netmiko-grep uses an inventory format loosely based on Ansible's inventory (very loosely). It will look for a file named '.netmiko.yml' first in your current directory and then in your home directory.

The inventory file uses YAML and consists of two items—individual devices and groups of devices. Individual devices are created by specifying a YAML dictionary with all of the necessary Netmiko connection arguments. Groups are created by specifying a YAML list that includes previously defined devices.

Here is an example .netmiko.yml file:

---

# Dictionaries are devices
pynet_rtr1:
  device_type: cisco_ios
  ip: 10.10.10.27
  username: admin
  password: password1
  port: 22

pynet_rtr2:
  device_type: cisco_ios
  ip: 10.10.10.27
  username: admin
  password: password1
  port: 8022

# Lists are groups of devices
cisco:
  - pynet_rtr1
  - pynet_rtr2 



In the above, 'pynet_rtr1' and 'pynet_rtr2' are individual network devices; 'cisco' is a group that contains both pynet_rtr1 and pynet_rtr2. A group named 'all' is created automatically.

You can see a more detailed .netmiko.yml file here.


You can display your inventory by using the '--list-devices' argument: 

$ netmiko-grep --list-devices

Devices:
----------------------------------------
arista_sw1                  (arista_eos)
arista_sw2                  (arista_eos)
arista_sw3                  (arista_eos)
arista_sw4                  (arista_eos)
cisco_asa                    (cisco_asa)
cisco_xrv                     (cisco_xr)
hp_procurve                (hp_procurve)
juniper_srx                    (juniper)
pynet_rtr1                   (cisco_ios)
pynet_rtr2                   (cisco_ios)


Groups:
----------------------------------------
all
arista
cisco



 
What does netmiko-grep do behind the scenes?
Behind the scenes netmiko-grep will automatically create a ~/.netmiko/tmp directory.

Inside this directory it will store the 'cmd' output from the remote device. By default, 'cmd' will be 'show run' or its equivalent as determined by the SHOW_RUN_MAPPER in Netmiko's utilities.py module. In other words, Netmiko tries to automatically determine what the 'show run' equivalent is for a given platform.

netmiko-grep does not currently remove the output files from ~/.netmiko/tmp (so be aware of this if you use this utility).


 
Performance
netmiko-grep automatically uses threads to establish concurrent SSH connections. You can test how long a given action takes by adding the '--display-runtime' argument.

$ ./netmiko-grep --display-runtime 'bgp' all
cisco_xrv.txt:router bgp 44
cisco_xrv.txt: bgp router-id 10.220.88.38
pynet_rtr1.txt:router bgp 42
pynet_rtr1.txt: bgp router-id 10.220.88.20
pynet_rtr1.txt: bgp log-neighbor-changes
Total time: 0:00:10.975614 

The above command took about 11 total seconds to execute on ten test devices. Note, it takes some of my virtual devices about 8 to 9 seconds to individually execute the above command (whereas the physical devices were executing in ~3 to 6 seconds).

netmiko-grep also has a way to use the previously saved configurations—just add the --use-cache argument. This argument will reuse whatever output data was previously saved (by default the running-config output).

$ netmiko-grep --display-runtime 'bgp' all --use-cache
cisco_xrv.txt:router bgp 44
cisco_xrv.txt: bgp router-id 10.220.88.38
pynet_rtr1.txt:router bgp 42
pynet_rtr1.txt: bgp router-id 10.220.88.20
pynet_rtr1.txt: bgp log-neighbor-changes
Total time: 0:00:00.086278 

This is a lot faster since it just grepping local files that already exist on the system.


 
Installation process
Linux:

$ cd test_tmp/
# Grab latest release from here 
# https://github.com/ktbyers/netmiko_tools/releases 
$ wget /path/to/latest/release
$ tar -xvpf v0.1.0.tar.gz

# Now install netmiko >= 1.0.0
$ cd netmiko_tools-0.1.0/
$ pip install -r ./requirements.txt

# Create your .netmiko.yml inventory
$ vi ~/.netmiko.yml

# Now you should be able to use netmiko-grep
$ cd netmiko_tools/
$ ./netmiko-grep 'interface' cisco

# You probably need to update your PATH or move netmiko-grep 
# to somewhere logical on your PATH. 

Note, I have been testing almost exclusively on Linux; I have only done a small amount of validation on MacOS. This utility won't work on Windows (in general).



The code for netmiko-grep can be found here:

https://github.com/ktbyers/netmiko_tools


