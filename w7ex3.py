#! /usr/bin/env python3

"""
3a. Create a YAML file that defines a list of interface names. 
Use the expanded form of YAML.

Use a Python script to read in this YAML list and print it to the screen.

The output of your Python script should be:

['Ethernet1', 'Ethernet2', 'Ethernet3', 
'Ethernet4', 'Ethernet5', 'Ethernet6', 
'Ethernet7', 'Management1', 'Vlan1']



3b. Expand the data structure defined earlier in exercise 3a.
This time you should have an 'interfaces' key that refers to a dictionary.

Use Python to read in this YAML data structure and print this to the screen.

The output of your Python script should look as follows 
(in other words, your YAML data structure should yield 
the following when read by Python). 
You YAML data structure should be written in expanded YAML format.


{'interfaces': {
    'Ethernet1': {'mode': 'access', 'vlan': 10},
    'Ethernet2': {'mode': 'access', 'vlan': 20},
    'Ethernet3': {'mode': 'trunk',
                  'native_vlan': 1,
                  'trunk_vlans': 'all'}
    }
}
"""

from __future__ import print_function, unicode_literals
from jinja2 import Environment, FileSystemLoader
import yaml as yaml
from pprint import pprint


def main():
    with open("intf.yaml") as intfs:
        try:
            intf = yaml.load(intfs)
            pprint(intf)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    main()
