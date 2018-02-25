#! /usr/bin/env python3

"""
Create a dictionary representing a network device. 
The dictionary should have key-value pairs representing 
the 'ip_addr', 'vendor', 'username', and 'password' fields.

Print out the 'ip_addr' key from the dictionary.

If the 'vendor' key is 'cisco', then set the 'platform' to 'ios'. 
If the 'vendor' key is 'juniper', then set the 'platform' to 'junos'.

Create a second dictionary named 'bgp_fields'.
The 'bgp_fields' dictionary should have a keys for 'bgp_as', 'peer_as', and 'peer_ip'.

Using the .update() method add all of the 'bgp_fields' 
dictionary key-value pairs to the network device dictionary.

Using a for-loop, iterate over the dictionary 
and print out all of the dictionary keys.

Using a single for-loop, iterate over the dictionary 
and print out all of the dictionary keys and values.

"""
from __future__ import print_function, unicode_literals


def main():
    dict_net_device = {
        'ip_addr' : '10.0.0.1',
        'vendor' : 'cisco',
        'username' : 'user',
        'password' : 'pass'
    }

    print('ip addr = {}'.format(dict_net_device['ip_addr']))

    if 'cisco' in dict_net_device['vendor']:
        dict_net_device['platform'] = 'ios'
    elif 'juniper' in dict_net_device['vendor']:
        dict_net_device['platform'] = 'junos'

    bgp_fields = {
        'bgp_as' : '10',
        'peer_as' : '11',
        'peer_ip' : '10.0.0.2',
    }
    dict_net_device.update(bgp_fields)

    for k, v in dict_net_device.items(): 
        print('key {}, value {}'.format(k, v))


if __name__ == '__main__':
    main()