#! /usr/bin/env python3

"""
Similar to lesson3, exercise4 write a function
that normalizes a MAC address to the following format:

01:23:45:67:89:AB

This function should handle the lower-case to upper-case conversion.

It should also handle converting from '0000.aaaa.bbbb'
and from '00-00-aa-aa-bb-bb' formats.

The function should have one parameter, the mac_address.
It should return the normalized MAC address

Single digit bytes should be zero-padded to two digits.

In other words, this:
a:b:c:d:e:f
should be converted to:
0A:0B:0C:0D:0E:0F

Write several test cases for your function and verify it is working properly.
"""

from __future__ import print_function, unicode_literals


def normalize_mac(mac_addr):
    octets = []
    if ':' in mac_addr:
        octets = mac_addr.split(':')
    elif '-' in mac_addr:
        octets = mac_addr.split('-')
    else:
        double_octets = mac_addr.split('.')
        for double in double_octets:
            if len(double) < 4:
                double = double.zfill(4)
            octets.append(double[:2])
            octets.append(double[2:])
    mac = []
    for octet in octets:
        if len(octet) == 1:
            octet = '0' + octet
        mac.append(octet.upper())
    return ':'.join(mac)

def main():

    mac = normalize_mac('01:23:45:67:89:ab')
    print(mac)
    mac = normalize_mac('a:b:c:d:e:f')
    print(mac)
    mac = normalize_mac('00-00-aa-aa-bb-bb')
    print(mac)
    mac = normalize_mac('0000.aaaa.bbbb')
    print(mac)

    assert "01:23:02:34:04:56" == normalize_mac('123.234.456')
    assert "AA:BB:CC:DD:EE:FF" == normalize_mac('aabb.ccdd.eeff')
    assert "00:BB:CC:DD:00:FF" == normalize_mac('bb.ccdd.ff')
    assert "0A:0B:0C:0D:0E:0F" == normalize_mac('a:b:c:d:e:f')
    assert "01:02:0A:0B:03:44" == normalize_mac('1:2:a:b:3:44')
    assert "0A:0B:0C:0D:0E:0F" == normalize_mac('a-b-c-d-e-f')
    assert "01:02:0A:0B:03:44" == normalize_mac('1-2-a-b-3-44')
    print('Ok, asserts done') 

if __name__ == '__main__':
    main()
