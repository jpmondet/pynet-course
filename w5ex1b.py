#! /usr/bin/env python3

"""
Expand on the ssh_conn function from exercise1 except add a fourth
parameter 'device_type' with a default value of 'cisco_ios'.
Print all four of the function variables out as part of the function's execution.

Call the 'ssh_conn2' function both with and without specifying the device_type

Create a dictionary that maps to the function's parameters.
Call this ssh_conn2 function using the **kwargs technique.
"""

from __future__ import print_function, unicode_literals


def ssh_conn(ip_addr, username, password, device_type='cisco_ios'):
    print("\nIP_addr : {} \nusername: {} \npassword: {} \
          \ndevice type: {}".format(ip_addr, username, password, device_type))

def main():
    ssh_conn('10.0.0.1', 'user1', 'pwd')
    ssh_conn('10.0.0.1', 'user1', 'pwd', device_type='junos')

    parameters = {
        'ip_addr': '10.10.10.10',
        'username': 'user10',
        'password': 'pwd10',
        'device_type': 'nxos'
    }
    ssh_conn(**parameters)

if __name__ == '__main__':
    main()
