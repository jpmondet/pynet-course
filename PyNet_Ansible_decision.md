Adding flow control and complex data structures into Ansible playbooks is difficult. You would like to be able to make decisions on information retrieved from network devices, but both the Ansible syntax and the Ansible keywords are difficult to use.

In this article, I will demonstrate an example of retrieving network information and making configuration decisions based upon this information. Here, I will retrieve 'show vlan' from four Arista switches. From this information, I will determine if VLAN999 exists and, if not, add it to the switches.


Now there are several ways we could accomplish this task. I am going to use the ntc-ansible modules. There is a nice feature in the ntc-ansible modules that allows me to retrieve show command output as structured data (using  TextFSM templates). By structured data, I mean the output is returned as some combination of lists and dictionaries as contrasted with returning a single string.


First, let's retrieve the 'show vlan' output:

# File ntc_show_simple.yml
--- 
- name: Obtain current Arista VLANs
  hosts: arista
  gather_facts: false
  tags: arista
  tasks:
    - name: show vlan
      ntc_show_command:
        host: "{{ host }}"
        username: "{{ username }}"
        password: "{{ password }}"
        platform: arista_eos
        command: 'show vlan'
      register: result

    - debug: var=result


The variables {{ host }}, {{ username }}, and {{ password }} are all defined in Ansible inventory. The 'arista' group consists of four Arista vEOS switches and is also defined in Ansible inventory.


When I execute this playbook, I receive the following output:

$ ansible-playbook ntc_show_simple.yml -i ./ansible-hosts 

PLAY [Obtain current Arista VLANs] *********************************************

TASK [show vlan] ***************************************************
ok: [pynet-sw4]
ok: [pynet-sw1]
ok: [pynet-sw3]
ok: [pynet-sw2]

TASK [debug] *******************************************************
ok: [pynet-sw1] => {
    "result": {
        "changed": false, 
        "response": [
            {
                "name": "default", 
                "status": "active", 
                "vlan_id": "1"
            }, 
            {
                "name": "BLUE", 
                "status": "active", 
                "vlan_id": "999"
            }
        ], 
        "response_list": []
    }
}
ok: [pynet-sw2] => {
    "result": {
        "changed": false, 
        "response": [
            {
                "name": "default", 
                "status": "active", 
                "vlan_id": "1"
            }
        ], 
        "response_list": []
    }
}
ok: [pynet-sw3] => {
    "result": {
        "changed": false, 
        "response": [
            {
                "name": "default", 
                "status": "active", 
                "vlan_id": "1"
            }, 
            {
                "name": "BLUE", 
                "status": "active", 
                "vlan_id": "999"
            }
        ], 
        "response_list": []
    }
}
ok: [pynet-sw4] => {
    "result": {
        "changed": false, 
        "response": [
            {
                "name": "default", 
                "status": "active", 
                "vlan_id": "1"
            }, 
            {
                "name": "BLUE", 
                "status": "active", 
                "vlan_id": "999"
            }
        ], 
        "response_list": []
    }
}

PLAY RECAP *********************************************************
pynet-sw1           : ok=2    changed=0    unreachable=0    failed=0
pynet-sw2           : ok=2    changed=0    unreachable=0    failed=0
pynet-sw3           : ok=2    changed=0    unreachable=0    failed=0
pynet-sw4           : ok=2    changed=0    unreachable=0    failed=0



The key thing to observe above is that the 'response' output is structured data.


Since we are able to retrieve structured data back, let's expand on this and see if we can add the logic to determine if VLAN999 exists. The first thing I want to do in this regard is to simplify the response output (now stored in the 'result' variable). Consequently, I expand my playbook to look as follows:

--- 
- name: Obtain current Arista VLANs
  hosts: arista
  gather_facts: false
  tags: arista
  tasks:
    - name: show vlan
      ntc_show_command:
        host: "{{ host }}"
        username: "{{ username }}"
        password: "{{ password }}"
        platform: arista_eos
        command: 'show vlan'
      register: result
 
    - name: Save vlan_output
      set_fact:
        vlan_out: "{{ result.response }}"  



I am still receiving the 'show vlan' output and assigning it into a variable named 'result'. I am then grabbing the 'response' field from this output and assigning it to the 'vlan_out' variable.


Now I want to create a 'vlan_999' variable based on this output. First I set the 'vlan_999' variable to an initial value of false.

    - name: vlan_999 initial value
      set_fact:
        vlan_999: false


Next, I parse the 'vlan_out' output and determine if VLAN999 already exists. I accomplish this using the following task:

    - name: Set vlan_999 
      set_fact:
        vlan_999: true
      with_items: "{{ vlan_out }}"
      when: item.vlan_id == "999"
    - debug: var=vlan_999 


This task combines both a for loop (with_items) and a conditional (when). Translated into Python, the logic of this task is:

for item in vlan_out:
    if item['vlan_id'] == '999':
        vlan_999 = True


In other words, for each of the four Arista switches, go through the 'vlan_out' output, find the 'vlan_id' field and test if this vlan_id is '999'. If you find VLAN999 (for a given Arista switch), then assign the vlan_999 variable to be true.

At the end of this, each Arista switch will have a 'vlan_999' variable that should reflect whether the switch has VLAN999 or not.


Here is the output of my playbook at this point (for the vlan_999 variable):

