#!/usr/bin/python
# After First Time Running
import requests # php
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os		# hostname
import uuid # mac address
import socket	# ip address
import re 		# System manufactor, Memory
import psutil  	# Hard-drive
import logging	# Logging

# Import cpuinfo  # cpu - not compatible with py2exe

# Return System Information
def SysInfo(opt):
	values  = {}
	cache   = os.popen2("SYSTEMINFO")
	source  = cache[1].read()
    #sysOpts = ["OS Name", "OS Version", "System Manufacturer", "System Model", "Domain", "Total Physical Memory", "Available Physical Memory"]
	sysOpts = [opt]

	values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]
    #return values["OS Name"]
	return values[opt]

# return true if the log file exists = It's not first time running
value = {}

value["Hostname"] = os.environ['COMPUTERNAME']

value["IP"] = socket.gethostbyname(socket.gethostname())

value["Mac"] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

value["AvailableMemory"] = SysInfo("Available Physical Memory")

usage = psutil.disk_usage('/')

value["HD-Percent"] = usage.percent

logging.basicConfig(filename='./Inventory_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

logging.info('IP = %s, Mac = %s, AvailableMemory = %s, HD-Percent = %s', value["IP"], value["Mac"], value["AvailableMemory"], value["HD-Percent"])

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
r = requests.post("https://caltech.csusb.edu/ip/include/update_inventory.php", data = {'hostname': value["Hostname"], 'ip': value["IP"], 'mac': value["Mac"], 'AvailableMemory': value["AvailableMemory"], 'HD-Percent': value["HD-Percent"]}, verify = False )
