#! /usr/bin/env python3

"""
Read the contents of the "show_arp.txt" file. 
Using a for loop, iterate over the lines of this file. 
Process the lines of the file and separate out the ip_addr 
and mac_addr for each entry into a separate variable.

Add a conditional statement that searches for '10.220.88.1'.
 If 10.220.88.1 is found, print out the string "Default gateway IP/Mac"
  and the corresponding IP address and MAC Address.

Using a conditional statement, also search for '10.220.88.30'.
 If this IP address is found, then print out "Arista3 IP/Mac is"
  and the corresponding ip_addr and mac_addr.

Keep track of whether you have found both the Default Gateway 
and the Arista3 switch. Once you have found both of these devices,
'break' out of the for loop.

"""

from __future__ import print_function, unicode_literals

with open("show_arp.txt", "r") as sa:
    track_gw = True
    track_ar3 = True
    for line in sa.readlines()[1:]:
        ip_addr = line.split()[1]
        mac_addr = line.split()[3]  
        if "10.220.88.1" in ip_addr:
            print("Default gateway IP/Mac {}/{}".format(ip_addr,mac_addr))
            track_gw = False
        if "10.220.88.30" in ip_addr:
            print("Arista3 IP/Mac {}/{}".format(ip_addr,mac_addr))
            track_ar3 = False
        if not track_gw and not track_ar3:
            print("Ok, found everything")
            break
