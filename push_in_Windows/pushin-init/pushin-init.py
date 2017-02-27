#!/usr/bin/python
# First Time Running
import requests # php
import os		# hostname
import re, uuid # mac address
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

# Convert bytes to GB
def bytes2human(n):
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.1f%s' % (value, s)
	return "%sB" % n

# Get manual input
tag = raw_input("Input tag number(5): ")

building = raw_input("Input building(2): ")

room = raw_input("Input room number: ")

purpose = raw_input("Input purpose(Faculty Name, Lab, etc): ")

# Get auto input
value = {}

value["Hostname"] = os.environ['COMPUTERNAME']
print "Hostname Collected: " + value["Hostname"]
value["IP"] = socket.gethostbyname(socket.gethostname())
print "IP Address Collected: " + value["IP"]
value["Mac"] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
print "MAC Address Collected: " + value["Mac"]
value["Active"] = "1"
value["OS"] = SysInfo("OS Name")
print "Operating System Name Collected: " + value["OS"]

# SysInfo
value["TotalMemory"] = SysInfo("Total Physical Memory")
print "Total Memory Collected: " + value["TotalMemory"]
value["AvailableMemory"] = SysInfo("Available Physical Memory")
print "Available Memory Collected: " + value["AvailableMemory"]
value["SysModel"] = SysInfo("System Model")
print "System Model Collected: " + value["SysModel"]
# Hard-drive Information
usage = psutil.disk_usage('/')
value["HD-Total"] = bytes2human(usage.total)
print "Hard-drive Total size Collected: " + value["HD-Total"]
value["HD-Percent"] = usage.percent
print "Hard-drive Usage Collectd: %d" % (value["HD-Percent"])
# Serial Number
process = os.popen('wmic bios get serialnumber')
value["Serial"] = process.read()
print "Serial Number Collected: " + value["Serial"]
# Write Log
logging.basicConfig(filename='./Inventory_log.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('Hostname = %s, IP = %s, Mac = %s, OS = %s, TotalMemory = %s, AvailableMemory = %s, SysManufacturer = %s, HD-Total = %s, Serial = %s, Tag = %s, Building = %s, Room = %s, Purpose = %s', value["Hostname"], value["IP"], value["Mac"], value["OS"],value["TotalMemory"], value["AvailableMemory"], value["SysModel"], value["HD-Total"], value["Serial"], tag, building, room, purpose)
print "Finished Writing a Log"
# Send data
r = requests.post("https://caltech.csusb.edu/ip/include/add_inventory.php", data = {'tag': tag, 'building': building, 'room': room, 'purpose': purpose, 'hostname': value["Hostname"], 'ip': value["IP"], 'mac': value["Mac"], 'Active': value["Active"], 'os': value["OS"], 'TotalMemory': value["TotalMemory"], 'AvailableMemory': value["AvailableMemory"], 'SysModel': value["SysModel"], 'HD-Total': value["HD-Total"], 'HD-Percent': value["HD-Percent"], 'serial': value["Serial"]}, verify = False )
print(r.text)
# Verify output
print (r.json)
print (r.content)
freeze = raw_input("Press Enter to Exit")
