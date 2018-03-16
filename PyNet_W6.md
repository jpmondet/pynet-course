CLASS OUTLINE

1. Netmiko Introduction and Basics (VIDEO1)
   A. Netmiko overview   [00:05]
      1. Alternate libraries   [00:36]
      2. Netmiko supported platforms   [1:00]
   B. Establishing a connection   [2:02]
      1. device_type   [3:35]
      2. Passing connection arguments using a dictionary   [5:00]
 
2. Netmiko Show Commands (VIDEO2)
   A. Using the .enable() method   [00:47]
   B. Executing show commands   [4:14]
      1. Command echo, trailing prompt are removed   [5:42]
      2. Executing multiple commands in sequence   [6:35]
   C. Changing the terminating search pattern   [7:48]
   D. Other platforms (Arista, Juniper)   [8:57]
      1. Convert to a loop structure   [10:26]
 
3. Netmiko and Prompting (VIDEO3)
   A. Multiline commands (i.e. additional prompting)   [00:36]
      1. Handling of additional prompting   [1:16]
   B. Commands that take longer than expected   [6:53]
      1. Using delay_factor   [9:13]
      2. Using global_delay_factor   [10:11]
 
4. Netmiko and TextFSM (VIDEO4)
   A. Integrating to TextFSM   [1:23]
      1. Using ntc-templates   [2:03]
      2. How to use TextFSM in Netmiko   [2:17]
      3. How Netmiko finds the templates   [4:20]
         a. Use 'git clone' for installation   [5:25]
      4. Listing of templates   [6:22]
      5. Using an environment variable   [7:34]
 
5. Netmiko and Config Changes (VIDEO5)
   A. Making configuration changes   [00:05]
      1. How to use send_config_set()   [1:28]
      2. Juniper commit() example   [2:39]
      3. Separate 'write memory' is required   [4:25]

6. Netmiko Troubleshooting (VIDEO6)
   A. Logging all reads and writes   [0:40]
   B. Using write_channel() and read_channel()   [3:50]
   C. Misc items   [6:55]
      1. Secure Copy   [6:59]
      2. Telnet and Serial support   [7:32]
      3. Terminal server   [8:19]


    Netmiko Introduction and Basics 
    Video link https://vimeo.com/254569911
    Length is 8 minutes
     
    Netmiko Show Commands
    Video link https://vimeo.com/254578980
    Length is 13 minutes
     
    Netmiko and Prompting
    Video link https://vimeo.com/254587832
    Length is 12 minutes
     
    Netmiko and TextFSM
    Video link https://vimeo.com/254611876
    Length is 10 minutes
     
    Netmiko Config Changes
    Video link https://vimeo.com/254614073
    Length is 8 minutes
     
    Netmiko Troubleshooting
    Video link https://vimeo.com/254786724
    Length is 9 minutes





Additional Content:

Netmiko Readme
(https://github.com/ktbyers/netmiko)

Netmiko Examples
(https://github.com/ktbyers/netmiko/tree/develop/examples)

Netmiko Tutorial
This tutorial is a bit old, but still should be generally correct.
(https://pynet.twb-tech.com/blog/automation/netmiko.html)


Exercises

Reference code for these exercises is posted on GitHub at:
    https://github.com/ktbyers/pynet/tree/master/learning_python/lesson6

Note, you will need some sort of a network device to work on these exercises. This can be a virtual or physical device. Make sure you are only working on test or lab devices.


1. Using Netmiko, establish a connection to a network device and print out the device's prompt.


2. Use send_command() to send a show command down the SSH channel. Retrieve the results and print the results to the screen.


3. Find a command on your device that has additional prompting. Use send_command_timing to send the command down the SSH channel. Capture the output and handle the additional prompting.


4. Use send_config_set() and send_config_from_file() to make configuration changes. 

The configuration changes should be benign. For example, on Cisco IOS I typically change the logging buffer size. 

As part of your program verify that the configuration change occurred properly. For example, use send_command() to execute 'show run' and verify the new configuration.


5. Optional, use send_command() in conjunction with ntc-templates to execute a show command. Have TextFSM automatically convert this show command output to structured data.


6. Optional, connect to three networking devices one after the other. Use send_command() to execute a show command on each of these devices. Print this output to the screen.





