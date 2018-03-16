#! /usr/bin/env python3

"""
Using Netmiko, establish a connection to a network device 
and print out the device's prompt.

public csr1000v from devnet sandbox : 

    CSR1000V Host : ios-xe-mgmt.cisco.com
    SSH Port: 8181
    NETCONF Port: 10000
    RESTCONF Port : 9443 (HTTPS)
    Credentials:
        Username: root
    Password: D_Vay!_10&

"""

from __future__ import print_function, unicode_literals

from netmiko import Netmiko


def main():
    my_device = {
        'host': 'ios-xe-mgmt.cisco.com',
        'username': 'root',
        'password': '',
        'device_type': 'cisco_ios',
        'port': 8181
    }

    net_connect = Netmiko(**my_device)

    output = net_connect.find_prompt()
    print(output)

    net_connect.disconnect()



if __name__ == '__main__':
    main()
