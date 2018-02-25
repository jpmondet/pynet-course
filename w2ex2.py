#! /usr/bin/env python3

"""
Create a list of five IP addresses.

Use the .append() method to add an IP address onto the end of the list. 
Use the .extend() method to add two more IP addresses to the end of the list.

Use list concatenation to add two more IP addresses to the end of the list.

Print out the entire list of ip addresses. 
Print out the first IP address in the list. 
Print out the last IP address in the list.

Using the .pop() method to remove the first IP address 
in the list and the last IP address in the list.

Update the new first IP address in the list to be '2.2.2.2'. 
Print out the new first IP address in the list.
"""

from __future__ import print_function, unicode_literals

IP_ADDRESSES = []
for nb in range(5):
    IP_ADDRESSES.append("10.0.0." + str(nb))
IP_ADDRESSES.append("111.111.111.111")
IP_ADDRESSES.extend(["2.2.2.2","3.3.3.3"])
IP_ADDRESSES = IP_ADDRESSES + ["4.4.4.4","5.5.5.5"]

print(IP_ADDRESSES)
print(IP_ADDRESSES[0])
print(IP_ADDRESSES[-1])

IP_ADDRESSES.pop(0)
IP_ADDRESSES.pop(-1)
IP_ADDRESSES[0] = "2.2.2.2"
print(IP_ADDRESSES[0])
