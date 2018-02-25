#! /usr/bin/env python3


"""
Create three separate lists of IP addresses. 
The first list should be the IP addresses of the Houston data center routers, 
and it should have over ten RFC1918 IP addresses in it (including some duplicate IP addresses).

The second list should be the IP addresses of the Atlanta data center routers, 
and it should have at least eight RFC1918 IP addresses 
(including some addresses that overlap with the Houston data center).

The third list should be the IP addresses of the Chicago data center routers, 
and it should have at least eight RFC1918 IP addresses. 
The Chicago IP addresses should have some overlap with both the IP addresses in Houston and Atlanta.

Convert each of these three lists to a set.

Using a set operation, find the IP addresses that are duplicated between Houston and Atlanta.

Using set operations, find the IP addresses that are duplicated in all three sites.

Using set operations, find the IP addresses that are entirely unique in Chicago.
"""

from __future__ import print_function, unicode_literals
from random import randint


def generating_ips(nb_of_ips):
    list_ips = []
    for nb in range(nb_of_ips):
        #.{randint(1,254)}.{randint(1,254)}
        list_ips.append("10.0.0.{0}".format(randint(1,9)))
    list_ips.sort()
    return list_ips

def main():
    houston_ips = generating_ips(10)
    atlanta_ips = generating_ips(8)
    chicago_ips = generating_ips(8)
    print("houston : {} \natlanta : {} \nchicago : {}".format(houston_ips, atlanta_ips, chicago_ips))

    houston_ips = set(houston_ips)
    atlanta_ips = set(atlanta_ips)
    chicago_ips = set(chicago_ips)

    print("duplicated between Houston & Atlanta : {}".format(houston_ips & atlanta_ips))
    print("duplicated in all sites : {}".format(houston_ips & atlanta_ips & chicago_ips))
    print("Unique in Chicago : {}".format( (chicago_ips - (houston_ips | atlanta_ips)) or 'No unique address, retry please' ))

if __name__ == '__main__':
    main()