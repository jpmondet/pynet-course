#! /usr/bin/env python3

"""
Use send_config_set() and
send_config_from_file()
to make configuration changes. 

The configuration changes should be benign.
For example, on Cisco IOS I typically change the logging buffer size. 

As part of your program verify that the configuration
change occurred properly.
For example, use send_command() to execute 'show run'
and verify the new configuration.
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

#    commands = ['int gi3', 'ip addr 1.2.3.4 255.255.255.0']
#
#    output = net_connect.send_config_set(commands)
#    print(output)
#
#    output = net_connect.send_command('sh run int gi3')
#    print(output)
#
    output = net_connect.send_config_from_file('commands_file')
    print(output)

    output = net_connect.send_command('sh run int gi3')
    print(output)

    net_connect.disconnect()




if __name__ == '__main__':
    main()
