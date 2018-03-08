#! /usr/bin/env python3

"""
Create an ssh_conn function. This function should have three parameters:
    ip_addr, username, and password. The function should print out each
    of these three variables and clearly indicate which variable it is printing out.

Call this ssh_conn function using entirely positional arguments.

Call this ssh_conn function using entirely named arguments.

Call this ssh_conn function using a mix of positional and named arguments.
"""

from __future__ import print_function, unicode_literals


def ssh_conn(ip_addr, username, password):
    print("\nIP_addr : {} \nusername: {} \npassword: {}\n".format(ip_addr, username, password))

def main():
    ssh_conn('10.0.0.1', 'user1', 'pwd')
    ssh_conn(password='pwd_named', username='user1_named', ip_addr='10.0.0.2')
    ssh_conn('10.0.0.3', password='pwd_named', username='user1_named')


if __name__ == '__main__':
    main()


