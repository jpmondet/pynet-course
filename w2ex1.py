#! /usr/bin/env python3

"""
 Open the "show_version.txt" file for reading. 
 Use the .read() method to read in the entire file contents to a variable. 
 Print out the file contents to the screen. Also print out the type of the variable 
 (you should have a string at this point).

Close the file.

Open the file a second time using a Python context manager (with statement). 
Read in the file contents using the .readlines() method. 
Print out the file contents to the screen. 
Also print out the type of the variable (you should have a list at this point).
"""

import __future__

with open("show_version.txt","r") as f:
    file = f.read()
    print(file)
    print(type(file))

with open("show_version.txt","r") as f:
    file_lines = f.readlines()
    print(file_lines)
    print(type(file_lines))
