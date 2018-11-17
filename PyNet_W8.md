
CLASS OUTLINE

1. Importing Libraries (VIDEO1)
   A. import re   [00:04]
   B. re.__file__   (where is the library)   [00:34]
   C. How using 'import' affects the namespace   [2:19]
   D. from re import search   [3:08]
   E. How using 'from' affects the namespace   [3:47]

2. sys.path and PYTHONPATH (VIDEO2)
   A. Where is Python looking   [00:30]
   B. sys.path   [1:02]
   C. PYTHONPATH   [2:30]
   D. Example of a failure   [4:27]

3. Pip (VIDEO3)
   A. How to install libraries   [00:01]
      1. pip install netmiko   [00:21]
      2. pip install netmiko==2.1.0   [1:26]
      3. pip uninstall netmiko   [1:53]
      4. pip install --upgrade netmiko   [2:13]
      5. pip list   [3:01]
      6. pip installing from git repo   [3:19]

4. Virtual Environments (VIDEO4)
   A. Virtual environment options   [00:28]
   B. Activating the virtual environment   [00:47]
   C. pip list on a new clean virtual environment   [2:33]
   D. Deactivate   [5:03]

5. Simple Python Module (VIDEO5)
   A. Creating your own module   [00:06]
   B. Define devices and importing them   [1:29]




    Importing Libraries
    Video link https://vimeo.com/259422351
    Length is 5 minutes
     
    sys.path and PYTHONPATH
    Video link https://vimeo.com/259423316
    Length is 7 minutes
     
    pip
    Video link https://vimeo.com/259424573
    Length is 7 minutes
     
    Virtual Environments
    Video link https://vimeo.com/259426537
    Length is 6 minutes
     
    Creating a Simple Python Module
    Video link https://vimeo.com/259427586
    Length is 4 minutes





Additional Content:

A non-magical introduction to Pip and Virtualenv for Python beginners​

Common Python Tools: Using virtualenv, Installing with Pip, and Managing Packages​
Read the "Using pip" section.

 



Exercises

Reference code for these exercises is posted on GitHub at:
https://github.com/ktbyers/pynet/tree/master/learning_python/lesson8



1a. Import the 'datetime' library. Print out the module that is being imported by datetime (the __file__ attribute)

Import the Python ipaddress library. Print out the module that is being imported by ipaddress (the __file__ attribute). If you are using Python 2.7, you will need to pip install the ipaddress library.

Import sys and use pprint to pprint sys.path


1b. In a separate Python file named 'my_devices.py', define a dictionary named 'rtr1' with the following key-value pairs:

host = rtr1.domain.com
username = cisco
password = cisco123
device_type = cisco_ios


Import my_devices into this program, and print the rtr1 dictionary to the screen using pprint.


1c. In a Python shell, try importing the 'my_devices' when my_devices.py is not in your current working directory.

What exception do you get when you do this?

Update your PYTHONPATH environment variable so that you are successfully able to import this module.


2a. Create a new virtual environment on your system named 'test_venv'.

b. Activate the virtual environment

c. Use 'which python' to see the path of the Python that you are using.

d. Use 'pip list' to see the packages you have installed.

e. Use pip to install Netmiko and the requests library.

f. Use 'pip list' to see the updated list of installed packages.


3a. Using the same 'test_venv' that you created in exercise2, install netmiko version 2.0.1. Verify that this version is installed by executing the following from the Python shell:

>>> import netmiko
>>> netmiko.__version__
'2.0.1'


b. Using pip, upgrade your version of Netmiko to the latest version.

c. Deactivate your virtual environment. See 'which python' is now being used.


4a. Activate your 'test_venv' virtual environment.

b. Use pip to uninstall the Netmiko library.

c. Verify that Netmiko is no longer installed.

d. Use pip to install the 'develop' branch of Netmiko.




