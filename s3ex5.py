#! /usr/bin/env python3

"""
Construct a list of 254 IP addresses. 
The base IP address should be equal to '10.10.100.0' or '10.10.100.'.

You should use the 'range' builtin to accomplish this.

Your list should have all of the IP addresses from 10.10.100.1 to 10.10.100.254.

Use Python's 'enumerate' to print out all of the IP addresses 
and their corresponding list index. 
The output should look similar to the following: 

0 ---> 10.10.100.1
1 ---> 10.10.100.2
2 ---> 10.10.100.3
3 ---> 10.10.100.4
4 ---> 10.10.100.5
...


Use a list slice to create a new list 
that goes from 10.10.100.3 to 10.10.100.6.

Using a loop and os.system("ping -c 2 10.10.100.3") 
try pinging all of the IP addresses in this short list. 
For Windows the command will probably be os.system("ping -n 2 10.10.100.3").

Put a variable at the top to define whether 
you are using Windows or Linux/MacOs. 
This should be similar to the following:

WINDOWS = False

base_cmd_linux = 'ping -c 2'
base_cmd_windows = 'ping -n 2'
# Ternary operator
base_cmd = base_cmd_windows if WINDOWS else base_cmd_linux

"""

from __future__ import print_function, unicode_literals
import os

WINDOWS = False
base_cmd_linux = 'ping -c 2'
base_cmd_windows = 'ping -n 2'
base_cmd = base_cmd_windows if WINDOWS else base_cmd_linux

ip_addresses = []
base_ip = "10.10.100."
for x in range(255):
    ip_addresses.append(base_ip + str(x))

for index, ip_addr in enumerate(ip_addresses):
    print("{} ---> {}".format(index, ip_addr))

sliced_ip_addresses = ip_addresses[3:7]
for ip in sliced_ip_addresses:
    os.system("{} {}".format(base_cmd, ip))

