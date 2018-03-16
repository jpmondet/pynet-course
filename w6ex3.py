#! /usr/bin/env python3

"""
Find a command on your device that has additional prompting.
Use send_command_timing to send the command down the SSH channel.
Capture the output and handle the additional prompting.
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
    prompt = net_connect.find_prompt()
    output = net_connect.send_command_timing("delete bootflash:macdb.txt", strip_prompt=False, strip_command=False)
    while prompt not in output:
        output += net_connect.send_command_timing('n')
    print(output)

    net_connect.disconnect()




if __name__ == '__main__':
    main()
