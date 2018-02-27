#! /usr/bin/env python3

"""
Read the 'show_ipv6_intf.txt' file.

From this file, use Python regular expressions to extract the two IPv6 addresses.

The two relevant IPv6 addresses you need to extract are:

2001:11:2233::a1/24
2001:cc11:22bb:0:2ec2:60ff:fe4f:feb2/64

Try to use re.DOTALL flag as part of your search.
Your search pattern should not include any of the
literal characters in the IPv6 address.

From this, create a list of IPv6 addresses that
includes only the above two addresses.

Print this list to the screen.

"""

from __future__ import print_function, unicode_literals
import re

def main():
    with open('show_ipv6_intf.txt', 'r') as siit:
        shipv6 = siit.read()
    ipv6 = re.search(r'\s{4}(\S+)\s\S+\n\s{4}(\S+)', shipv6, re.DOTALL)
    ipv6_addressses = [ipv6.group(1), ipv6.group(2)]
    print(ipv6_addressses)

if __name__ == '__main__':
    main()
