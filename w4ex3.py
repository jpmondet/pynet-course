#!/usr/bin/env python3

"""
Read in the 'show_version.txt' file. 
From this file, use regular expressions 
to extract the OS version, serial number, and configuration register values.

Your output should look as follows:

OS Version: 15.4(2)T1      
Serial Number: FTX0000038X    
​Config Register: 0x2102 
"""

from __future__ import print_function, unicode_literals
import re



def main():

    with open('show_version.txt') as shver:
        sh_ver = shver.read()
        match = re.search(r'.*?, Version (.*?),.*?', sh_ver)
        print('OS Version: {}'.format(match.group(1)))
        match = re.search(r'SN\n.*? \w+-\w+-\w+.*?(\w+).*?', sh_ver, re.DOTALL)
        print('Serial Number: {}'.format(match.group(1)))
        match = re.search(r'Configuration register is (\w+)', sh_ver, re.DOTALL)
        print('Config Register: {}'.format(match.group(1)))

if __name__ == '__main__':
    main()