#! /usr/bin/env python3

"""
Use send_command() to send a show command down the SSH channel.
Retrieve the results and print the results to the screen.
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

    output = net_connect.send_command("show ip int b")
    print(output)

    net_connect.disconnect()




if __name__ == '__main__':
    main()
