#! /usr/bin/env python3

"""
Create three different variables 
the first variable should use all lower case characters with underscore ( _ ) as the word separator. 
The second variable should use all upper case characters with underscore as the word separator. 
The third variable should use numbers, letters, and underscore, but still be a valid variable Python variable name.

Make all three variables be strings that refer to IPv6 addresses.

Use the from future technique so that any string literals in Python2 are unicode.

compare if variable1 equals variable2
compare if variable1 is not equal to variable3
"""
from __future__ import unicode_literals

ipvsix_address = "2001::1"
IPV6_ADDR = "2001::2"
ipv6_aDDress = "2001::3"

if ipvsix_address == IPV6_ADDR:
    print('variable1 == variable2')
else:
    print('variable1 != variable2')
if ipvsix_address != ipv6_aDDress:
    print('variable1 != variable3')
else:
    print('variable1 == variable3')
## OR
print("variable1 equal to variable2 ?  {}".format(ipvsix_address == IPV6_ADDR))
print("variable1 not equal to variable3 ? {}".format(ipvsix_address != ipv6_aDDress))
