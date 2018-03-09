#! /usr/bin/env python3

"""
Copy your solution from exercise3 to exercise4.
Add an 'import pdb' and pdb.set_trace() statement outside
of your function (i.e. where you have your function calls).

Inside of pdb, experiment with:
    Listing your code.
    Using 'next' and 'step' to walk through your code. Make sure you understand the difference between next and step.
    Experiment with 'up' and 'down' to move up and down the code stack.
    Use p <variable> to inspect a variable.
    Set a breakpoint and run your code to the breakpoint.
    Use '!command' to change a variable (for example !new_mac = [])
"""

from __future__ import print_function, unicode_literals
import pdb

def normalize_mac(mac_addr):
    octets = []
    if ':' in mac_addr:
        octets = mac_addr.split(':')
    elif '-' in mac_addr:
        octets = mac_addr.split('-')
    else:
        double_octets = mac_addr.split('.')
        for double in double_octets:
            octets.append(double[:2])
            octets.append(double[2:])
    mac = []
    for octet in octets:
        if len(octet) == 1:
            octet = '0' + octet
        mac.append(octet.upper())
    return mac

def main():

    pdb.set_trace()
    mac = normalize_mac('01:23:45:67:89:ab')
    print(mac)
    mac = normalize_mac('a:b:c:d:e:f')
    print(mac)
    mac = normalize_mac('00-00-aa-aa-bb-bb')
    print(mac)
    mac = normalize_mac('0000.aaaa.bbbb')
    print(mac)

if __name__ == '__main__':
    main()