TASK [debug] ********************************************************
ok: [pynet-sw1] => {
    "vlan_999": true
}
ok: [pynet-sw2] => {
    "vlan_999": false
}
ok: [pynet-sw3] => {
    "vlan_999": true
}
ok: [pynet-sw4] => {
    "vlan_999": true
}

 
The key thing to observe at this point is that all of the switches except pynet-sw2 have VLAN999.


I can now take configuration actions based upon the vlan_999 variable.

    - name: Create Vlan 999   
      ntc_config_command:
        host: "{{ host }}"
        username: "{{ username }}"
        password: "{{ password }}"
        platform: arista_eos
        commands: 
          - 'vlan 999'
          - 'name BLUE'
      when: vlan_999 == false
      register: result  


This task uses the ntc_config_command module to create VLAN999 and to name it BLUE.

Once again I used an Ansible conditional (when), and I also saved this output to a variable named "result".


The full playbook looks as follows:

--- 
- name: Obtain current Arista VLANs
  hosts: arista
  gather_facts: false
  tags: arista
  tasks:
    - name: show vlan
      ntc_show_command:
        host: "{{ host }}"
        username: "{{ username }}"
        password: "{{ password }}"
        platform: arista_eos
        command: 'show vlan'
      register: result

    - name: Save vlan_output
      set_fact:
        vlan_out: "{{ result.response }}"

    - name: vlan_999 initial value
      set_fact:
        vlan_999: false

    - name: Set vlan_999
      set_fact:
        vlan_999: true
      with_items: "{{ vlan_out }}"
      when: item.vlan_id == "999"

    - name: Create Vlan 999
      ntc_config_command:
        host: "{{ host }}"
        username: "{{ username }}"
        password: "{{ password }}"
        platform: arista_eos
        commands: 
          - 'vlan 999'
          - 'name BLUE'
      when: vlan_999 == false
      register: result

    - debug: var=result  



Execution of the playbook yields:

$ ansible-playbook vlan_test.yml -i ./ansible-hosts 

PLAY [Obtain current Arista VLANs] *********************************

TASK [show vlan] ***************************************************
ok: [pynet-sw4]
ok: [pynet-sw3]
ok: [pynet-sw2]
ok: [pynet-sw1]

TASK [Save vlan_output] ********************************************
ok: [pynet-sw1]
ok: [pynet-sw2]
ok: [pynet-sw3]
ok: [pynet-sw4]

TASK [vlan_999 initial value] **************************************
ok: [pynet-sw1]
ok: [pynet-sw2]
ok: [pynet-sw3]
ok: [pynet-sw4]

TASK [Set vlan_999] ************************************************
skipping: [pynet-sw1] =>
(item={u'status': u'active', u'name': u'default', u'vlan_id': u'1'}) 
skipping: [pynet-sw2] =>
(item={u'status': u'active', u'name': u'default', u'vlan_id': u'1'}) 
skipping: [pynet-sw3] =>
(item={u'status': u'active', u'name': u'default', u'vlan_id': u'1'}) 
ok: [pynet-sw1] =>
(item={u'status': u'active', u'name': u'BLUE', u'vlan_id': u'999'})
skipping: [pynet-sw4] =>
(item={u'status': u'active', u'name': u'default', u'vlan_id': u'1'}) 
ok: [pynet-sw3] =>
(item={u'status': u'active', u'name': u'BLUE', u'vlan_id': u'999'})
ok: [pynet-sw4] =>
(item={u'status': u'active', u'name': u'BLUE', u'vlan_id': u'999'})

TASK [Create Vlan 999] *********************************************
skipping: [pynet-sw1]
skipping: [pynet-sw3]
skipping: [pynet-sw4]
changed: [pynet-sw2]

TASK [debug] *******************************************************
ok: [pynet-sw1] => {
    "result": {
        "changed": false, 
        "skip_reason": "Conditional check failed", 
        "skipped": true
    }
}
ok: [pynet-sw2] => {
    "result": {
        "changed": true, 
        "response": "config term\npynet-sw2(config)#vlan 999\nname BLUE\npynet-sw2(config-vlan-999)#name BLUE\npynet-sw2(config-vlan-999)#end\npynet-sw2#"
    }
}
ok: [pynet-sw3] => {
    "result": {
        "changed": false, 
        "skip_reason": "Conditional check failed", 
        "skipped": true
    }
}
ok: [pynet-sw4] => {
    "result": {
        "changed": false, 
        "skip_reason": "Conditional check failed", 
        "skipped": true
    }
}

PLAY RECAP *********************************************************
pynet-sw1           : ok=5    changed=0    unreachable=0    failed=0
pynet-sw2           : ok=5    changed=1    unreachable=0    failed=0
pynet-sw3           : ok=5    changed=0    unreachable=0    failed=0
pynet-sw4           : ok=5    changed=0    unreachable=0    failed=0



You can see from the above that VLA999 was configured on arista-sw2.


I can also verify this manually on the switch.

pynet-sw2#show vlan
VLAN  Name          Status    Ports
----- ------------- --------- -------------------------------
1     default       active    Cpu, Et1, Et2, Et3, Et4, Et5
                              Et6, Et7
999   BLUE          active   




NTC-ansible is an open-source library with a lot of contributions from Jason Edelman, Michael Ben-Ami, and Gabriele Gerbino.

For the two modules that I used in this article (ntc_show_command and ntc_config_command), Netmiko is used by default.

Note, this example is slightly contrived as you could probably accomplish the VLAN configuration in an idempotent manner just using a configuration operation (i.e. without directly executing any show commands in your playbook). While it is slightly contrived the patterns used are very common patterns in Ansible Network Automation.

