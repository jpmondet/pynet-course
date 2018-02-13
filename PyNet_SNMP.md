PyNet_S2.md

In this article, I briefly introduce Python and SNMP using the pysnmp library.

I assume that you already have some knowledge on SNMP including MIBs and OIDs.  If not, you should be able to find this information fairly easily on the Internet.

 

In order to get started, you need to install the pysnmp library.  For context, I am testing on an AWS AMI server (RedHat based i.e. yum instead of apt).

For installation just use 'pip':
# As root or sudo (or in a virtual environment)
$ pip install pysnmp


I also installed net-snmp to simplify testing and to add an easy way to perform an SNMP walk.  The installation method for net-snmp will vary depending on your system.

# As root or sudo
$ yum install net-snmp
$ yum install net-snmp-utils

 

To keep things simple I am only going to use SNMPv1/2c (i.e. this article does not cover SNMPv3).  This is obviously not secure.

 

Now that I have the pysnmp library installed, the next step is to verify that I can communicate with my test router using SNMP.  First, let's test this directly from the Linux command line: 

$ snmpget -v 2c -c <COMMUNITY> <IP_ADDR> .1.3.6.1.2.1.1.1.0
SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software, C880 Software (C880DATA-UNIVERSALK9-M), Version 15.0(1)M4, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2010 by Cisco Systems, Inc.
Compiled Fri 29-Oct-10 00:02 by prod_rel_team


The OID .1.3.6.1.2.1.1.1.0 is the MIB-2 sysDecr object.  During testing I had multiple problems getting SNMP to work on the router including that I had Cisco's Control Plane Policing enabled (ooops) and that I needed to allow access through both an edge ACL and through a separate SNMP ACL.

At this point, I am able to communicate using SNMP from my AWS server to my test router.

 

Now let's try the same thing except using the pysnmp library.  In order to simplify this I have created a couple of SNMP helper functions see:

https://github.com/ktbyers/pynet/tree/master/snmp/snmp_helper.py

First we need to do some initialization:
>>> from snmp_helper import snmp_get_oid,snmp_extract
>>>
>>> COMMUNITY_STRING = '<COMMUNITY>'
>>> SNMP_PORT = 161
>>> a_device = ('1.1.1.1', COMMUNITY_STRING, SNMP_PORT)

This code loads my two functions (snmp_get_oid and snmp_extract); it also creates a tuple named 'a_device' consisting of an IP, community string, and port 161.

I then call my snmp_get_oid function using the OID of MIB-2 sysDescr:
>>> snmp_data = snmp_get_oid(a_device, oid='.1.3.6.1.2.1.1.1.0', display_errors=True)
>>> snmp_data
[(MibVariable(ObjectName(1.3.6.1.2.1.1.1.0)), DisplayString(hexValue='436973636f20494f5320536f6674776172652c204338383020536f6674776172652
02843383830444154412d554e4956455253414c4b392d4d292c2056657273696f6e2031352e302831294d
342c2052454c4541534520534f4654574152452028666331290d0a546563686e6963616c20537570706f72
743a20687474703a2f2f7777772e636973636f2e636f6d2f74656368737570706f72740d0a436f7079726967
68742028632920313938362d3230313020627920436973636f2053797374656d732c20496e632e0d0a436
f6d70696c6564204672692032392d4f63742d31302030303a30322062792070726f645f72656c5f74656
16d'))]
 

I can see that I received SNMP data back albeit in an ugly format.  I can now use the snmp_extract function to display the output in a more friendly way.

>>> output = snmp_extract(snmp_data)
>>> print output
Cisco IOS Software, C880 Software (C880DATA-UNIVERSALK9-M), Version 15.0(1)M4, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2010 by Cisco Systems, Inc.
Compiled Fri 29-Oct-10 00:02 by prod_rel_team

 

Now, let's repeat this process but using a different OID.  Using snmpwalk on the 'interfaces' MIB and the Cisco SNMP Object Navigator (http://t.dripemail2.com/c/eyJhY2NvdW50X2lkIjoiNDI1NDQ5NyIsImRlbGl2ZXJ5X2lkIjoiMjA2NzQ1MTI0OSIsInVybCI6Imh0dHA6Ly90b29scy5jaXNjby5jb20vU3VwcG9ydC9TTk1QL2RvL0Jyb3dzZU9JRC5kbz9sb2NhbD1lblx1MDAyNnRyYW5zbGF0ZT1UcmFuc2xhdGVcdTAwMjZvYmplY3RJbnB1dD0xLjMuNi4xLjIuMS4yLjIuMVx1MDAyNl9fcz14bjZubzZmejd5dTZ6cmtvbmR2YyNvaWRDb250ZW50In0), I was able to determine that the OID = .1.3.6.1.2.1.2.2.1.16.5 corresponded to the output octets on FastEthernet4.

Here I query that OID a couple of times in fairly quick succession (less than a minute between queries):
>>> snmp_data = snmp_get_oid(a_device, oid='.1.3.6.1.2.1.2.2.1.16.5', display_errors=True)
>>> output = snmp_extract(snmp_data)
>>> print output
293848947

>>> snmp_data = snmp_get_oid(a_device, oid='.1.3.6.1.2.1.2.2.1.16.5', display_errors=True)
>>> output = snmp_extract(snmp_data)
>>> print output
293849796

You can see that the count incremented.

 

Hopefully, this article helps you get started with Python and SNMP.