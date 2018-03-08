As a quick overview, SNMPv3 was standardized in 2002.  It added both encryption and a reasonable authentication scheme to SNMP.  Prior to this, both SNMPv1 and SNMPv2c relied on a simple community string that passed clear-text on the wire. Similarly, all of the SNMP data itself was not encrypted in SNMPv1 and SNMPv2c.


In order to use SNMPv3, I configured the following on a Cisco 881 router:

>>>>
snmp-server view VIEWSTD iso included
snmp-server group READONLY v3 priv read VIEWSTD access 98
snmp-server user pysnmp READONLY v3 auth sha <auth_key> priv aes 128 <crypt_key>
>>>>

The above commands accomplish three items.  First, a view is created that allows access to the entire SNMP tree.  Second, a read-only group is created that requires both authentication and encryption ('priv' option) and that uses the previously created view.  Third, an SNMP user is created named 'pysnmp' that is bound to the READONLY group and that uses SHA authentication with AES128 encryption.

Note, ACL98 is also bound to the READONLY group, but this ACL is currently configured to allow all IP.

 

After the router is configured, we should be able to connect to it using SNMPv3:

$ snmpget -v 3 -u pysnmp -l authpriv -a SHA -A "<auth_key>" -x AES -X "<crypt_key>" <ip_address>:7961 sysUpTime.0

DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (370751064) 42 days, 21:51:50.64
 

Here I use the snmpget command to retrieve the system uptime.  This command uses SNMPv3 (-v 3), a username of pysnmp (-u pysnmp), both encryption and authentication (-l authpriv), SHA authentication (-a SHA), and AES encryption (-x AES).  The command above also uses a non-standard SNMP port (7961) due to a static PAT (i.e. there is a firewall performing PAT between the test server and the router).



Now that we can communicate with the router using SNMPv3, let's try to connect using Python's PySNMP library.  In order to do this, I created an SNMPv3 helper function named snmp_get_oid_v3.  You can find this function in the following library:

https://github.com/ktbyers/pynet/blob/master/snmp/snmp_helper.py


The function definition is as follows:

def snmp_get_oid_v3(snmp_device, snmp_user, oid='.1.3.6.1.2.1.1.1.0',
           auth_proto='sha', encrypt_proto='aes128', display_errors=True):

snmp_device is a tuple consisting of (IP_or_hostname, snmp_port); snmp_user is also a tuple consisting of (username, auth_key, encrypt_key).  The default OID is the MIB-2 sysDescr field.  I also intentionally set the default authentication and the default encryption to match the settings of my router (i.e. SHA and AES128).

Here is an example of using this function to retrieve data via SNMPv3: 

>>> import snmp_helper
>>>  
>>> IP = '10.10.10.10'
>>>
>>> a_user = 'pysnmp'
>>> auth_key = '********'
>>> encrypt_key = '********'
>>>
>>> snmp_user = (a_user, auth_key, encrypt_key)
>>>
>>> pynet_rtr1 = (IP, 7961)
>>>
>>> snmp_data = snmp_helper.snmp_get_oid_v3(pynet_rtr1, snmp_user)
>>> output = snmp_helper.snmp_extract(snmp_data)
>>>
>>> print output
Cisco IOS Software, C880 Software (C880DATA-UNIVERSALK9-M), Version 15.4(2)T1, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Thu 26-Jun-14 14:15 by prod_rel_team

* The IP, auth_key, and encrypt_key values have been masked or otherwise modified.

Note, the call to snmp_helper.snmp_extract uses a second function in the snmp_helper library.  This snmp_extract function converts the output data into a more readable form.



Now let's repeat this process using a different OID.  For example, sysUpTime:

>>> sys_uptime = '1.3.6.1.2.1.1.3.0'
>>> snmp_data = snmp_helper.snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=sys_uptime)
>>> output = snmp_helper.snmp_extract(snmp_data)
>>> print output
370829991

 

The sysUpTime value is in hundredths of seconds.  Consequently, the above value is an uptime of slightly less than 43 days.



Thus, we are able to communicate with a Cisco router using an encrypted and authenticated SNMP channel via Python.

