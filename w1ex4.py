#! /usr/bin/env python3

"""
Create a show_version variable that contains the following

 show_version = "*0        CISCO881-SEC-K9       FTX0000038X    " 


Remove all leading and trailing whitespace from the string.

Split the string and extract the model and serial_number from it.

Check if 'Cisco' is contained in the model string (ignore capitalization).

Check if '881' is in the model string.

Print out both the serial number and the model.
"""
from __future__ import print_function, unicode_literals

show_version = "*0        CISCO881-SEC-K9       FTX0000038X    "

show_version = show_version.strip()

### Not the easy way because I thought we had to specify the space character in split() (see next comment)
sh_ver_split = show_version.split(' ')
sh_ver_split_cleaned = []
for cell in sh_ver_split:
    if cell:
        sh_ver_split_cleaned.append(cell)
# The easy is without specifying the separation character. 
# This way, the useless cells are automatically ignored
sh_ver_split = show_version.split()


misc, model, serial = sh_ver_split_cleaned

print("Is Cisco in model ? {}".format("cisco" in model.lower()))

print("Is 881 in model ? {}".format("881" in model))

print("serial: {}, model: {}".format(serial, model))