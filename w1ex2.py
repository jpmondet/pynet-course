#! /usr/bin/env python3

"""
2. Prompt a user to enter in an IP address 
from standard input. Read the IP address in
 and break it up into its octets.
  Print out the octets in decimal, binary, and hex.

Your program output should look like the following:

​ $ python exercise2.py 
Please enter an IP address: 80.98.100.240

    Octet1         Octet2         Octet3         Octet4     
------------------------------------------------------------
      80             98             100            240      
   0b1010000      0b1100010      0b1100100     0b11110000   
     0x50           0x62           0x64           0xf0      
------------------------------------------------------------


Four columns, fifteen characters wide, a header column, 
data centered in the column.
"""

from __future__ import print_function

print("Which IP would you want to dissect ?")
try:
    ip_addr = raw_input("> ")
except NameError as ne:
    ip_addr = input("> ")


splitted_ip = ip_addr.split('.')
# Trying some arguments of format()
print("{:{padding}{align}{width}}{:{padding}{align}{width}}\
{:{padding}{align}{width}}{:{padding}{align}{width}}"\
    .format("Octet1","Octet2","Octet3", "Octet4", padding='~',\
     align='^', width='15'))
print("-" * 60)
print("{:^15}{:^15}{:^15}{:^15}".format(splitted_ip[0],splitted_ip[1],splitted_ip[2],splitted_ip[3]))
print("{:^15}{:^15}{:^15}{:^15}".format(bin(int(splitted_ip[0])),bin(int(splitted_ip[1])),bin(int(splitted_ip[2])),bin(int(splitted_ip[3]))))
print("{:^15}{:^15}{:^15}{:^15}".format(hex(int(splitted_ip[0])),hex(int(splitted_ip[1])),hex(int(splitted_ip[2])),hex(int(splitted_ip[3]))))
print("-" * 60)