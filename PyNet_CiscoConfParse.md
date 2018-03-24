PyNet_CiscoConfParse.md

There is a Python library named ciscoconfparse that helps you parse Cisco hierarchical configurations. This would include other vendors that are Cisco-like. Now what I mean by Cisco-like is that the configuration is text-based and that it uses indentation to indicate configuration hierarchy.


For example, consider the following configuration:

interface FastEthernet4
 description *** LAN connection (don't change) ***
 ip address 10.220.88.20 255.255.255.0
 duplex auto
 speed auto

'description', 'ip address', 'duplex', and 'speed' are all configuration items pertaining to interface FastEthernet4. They are inside FastEthernet4 hierarchically.



Now programmatic string processing of Cisco configurations can get complex. The ciscoconfparse library greatly helps with this. It can be used to identify the parent/child relationships of the Cisco hierarchy and it adds convenient searching capabilities.

Let's look at some examples of this.

Now one minor note on terminology. There is a ciscoconfparse library which I am going to identify in all lower case. There is also a CiscoConfParse class which I will identify in this Python PEP8 style.



First, I have installed ciscoconfparse using:

pip install ciscoconfparse


Then I have a Cisco configuration that contains the following:

interface FastEthernet0
 no ip address
!
interface FastEthernet1
 no ip address
!
interface FastEthernet2
 no ip address
!
interface FastEthernet3
 no ip address
!
interface FastEthernet4
 description *** LAN connection (don't change) ***
 ip address 10.220.88.20 255.255.255.0
 duplex auto
 speed auto
!
interface Vlan1
 no ip address



Now let's go into the Python interpreter shell and see what we can do with CiscoConfParse.

First we have to load the CiscoConfParse class.

>>> from ciscoconfparse import CiscoConfParse


Then I use CiscoConfParse to parse my Cisco configuration (which resides in an external file):

>>> cisco_cfg = CiscoConfParse("cisco.txt")
>>> cisco_cfg
<CiscoConfParse: 167 lines / syntax: ios / comment delimiter: '!' / factory: False>


Now that I have a CiscoConfParse object, let's search for all of the config lines that start with the word 'interface'.

>>> rtr_interfaces = cisco_cfg.find_objects(r"^interface")
>>> rtr_interfaces
[<IOSCfgLine # 111 'interface FastEthernet0'>, <IOSCfgLine # 114 'interface FastEthernet1'>, <IOSCfgLine # 117 'interface FastEthernet2'>, <IOSCfgLine # 120 'interface FastEthernet3'>, <IOSCfgLine # 123 'interface FastEthernet4'>, <IOSCfgLine # 129 'interface Vlan1'>]

Notice, I now have a list of six elements matching the six interfaces in the configuration.



Now that I have all these interfaces--what if I want to look at the children of one of them:

>>> intf_fa4 = rtr_interfaces[4]
>>> intf_fa4
<IOSCfgLine # 123 'interface FastEthernet4'>
>>> 
>>> intf_fa4.children
[<IOSCfgLine # 124 ' description *** LAN connection (don't change) ***' (parent is # 123)>, <IOSCfgLine # 125 ' ip address 10.220.88.20 255.255.255.0' (parent is # 123)>, <IOSCfgLine # 126 ' duplex auto' (parent is # 123)>, <IOSCfgLine # 127 ' speed auto' (parent is # 123)>]


Since '.children' returns a list, I can also iterate over it. This will allow me to view the children in a cleaner way.

>>> for child in intf_fa4.children:
...   print child.text
... 
 description *** LAN connection (don't change) ***
 ip address 10.220.88.20 255.255.255.0
 duplex auto
 speed auto

So that is fairly nice...I could pretty easily search for lines beginning with 'interface' and then from this retrieve all of the child configuration elements.



You can also directly search for a combination of conditions. For example, what if I want to find the interfaces that have 'no ip address'.

>>> no_ip_address = cisco_cfg.find_objects_w_child(parentspec=r"^interface", childspec=r"no ip address")
>>> no_ip_address
[<IOSCfgLine # 111 'interface FastEthernet0'>, <IOSCfgLine # 114 'interface FastEthernet1'>, <IOSCfgLine # 117 'interface FastEthernet2'>, <IOSCfgLine # 120 'interface FastEthernet3'>, <IOSCfgLine # 129 'interface Vlan1'>]


I can then print out both the parents and children fairly easily:

>>> for my_int in no_ip_address:
...   print my_int.text
...   for child in my_int.children:
...     print child.text
... 
interface FastEthernet0
 no ip address
interface FastEthernet1
 no ip address
interface FastEthernet2
 no ip address
interface FastEthernet3
 no ip address
interface Vlan1
 no ip address



CiscoConfParse also has a search for find_objects_wo_child (i.e. without child). So what if I want to find all of the interfaces that do NOT have 'no ip address'.

>>> ip_configured = cisco_cfg.find_objects_wo_child(parentspec=r"^interface", childspec=r"no ip address")
>>> ip_configured
[<IOSCfgLine # 123 'interface FastEthernet4'>]



You can also directly look at child and parent relationships. For example, the 'cisco.txt' file that we loaded contains the following configuration (Note, I slightly modified this to hide the key-hash and email address):

ip ssh pubkey-chain
  username testuser
   key-hash ssh-rsa C0B699C6EAAAE18E9EC099B30F5D01DA invalid@domain.com


Now I can use the find_objects() method to find this configuration element:

>>> ssh_pubkey_chain = cisco_cfg.find_objects(r"^ip ssh pubkey")[0]
>>> ssh_pubkey_chain
<IOSCfgLine # 97 'ip ssh pubkey-chain'>


I can then check if it is a parent and if it is a child:

>>> ssh_pubkey_chain.is_parent
True
>>> ssh_pubkey_chain.is_child
False


I can find its direct children:

>>> ssh_pubkey_chain.children
[<IOSCfgLine # 98 '  username testuser' (parent is # 97)>]


I can find all of its children (note, from this that .children implies a direct child whereas .all_children implies both direct and indirect children).

>>> ssh_pubkey_chain.all_children
[<IOSCfgLine # 98 '  username testuser' (parent is # 97)>, <IOSCfgLine # 99 '   key-hash ssh-rsa C0B699C6EAAAE18E9EC099B30F5D01DA invalid@domain.com' (parent is # 98)>]


There are similar attributes that go the other way i.e. from children to parents (namely 'parent' and 'all_parents').



As you can see (hopefully), CiscoConfParse can help you parse Cisco and search through Cisco and Cisco-like configurations. It is also pretty simple to use.

For more information see:

ciscoconfparse on GitHub 
(http://t.dripemail2.com/c/eyJhY2NvdW50X2lkIjoiNDI1NDQ5NyIsImRlbGl2ZXJ5X2lkIjoiMjMxOTY2ODMzNiIsInVybCI6Imh0dHBzOi8vZ2l0aHViLmNvbS9tcGVubmluZy9jaXNjb2NvbmZwYXJzZT9fX3M9eG42bm82Zno3eXU2enJrb25kdmMifQ)

CiscoConfParse Tutorial
(http://t.dripemail2.com/c/eyJhY2NvdW50X2lkIjoiNDI1NDQ5NyIsImRlbGl2ZXJ5X2lkIjoiMjMxOTY2ODMzNiIsInVybCI6Imh0dHA6Ly93d3cucGVubmluZ3Rvbi5uZXQvcHkvY2lzY29jb25mcGFyc2UvdHV0b3JpYWwuaHRtbD9fX3M9eG42bm82Zno3eXU2enJrb25kdmMifQ)
