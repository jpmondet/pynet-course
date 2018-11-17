Python has numerous libraries pertaining to IP addresses. PEP3144 (Python Enhancement Proposals) creates a standardized IP address library. This PEP has been implemented in the ipaddress library which is integrated into Python as of Python 3.3 and has been back-ported to Python 2.6, 2.7, and 3.2.

What follows are some useful things you can do with the ipaddress Library.



First, you can create both IPv4Address and IPv6Address objects.

>>> import ipaddress
>>> alt_ip = ipaddress.ip_address(u'10.220.7.193')
>>> alt_ip
IPv4Address(u'10.220.7.193')
>>> str(alt_ip)
'10.220.7.193'

>>> myipv6 = ipaddress.ip_address(u'ff05::1:3')
>>> str(myipv6)
'ff05::1:3'
>>> myipv6.exploded
u'ff05:0000:0000:0000:0000:0000:0001:0003'
>>> myipv6
IPv6Address(u'ff05::1:3')


The ip_address() call is a factory function that determines the proper class to use based on the input you provide (you can also directly create an object using ipaddress.IPv4Address).

Note, when creating IPv4Address/IPv6Address objects, a unicode string is required.



There really isn't all that much you can do with just IPv4Address/IPv6Address objects. Of more value are the IPv4Network and IPv6Network classes:

>>> my_net = ipaddress.ip_network(u'10.220.192.192/29')
>>> my_net
IPv4Network(u'10.220.192.192/29')

>>> ipv6_net = ipaddress.ip_network(u'fe80::0202:b3ff:fe1e:8329/64', strict=False)
>>> ipv6_net
IPv6Network(u'fe80::/64')



By default both the IPv4Network class and the IPv6Network class require the host portion of the address to be all zeroes. You can change this behavior by setting the 'strict=False' flag as I did with above IPv6 address. The 'strict=False' flag will cause the class to accept the network, but it will still zero out the host component. If you want to support both a network component and a host component, see the IPv4Interface/IPv6Interface classes (described below).

There are several alternate forms that you can use to create an IPv4Network object:

>>> my_net = ipaddress.ip_network(u'10.220.192.192/255.255.255.248')
>>> my_net
IPv4Network(u'10.220.192.192/29')
>>> my_net = ipaddress.ip_network(u'10.220.192.192/0.0.0.7')
>>> my_net
IPv4Network(u'10.220.192.192/29')



There are also several useful attributes on IPv4Network objects:

>>> my_net.network_address
IPv4Address(u'10.220.192.192')
>>> my_net.broadcast_address
IPv4Address(u'10.220.192.199')

>>> my_net.hostmask
IPv4Address(u'0.0.0.7')
>>> my_net.netmask
IPv4Address(u'255.255.255.248')

>>> my_net.with_netmask
u'10.220.192.192/255.255.255.248'
>>> my_net.with_hostmask
u'10.220.192.192/0.0.0.7'

>>> my_net.with_prefixlen
u'10.220.192.192/29'
>>> my_net.prefixlen
29

>>> my_net.num_addresses
8



You can iterate over the hosts of a network (this excludes the network number and the broadcast address):

>>> for test_ip in my_net.hosts():
...      print test_ip
... 
10.220.192.193
10.220.192.194
10.220.192.195
10.220.192.196
10.220.192.197
10.220.192.198



You can find the subnets for a given network (fixed length subnets):

>>> my_net = ipaddress.ip_network(u'10.220.2.0/24')
>>> my_net
IPv4Network(u'10.220.2.0/24')
>>> for subnet in my_net.subnets(new_prefix=27):
...       print subnet
... 
10.220.2.0/27
10.220.2.32/27
10.220.2.64/27
10.220.2.96/27
10.220.2.128/27
10.220.2.160/27
10.220.2.192/27
10.220.2.224/27


You can also find a supernet for a given network:

>>> ipaddress.ip_network(u'10.220.167.0/24').supernet(new_prefix=20)
IPv4Network(u'10.220.160.0/20')

 

Finally, the ipaddress library includes both IPv4Interface and IPv6Interface classes. These classes allow both a host component and a network component in one object:

>>> my_ip = ipaddress.ip_interface(u'10.220.192.194/29')
>>> my_ip
IPv4Interface(u'10.220.192.194/29')

>>> my_ipv6 = ipaddress.ip_interface(u'fe80::0202:b3ff:fe1e:8329/64')
>>> my_ipv6
IPv6Interface(u'fe80::202:b3ff:fe1e:8329/64')


From this you can obtain both the IP address and the IP network:

>>> my_ip.ip
IPv4Address(u'10.220.192.194')
>>> my_ip.network
IPv4Network(u'10.220.192.192/29')




The ipaddress library (while by no means earth shattering) has some useful features that could be used for ACL construction, ping sweeping, minor input validation, network-subnet determination, etc. Why re-invent the wheel when an okay one already exists. 



