#! /usr/bin/env python3

"""
Read the 'show_ip_bgp_summ.txt' file into your program.

From this BGP output obtain the first and last lines of the output

From the first line use the string .split()
method to obtain the local AS number.

From the last line use the string .split()
method to obtain the BGP peer IP address.

Print both local AS number and the BGP
peer IP address to the screen.
"""

from __future__ import print_function, unicode_literals

with open("show_ip_bgp_summ.txt", 'r') as sibs:
    sibsr = sibs.readlines()
    sibs1 = sibsr[0].split()
    sibs_last = sibsr[-1].split()
    as_num = sibs1[-1]
    peer = sibs_last[0]

    print("Local AS = {} and peer : {}".format(as_num, peer))
