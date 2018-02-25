#! /usr/bin/env python3

"""
Read the 'show_lldp_neighbors_detail.txt' file. 
Loop over the lines of this file. 
Keep reading the lines until you have encountered 
the remote "System Name" and remote "Port id". 
Save these two items into variables and print them to the screen. 
You should extract only the system name and port id from the lines 
(i.e. your variables should only have 'twb-sf-hpsw1' and '15'). 
Break out of your loop once you have retrieved these two items.

"""

from __future__ import print_function, unicode_literals

with open("show_lldp_neighbors_detail.txt", "r") as slnd:
    port_id = ""
    sysn = ""
    for line in slnd.readlines():
        if "Port id" in line:
            port_id = line.split(":")[1]
            # Interesting trick by K.B. : 
            # _, port_id = line.split("Port id: ")
        if "System Name" in line:
            sysn = line.split(":")[1]
        if port_id and sysn:
            print("Looks like we found that \
Port id is {} & System name is {}"
                .format(port_id, sysn))
            break