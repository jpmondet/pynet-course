PyNet_ASA.md

Because of Cisco's recent IKE vulnerability, I have some Cisco ASAs that need upgraded. One of these ASAs is in my lab environment and I thought it would be interesting to upgrade this ASA programmatically.

This lab ASA is currently running an old operating system (*cough*, *cough*, 8.0(4)32...yes, I know it's old). In order to get started, I created a virtualenv on one of my AWS servers and then installed Netmiko 0.4.1. This AWS server has SSH access into the ASA.

Through a process of iterative testing, I wrote the following code (https://github.com/ktbyers/netmiko/blob/master/examples/asa_upgrade.py).

Let's look at this code in some more detail:

def main():
    """Script to upgrade a Cisco ASA."""
    ip_addr = raw_input("Enter ASA IP address: ")
    my_pass = getpass()
    start_time = datetime.now()

    net_device = {
        'device_type': 'cisco_asa',
        'ip': ip_addr,
        'username': 'admin',
        'password': my_pass,
        'secret': my_pass,
        'port': 22,
    } 

Here I prompt for an ip address and a password. I then create a dictionary representing the device's attributes.


This net_device dictionary is then passed into Netmiko and the SSH connection to the device is thus established (using the Netmiko ConnectHandler method). After that a few variables related to the program are initialized:

    print "\nLogging in to ASA"
    ssh_conn = ConnectHandler(**net_device)
    print

    dest_file_system = 'disk0:'
    source_file = 'test1.txt'
    dest_file = 'test1.txt'
    alt_dest_file = 'asa825-59-k8.bin'
    scp_changed = False 

Note, for testing purposes I used a much smaller file 'test1.txt'. This allowed me to test and debug the program much more rapidly. I did at one point transfer 'asa825-59-k8.bin' to the ASA using Python so it is already on the ASA.


Up until this point, I have mostly just initialized things. Now, let's start doing some work:



  with FileTransfer(ssh_conn, source_file=source_file,  

      dest_file=dest_file,

      file_system=dest_file_system) as scp_transfer:



    if not scp_transfer.check_file_exists():

      if not scp_transfer.verify_space_available():

        raise ValueError("Insufficient space available on remote device") 

Here I create a FileTransfer object named 'scp_transfer'. FileTransfer is a Netmiko class that I created to demonstrate secure copy on Cisco IOS devices (https://pynet.twb-tech.com/blog/automation/cisco-ios.html). It also works, however, on Cisco ASAs.

What does the FileTranfer class do? It uses secure copy to transfer a file to the remote device. It accomplishes this by creating two channels—an SSH control channel and a SCP channel to transfer the file. Additionally, FileTransfer has methods that allow you to perform verifications. As you can see above, I use 'check_file_exists()' and 'verify_space_available()' to determine whether the file already exists and whether there is sufficient space available.


Now I am ready to do the file transfer. First, I call a small function that uses Netmiko to enable SCP on the ASA. I then transfer the file. Finally, I use the same function to disable SCP on the ASA.

            print "Enabling SCP"
            output = asa_scp_handler(ssh_conn, mode='enable')
            print output
            print "\nTransferring file\n"
            scp_transfer.transfer_file()

            print "Disabling SCP"
            output = asa_scp_handler(ssh_conn, mode='disable')
            print output


At this point, I just need to verify that the file is correct. Consequently, I call the "verify_file()" method which performs an MD5 comparison on the files. 

  print "\nVerifying file"
  if scp_transfer.verify_file():
      print "Source and destination MD5 matches"
  else:
      raise ValueError("MD5 failure between source and destination files") 

 

I now know the file is on the ASA and that the MD5 matches. Consequently, I can configure the 'boot system' command and then verify the boot variable is correct.

After, I do this verification, I then need to save the config and reload the ASA. Once again, I use Netmiko to accomplish this.

Note, when testing this program I manually verified the boot variable before sending the 'wr mem' and 'reload' commands. In other words, the program needs additional logic that verifies the boot variable. The program also should have additional sanity checks on the remote file (to prevent against cases where you specify the wrong source file).
 
    print "\nSending boot commands"
    full_file_name = "{}/{}".format(dest_file_system, alt_dest_file)
    boot_cmd = 'boot system {}'.format(full_file_name)
    output = ssh_conn.send_config_set([boot_cmd])
    print output


    print "\nVerifying state"
    output = ssh_conn.send_command('show boot')
    print output


    print "\nWrite mem and reload"
    output = ssh_conn.send_command_expect('write mem')
    output += ssh_conn.send_command('reload')
    output += ssh_conn.send_command('y')
    print output


    print "\n>>>> {}".format(datetime.now() - start_time)
    print



What does this script look like when it executes:

Enter ASA IP address: 10.10.10.26
Password: 
>>>> 2016-03-23 10:21:55.579044

Logging in to ASA

Enabling SCP
config term 
twb-py-lab(config)# ssh scopy enable
twb-py-lab(config)# end
twb-py-lab# 

Transferring file

Disabling SCP
config term
twb-py-lab(config)# no ssh scopy enable
twb-py-lab(config)# end
twb-py-lab# 

Verifying file
Source and destination MD5 matches

Sending boot commands
config term
twb-py-lab(config)# boot system disk0:/asa825-59-k8.bin
twb-py-lab(config)# end
twb-py-lab# 

Verifying state

BOOT variable = 
Current BOOT variable = disk0:/asa825-59-k8.bin
CONFIG_FILE variable = 
Current CONFIG_FILE variable = 

Write mem and reload
Building configuration...
Cryptochecksum: feefe731 960a78a8 1c1217e0 553b57fe 

8983 bytes copied in 1.310 secs (8983 bytes/sec)
[OK]Proceed with reload? [confirm] twb-py-lab# 
twb-py-lab#  


***
*** --- START GRACEFUL SHUTDOWN ---
Shutting down isakmp
Shutting down File system



***
*** --- SHUTDOWN NOW ---


>>>> 0:00:23.222710 

You can see above that the code took a bit over 23 seconds to execute. As I mentioned earlier this execution only transferred a small text file and didn't actually transfer the ASA image file (which was transferred earlier).

After the reload the ASA was running the new OS. I verified this and performed a before-after diff on the config using some other tools.
 

Now just for grins let's see how long it takes to secure copy the actual ASA image file. Here, I modify the following variables:

    #source_file = 'test1.txt'
    source_file = 'asa825-59-k8.bin'
    dest_file = 'asa-newimage.bin' 

I also commented out the code pertaining to configuring 'boot system' and executing 'write mem' and 'reload' (as the ASA is already running the new image).

Enter ASA IP address: 50.76.53.26
Password: 
>>>> 2016-03-23 15:34:30.179171

Logging in to ASA

Enabling SCP
config term
twb-py-lab(config)# ssh scopy enable
twb-py-lab(config)# end
twb-py-lab# 

Transferring file

Disabling SCP
config term
twb-py-lab(config)# no ssh scopy enable
twb-py-lab(config)# end
twb-py-lab# 

Verifying file
Source and destination MD5 matches

>>>> 0:08:59.881756 

As you can see the transfer took about nine minutes and the file is now on the device:

twb-py-lab# dir disk0:/asa-newimage.bin

Directory of disk0:/asa-newimage.bin

135    -rwx  15482880    14:55:23 Mar 23 2016  asa-newimage.bin 

 

The ASA is obviously very slow to transfer a 15MB file, but this is an ASA problem (i.e. it would also be slow if I transferred the file manually).

Because of this slowness, however, I would probably decouple the file transfer operation from the final verifications, boot system, and reload. In other words, I would split the program into two separate parts, one part that handled the initial image transfer, and the second part that completed the upgrade including the reload.
