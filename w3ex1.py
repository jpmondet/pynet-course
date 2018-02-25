#! /usr/bin/env python3

"""

Read the "show_vlan.txt" file into your program. 
Loop through the lines in this file and extract all 
of the VLAN_ID, VLAN_NAME combinations. 
From these VLAN_ID and VLAN_NAME construct a new 
list where each element in the list is a tuple 
consisting of (VLAN_ID, VLAN_NAME). 
Print this data structure to the screen. 
Your output should look as follows:

[('1', 'default'),
 ('400', 'blue400'),
 ('401', 'blue401'),
 ('402', 'blue402'),
 ('403', 'blue403')]

"""

from __future__ import print_function, unicode_literals
from pprint import pprint

with open("show_vlan.txt","r") as sv:
    new_list = []
    for line in sv.readlines()[2:]:
        line_split = line.split()
        try:
            new_list.append((int(line_split[0]),line_split[1]))
        except:
            pass
    pprint(new_list)