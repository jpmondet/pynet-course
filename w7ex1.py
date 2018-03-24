#! /usr/bin/env python3

"""
1a. Use Jinja2 templating to render the following:

vlan 
   name 


Your template should be inside of your Python program for simplicity.

The output from processing your template should be as follows. This should be printed to stdout.

vlan 400
   name red400

1b. Using a conditional in a Jinja2 template, generate the following output:

crypto isakmp policy 10
 encr aes
 authentication pre-share
 group 5
crypto isakmp key my_key address 1.1.1.1 no-xauth
crypto isakmp keepalive 10 periodic


The encryption of aes, and the Diffie-Hellman group should be variables in the template.

Additionally this entire ISAKMP section should only be added if the isakmp_enable variable is set to True.

Your template should be inside your Python program for simplicity.

1c. Using Jinja2 templating and a for-loop inside the template, generate the following configuration snippet:

vlan 501
   name blue501
vlan 502
   name blue502
vlan 503
   name blue503
vlan 504
   name blue504
vlan 505
   name blue505
vlan 506
   name blue506
vlan 507
   name blue507
vlan 508
   name blue508


Your template should be inside your Python program for simplicity.

It is fine for your VLAN IDs to be out of order in the generated configuration 
(for example, VLAN ID 508 can come before VLAN ID 504).
"""

from __future__ import print_function, unicode_literals
from jinja2 import Template


def vlan_rendering():
    tplte = Template("\
vlan {{ vlan_id }}\n \
    name {{ vlan_name }}")
    print(tplte.render(vlan_id="400", vlan_name="red400"))


def ipsec_conf_rendering():
    aes_encr = "aes"
    dh_grp = "5"
    isakmp_enable = True
    tplte = Template("""
{% if isakmp_enable %}
crypto isakmp policy 10
 encr {{ aes_encr }}
 authentication pre-share
 group {{ dh_grp }}
crypto isakmp key my_key address 1.1.1.1 no-xauth
crypto isakmp keepalive 10 periodic
{% endif %}
""")
    print(tplte.render(isakmp_enable=isakmp_enable, aes_encr=aes_encr, dh_grp=dh_grp))


def loop_vlan_rendering():
    tplte = Template("""
{% for i in range(8) -%}
vlan {{ i + 501 }}\n \
    name blue{{ i + 501 }}
{% endfor -%}
""")
    print(tplte.render())


def main():
    vlan_rendering()
    ipsec_conf_rendering()
    loop_vlan_rendering()


if __name__ == '__main__':
    main()
