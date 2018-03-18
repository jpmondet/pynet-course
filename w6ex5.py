#! /usr/bin/env python3

"""
    Using TextFSM to get structured outputs
    Need to add NET_TEXTFSM env variable. Exple : 
    export NET_TEXTFSM=./ntc-templates/templates
"""

from __future__ import print_function, unicode_literals

from netmiko import Netmiko


def main():

    my_device = {
        'host': 'ios-xe-mgmt.cisco.com',
        'username': 'root',
        'password': 'D_Vay!_10&',
        'device_type': 'cisco_ios',
        'port': 8181
    }
    net_connect = Netmiko(**my_device)

    routes = net_connect.send_command('sh ip route', use_textfsm=True)
    neigbors = net_connect.send_command('sh cdp neighbor', use_textfsm=True)
    arp_entries = net_connect.send_command('sh ip arp', use_textfsm=True)

    print("ROUTES : \n")
    for route in routes:
        print(route)

    print("NEIGHBORS : \n")
    if type(neigbors) == list: 
        for nei in neigbors:
            print(nei)

    print("ARPs : \n")
    for arp in arp_entries:
        print(arp)

    net_connect.disconnect()




if __name__ == '__main__':
    main()
    net_connect.disconnect()




if __name__ == '__main__':
    main()
