PyNet_Ansible_lbl.md

Ansible added a new set of networking modules into Ansible-core in Ansible 2.1 (May 2016).

These new networking modules support a set of platforms: Junos, Arista EOS, Cisco Nexus, Cisco IOS-XR, and Cisco IOS. For each platform, there are three distinct modules: _command, _config, and _template. Consequently, Junos has a junos_config, junos_command, and junos_template module. Likewise, Cisco IOS has an ios_config, ios_command, and ios_template module.

At a high-level the three module types allow you to accomplish the following:

    _command: execute a command(s) and retrieve the output from a remote device. This information could be used to make decisions in the playbook.
     
    _config: execute a config change on the remote device.
     
    _template: push config changes to the remote device generally from a file or from a template.




In this article, I am going to detail capabilities provided by the new "config" modules. These modules provide a valuable Ansible-feature to network engineers namely line-by-line configuration editing with an understanding of config hierarchy.

The other two module types (command and template) are not all that significant in my opinion. In particular, the functionality provided by the template module is better served by NAPALM (possibly coupled with Ansible's standard template module). NAPALM provides a better set of abstractions for performing config file operations on networking devices (disclaimer, I work on the NAPALM project).



In my lab environment, I have a Cisco IOS router. I also have an AWS server with Ansible2 installed (this was from the Ansible 'devel' branch as of March 2016).

My Ansible inventory has the following:

[local]
localhost ansible_connection=local

[cisco]
pynet-rtr1 host=10.10.10.27 port=22 username=admin password=pwd

[cisco:vars]
ansible_python_interpreter=~/VENV/ansible2/bin/python
ansible_connection=local



Since I am using Cisco IOS, I will be using the ios_config module. Here is the initial playbook that I started with:

--- 
- name: Test Cisco IOS line-by-line editing
  gather_facts: no
  hosts: cisco

  vars:
    creds:  
        host: "{{ host }}"
        username: "{{ username }}"
        password: "{{ password }}"

  tasks:
    - ios_config:
        provider: "{{ creds }}"
        lines: 
           - logging buffered 19000
           - no logging console
        match: line 



This playbook will operate on the 'cisco' group which as defined in the inventory file and is a single Cisco IOS router (pynet-rtr1). The 'vars' section of the playbook defines a dictionary named 'creds' which basically consolidates the ip address (host), username, and password in a single variable. This information is pulled from the Ansible inventory file.

In the next section, I use the ios_config module with the provider, lines, and match arguments. Provider allows the ip address, username, and password to be passed in as a single variable. The lines argument specifies the configuration elements that must exist on the device.

Match is the final argument. It allows three possible values--'line', 'strict', and 'exact'. Line is the most basic matching. Basically these lines must exist in the config and the order doesn't matter. Note, there is the possibility of qualifying this with a parent which I will discuss below.

What does the above playbook do when executed? Basically, Ansible will SSH to the network device, retrieve the current running configuration, and check whether the two configuration lines exist. If they aren't in the configuration, they will be added. If they are in the config, then no changes will be made. Note, there is a bit more subtlety depending on the parent argument which I will detail shortly. 

Currently the router has the following config:

pynet-rtr1#show run | inc logging
logging buffered 20000
no logging console
pynet-rtr1#



Now, I execute the playbook:

$ ansible-playbook -i ./ansible-hosts ios_test_config.yml

PLAY [Test Cisco IOS line-by-line editing] *******************

TASK [ios_config] ********************************************
changed: [pynet-rtr1]

PLAY RECAP ***************************************************
​​​​​​​pynet-rtr1       : ok=1    changed=1    unreachable=0    failed=0   


And back on the router I now have:

pynet-rtr1#show run | inc logging
logging buffered 19000
no logging console
pynet-rtr1#



If I run the playbook again, Ansible detects that no changes need to be made.



Now let's do something a bit more interesting and try to add a VLAN interface to the router. I update the playbook and append the following to the end of it (the initial task is still present).

    - name: Add interface vlan127 to the config 
      ios_config:
        provider: "{{ creds }}"
        lines:
          - ip address 192.168.127.1 255.255.255.0
          - no ip proxy-arp
        parents: ['interface Vlan127']
        match: line 


Here I have added a new argument 'parents'. Parents specifies a configuration context that the lines must exist inside of. In other words, the two lines must exist inside of the interface Vlan127 section. If no parents are specified, then the configuration context is the global config.

At this point, interface Vlan127 doesn't exist on the router:

pynet-rtr1#show ip int brief
Interface         IP-Address      OK? Method Status       Protocol
FastEthernet0     unassigned      YES unset  down         down    
FastEthernet1     unassigned      YES unset  down         down    
FastEthernet2     unassigned      YES unset  down         down    
FastEthernet3     unassigned      YES unset  down         down    
FastEthernet4     10.220.88.20    YES NVRAM  up           up      
Vlan1             unassigned      YES unset  down         down    



Now I run the playbook and observe the following:

$ ansible-playbook -i ./ansible-hosts ios_test_config.yml

PLAY [Test Cisco IOS line-by-line editing] *******************

TASK [ios_config] ********************************************
ok: [pynet-rtr1]

TASK [Add interface vlan127 to the config] *******************
changed: [pynet-rtr1]

PLAY RECAP ***************************************************
pynet-rtr1        : ok=2    changed=1    unreachable=0    failed=0   


And back on the router:

pynet-rtr1#show ip int brief | inc 127
Vlan127         192.168.127.1   YES manual down  down

pynet-rtr1#show run int vlan 127
Building configuration...
Current configuration : 82 bytes
!
interface Vlan127
 ip address 192.168.127.1 255.255.255.0
 no ip proxy-arp
end




Now what about an ACL example where both hierarchy and order matter. First I add the following task to my playbook:


    - name: Add TEST1 ACL 
      ios_config:
        provider: "{{ creds }}"
        lines:
          - permit ip host 1.1.1.1 any log
          - permit ip host 2.2.2.2 any log
          - permit ip host 3.3.3.3 any log
          - permit ip host 4.4.4.4 any log
          - permit ip host 5.5.5.5 any log
        parents: ["ip access-list extended TEST1"]
        before: ["no ip access-list extended TEST1"]
        replace: block
        match: line 


Here I have the ACL lines in a specific order. Additionally, I have the parent that will create the access-list. Beneath the parents argument, is a new argument named 'before'. On any change operation the 'before' command will be executed. So in this example, if Ansible determines the ACL needs to be changed (or doesn't exist), then the before command will be executed. After the before command is executed, the ACL will be added.

Note, executing 'no ip access-list extended TEST1' does not generate an error (in the case where the ACL does not exist). If your 'before' command generated an error (when the element doesn't exist), then you would to add some additional logic to your playbook.

A couple of additional items to note about this playbook, 'replace: block' indicates to replace the entire configuration block (all the lines including the parents). In other words, do not try to determine individual lines that are missing from the ACL, always do all of the lines. Since the 'before' command removes the entire ACL, not doing 'replace: block' could result in a partial ACL being configured. Finally, I have once again specified 'match: line'. So for this task, Ansible will check that all of the ACL entries exist, but it will not care about their order.
 

$ ansible-playbook -i ./ansible-hosts ios_test_config.yml
PLAY [Test Cisco IOS line-by-line editing] *********************

TASK [ios_config] **********************************************
ok: [pynet-rtr1]

TASK [Add interface vlan127 to the config] *********************
ok: [pynet-rtr1]

TASK [Add TEST1 ACL] *******************************************
changed: [pynet-rtr1]

PLAY RECAP *****************************************************
pynet-rtr1          : ok=3    changed=1    unreachable=0    failed=0   



And now I have the ACL on the router:

pynet-rtr1#show access-lists TEST1
Extended IP access list TEST1
    10 permit ip host 1.1.1.1 any log
    20 permit ip host 2.2.2.2 any log
    30 permit ip host 3.3.3.3 any log
    40 permit ip host 4.4.4.4 any log
    50 permit ip host 5.5.5.5 any log




Let's make some small changes and see how 'match: exact' works. First, I am going to keep the same five ACL lines but reorder them.

I have manually reconfigured the TEST1 ACL to be the following:

pynet-rtr1#show access-lists TEST1
Extended IP access list TEST1
    10 permit ip host 5.5.5.5 any log
    20 permit ip host 2.2.2.2 any log
    30 permit ip host 3.3.3.3 any log
    40 permit ip host 4.4.4.4 any log
    50 permit ip host 1.1.1.1 any log


Re-running the exact same playbook--Ansible thinks nothing needs to change. This is because Ansible checks that the parent exists. It also checks all the children, but with 'match: line' Ansible doesn't care about the ACL order.

If we want to enforce the ACL order, then we need to use either 'match: strict' or 'match: exact'. Match strict will enforce the order of the elements, but it will not change the ACL in subset/superset situations. In our example, 'match: strict' would indicate the ACL was correct if TEST1 had the five lines in the correct order even if the ACL on the router had an additional ten lines.

Match exact on the other hand enforces not only order, but also that the elements specified are the only elements in the given context.

Note, there is a bug in the 'match: strict' code pertaining to the subset/superset behavior. Consequently, I am going to demonstrate 'match: exact' here. Additionally, I did not test the behavior of a multi-level hierarchy. In other words, how would children of children be handled.

In the playbook, I toggle the match condition to be match: exact and then re-execute the playbook.

 

Now Ansible makes a change and puts the correct ACL in place:

$ ansible-playbook -i ./ansible-hosts ios_test_config.yml

PLAY [Test Cisco IOS line-by-line editing] *********************

TASK [ios_config] **********************************************
ok: [pynet-rtr1]

TASK [Add interface vlan127 to the config] *********************
ok: [pynet-rtr1]

TASK [Add TEST1 ACL] *******************************************
changed: [pynet-rtr1]

PLAY RECAP *****************************************************
pynet-rtr1          : ok=3    changed=1    unreachable=0    failed=0   


And the router now has:

pynet-rtr1#show access-lists TEST1
Extended IP access list TEST1
    10 permit ip host 1.1.1.1 any log
    20 permit ip host 2.2.2.2 any log
    30 permit ip host 3.3.3.3 any log
    40 permit ip host 4.4.4.4 any log
    50 permit ip host 5.5.5.5 any log



And for one last test, let me manually expand the TEST1 ACL on the router to have some additional lines:

pynet-rtr1#show access-lists TEST1
Extended IP access list TEST1
    10 permit ip host 1.1.1.1 any log
    20 permit ip host 2.2.2.2 any log
    30 permit ip host 3.3.3.3 any log
    40 permit ip host 4.4.4.4 any log
    50 permit ip host 5.5.5.5 any log
    60 permit ip host 6.6.6.6 any log
    70 permit ip host 7.7.7.7 any log




Now, let me re-run the 'match: exact' playbook (with the five ACL lines) and see what happens:

$ ansible-playbook -i ./ansible-hosts ios_test_config.yml

PLAY [Test Cisco IOS line-by-line editing] *********************

TASK [ios_config] **********************************************
ok: [pynet-rtr1]

TASK [Add interface vlan127 to the config] *********************
ok: [pynet-rtr1]

TASK [Add TEST1 ACL] *******************************************
changed: [pynet-rtr1]

PLAY RECAP *****************************************************
pynet-rtr1          : ok=3    changed=1    unreachable=0    failed=0


pynet-rtr1#show access-lists TEST1
Extended IP access list TEST1
    10 permit ip host 1.1.1.1 any log
    20 permit ip host 2.2.2.2 any log
    30 permit ip host 3.3.3.3 any log
    40 permit ip host 4.4.4.4 any log
    50 permit ip host 5.5.5.5 any log


As expected the ACL is restored back to the five-line state.