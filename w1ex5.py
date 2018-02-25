#! /usr/bin/env python3

"""
You have the following three variables from the arp table of a router:

mac1 = "Internet  10.220.88.29           94   5254.abbe.5b7b  ARPA   FastEthernet4"
mac2 = "Internet  10.220.88.30            3   5254.ab71.e119  ARPA   FastEthernet4"
mac3 = "Internet  10.220.88.32          231   5254.abc7.26aa  ARPA   FastEthernet4"

Process these ARP entries and print out a table of "IP ADDR" to "MAC ADDRESS" mappings. The output should look like following:

             IP ADDR          MAC ADDRESS
-------------------- --------------------
        10.220.88.29       5254.abbe.5b7b
        10.220.88.30       5254.ab71.e119
        10.220.88.32       5254.abc7.26aa


Two columns, 20 characters wide, data right aligned, a header column.

"""
from __future__ import print_function, unicode_literals


mac1 = "Internet  10.220.88.29           94   5254.abbe.5b7b  ARPA   FastEthernet4"
mac2 = "Internet  10.220.88.30            3   5254.ab71.e119  ARPA   FastEthernet4"
mac3 = "Internet  10.220.88.32          231   5254.abc7.26aa  ARPA   FastEthernet4"


arp1, mac1 = mac1.split()[1], mac1.split()[3]
arp2, mac2 = mac2.split()[1], mac2.split()[3]
arp3, mac3 = mac3.split()[1], mac3.split()[3]

print("{:>20} {:>20}".format("IP ADDR", "MAC ADDRESS"))
print("-" * 20 + " " + "-" * 20 )
print("{:>20} {:>20}".format(arp1, mac1))
print("{:>20} {:>20}".format(arp2, mac2))
print("{:>20} {:>20}".format(arp3, mac3))
