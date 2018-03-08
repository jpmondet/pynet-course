#! /usr/bin/env python3

"""
Create a function that randomly generates an IP address for a network.
The default base network should be '10.10.10.'.
For simplicity the network will always be a /24.

You should be able to pass a different base network into your function as an argument.

Randomly pick a number between 1 and 254 for the last octet and return the full IP address.

You can use the following to randomly generate the last octet:

import random
random.randint(1, 254)
"""

from __future__ import print_function, unicode_literals
import random
import sys

def generate_random_ip(subnet='10.10.10.'):
    last_octet = random.randint(1, 254)
    return subnet + str(last_octet) + '/24'


def main():
    if len(sys.argv) > 1:
        ip_addr = generate_random_ip(sys.argv[1])
    else:
        ip_addr = generate_random_ip()

    print(ip_addr)

if __name__ == '__main__':
    main()

