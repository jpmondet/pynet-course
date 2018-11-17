So you have a brand new router and you want to fully automate the configuration process?


Now once the device is on the network, then you can use SSH or an API to programmatically configure it. But you still potentially need to minimally configure the device to safely add it onto the network. For example, disable the DHCP server, configure SSH, add a user, etc. The specifics will depend on the device. 

There are obviously "zero touch" ways to accomplish this like Cisco's POAP or Arista's ZTP.


But for a quick and easy solution--why can't you just programmatically configure the device via the console connection?


You can using pySerial.


Let's do some experimentation with this. First, I am working on an old Windows machine that has Python 2.7.6 installed. I also installed pySerial on this machine.


The first thing I need to do is establish a serial connection. After some experimentation I was able to do the following:

>>> import serial
>>>
>>> console = serial.Serial(
...         port='COM1',
...         baudrate=9600,
...         parity="N",
...         stopbits=1,
...         bytesize=8,
...         timeout=8
...
)



I can then verify that the serial port is open using the isOpen() method.

>>> console.isOpen()
​True



At this point, I need to write and read from the serial port and this is where it got a bit tricky. First, let's just send a newline down the channel (note, it is a Windows-style newline).

>>> console.write("\r\n")
2L



Now I use the inWaiting() method to see if there are any data bytes waiting to be read. inWaiting() will return the number of bytes that need to be read.

>>> console.inWaiting()
225L


Now there are 225 bytes ready to be read. Let's read them and display what we receive:

>>> input_data = console.read(225)
>>> print input_data

User Access Verification

Username:
% Username:  timeout expired!



There was more on the screen, but you get the picture.


As you can see we are able to send data to the serial port and read data from it. Now let's create a Python script and see if we can handle the login process. In order to do this, I will need to send a newline, wait for a second, and then read the data. If 'Username' is present in the input data, then I can proceed.

Here is a crude script to accomplish this:

import serial
import sys
import time
import credentials

READ_TIMEOUT = 8

def main():

    print "\nInitializing serial connection"

    console = serial.Serial(
        port='COM1',
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=READ_TIMEOUT
    )

    if not console.isOpen():
        sys.exit()

    console.write("\r\n\r\n")
    time.sleep(1)
    input_data = console.read(console.inWaiting())
    print input_data
    if 'Username' in input_data:
        console.write(credentials.username + '\r\n')
    time.sleep(1)
    input_data = console.read(console.inWaiting())

if __name__ == "__main__":
    main()



Note, I have stored the username and password in an external file called credentials.py and then import them.

At this point if I run the script I get:

$ python serial1.py

Initializing serial connection


User Access Verification

Username:



Note, I do not see 'Username:' consistently when I run this script. This is due to the behavior of the Cisco router (i.e. it will show 'Username:' three times and then it will delay for about 3 seconds and then it will show me a message that 'router_name con0 is now available').

Even with that problem let's proceed and try to send the password down the channel.

import serial
import sys
import time
import credentials

READ_TIMEOUT = 8

def main():

    print "\nInitializing serial connection"

    console = serial.Serial(
        port='COM1',
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=READ_TIMEOUT
    )

    if not console.isOpen():
        sys.exit()

    console.write("\r\n\r\n")
    time.sleep(1)
    input_data = console.read(console.inWaiting())
    if 'Username' in input_data:
        console.write(credentials.username + '\r\n')
    time.sleep(1)
    input_data = console.read(console.inWaiting())
    if 'Password' in input_data:
        console.write(credentials.password + '\r\n')
    time.sleep(1)
    input_data = console.read(console.inWaiting())
    print input_data


if __name__ == "__main__":
    main()



As you can see I now handle sending the password. If I run this script, I get the following:

$ python serial2.py

Initializing serial connection


pynet-rtr1>
pynet-rtr1>



We are now receiving the router prompt and are able to login successfully.

Now the script has some significant reliability issues, but you can see from the above that we are able to successfully interact with the router via its console port using Python.



Here is an expanded version of this program.


The script still is pretty rough, but it better handles some of the issues. I also had the script execute the command "show ip int brief" and return the output.

Here you can see the program being run:

$ python cisco_serial.py

Initializing serial connection
Logging into router
We are logged in

show ip int brief
Interface           IP-Address      OK? Method Status     Protocol
FastEthernet0       unassigned      YES unset  down       down
FastEthernet1       unassigned      YES unset  down       down
FastEthernet2       unassigned      YES unset  down       down
FastEthernet3       unassigned      YES unset  down       down
FastEthernet4       10.220.88.20    YES NVRAM  up         up
Vlan1               unassigned      YES unset  down       down
pynet-rtr1>
pynet-rtr1>
Logging out from router
Successfully logged out from router



Obviously, in order to send configuration changes--we would have to go into enable mode, then config mode, and then execute our changes. But these series of actions should not be too tough to accomplish.