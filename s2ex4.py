#! /usr/bin/env python3

"""
Read in the "show_ip_int_brief.txt" file into your
program using the .readlines() method.

Obtain the list entry associated with the
FastEthernet4 interface.
You can just hard-code the index at this
point since we haven't covered for-loops
or regular expressions. Use the string
.split() method to obtain both the IP address
and the corresponding MAC address
associated with the IP.

Create a two element tuple from
the result (intf_name, ip_address).

Print that tuple to the screen.

Use pycodestyle on this script. Get the warnings/errors to zero.
You might need to 'pip install pycodestyle' on your computer
(you should be able to type this from the shell prompt).
Alternatively, you can type 'python -m pip install pycodestyle'.
"""

from __future__ import print_function, unicode_literals

sipib = open('show_ip_int_brief.txt', 'r').readlines()

ip_address = ""
mac_address = ""
for intf in sipib:
    if "FastEthernet4" in intf:
        ip_address = intf.split()[1]

with open('show_arp.txt', 'r') as arp:
    for mac in arp.readlines():
        if ip_address in mac:
            mac_address = mac.split()[3]
tupled = ("FastEthernet4", ip_address, mac_address)
print(tupled)
