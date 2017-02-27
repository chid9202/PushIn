#!/bin/bash

#<----------------MAUNAL INPUTS---------------->
#TAKE TAG NUMBER
echo "Input tag number(5): "
read TAG

#TAKE BUILDING
echo "Input building(2): "
read BUILDING

#TAKE ROOM NUMBER
echo "Input room number: "
read ROOM

#TAKE PURPOSE
echo "Input purpose(Faculty, Name, Lab, etc): "
read PURPOSE

echo -e "Tag number:\t" $TAG
echo -e "Location:\t" $BUILDING$ROOM
echo -e "Purpose:\t" $PURPOSE

#<----------------AUTOMATED INPUTS---------------->
#1. TAKE HOSTNAME
HOSTNAME=$(hostname -s)
echo "1. PRINT HOSTNAME: $HOSTNAME"

#2. TAKE IP ADDRESS
IP=$(ifconfig en0 | awk '$1 == "inet" {print $2}')
echo "2. PRINT IP ADDRESS: $IP"

#3. TAKE MAC ADDRESS
MAC=$(ifconfig en0 | awk '$1 == "ether" {print $2}')
echo "3. PRINT MAC ADDRESS: $MAC"

#4. SET ACTIVE TO 1
ACTIVE="1"
echo "4. PRINT ACTIVE: $ACTIVE"

#5. TAKE OPERATING SYSTEM
OS=$(system_profiler SPSoftwareDataType | awk '$1 == "System" && $2 == "Version:" {print $3" "$4" "$5" "$6}')
echo "5. PRINT OS VERISON: $OS"

#6. TAKE TOTAL MEMORY
TOTALMEM=$(system_profiler SPHardwareDataType | awk '$1 == "Memory:" {print $2" "$3}')
echo "6. PRINT TOTAL MEMORY: $TOTALMEM"

#7. TAKE AVAILABLE MEMORY
AVAILABLEMEM=$(top -l 1 -s 0 | awk '/PhysMem/ || $1=="PhysMem:"{print $10}')
echo "7. PRINT AVAILABLE MEMORY: $AVAILABLEMEM"

#8. TAKE SYSTEM MODEL
SYSMODEL=$(system_profiler SPHardwareDataType | awk '$1=="Model" && $2=="Identifier:" {print $3}')
echo "8. PRINT SYSTEM MODEL: $SYSMODEL"

#9. TAKE TOTAL HARD DRIVE SIZE
TOTALHD=$(df -h | awk 'NR==2 {print $2}')
echo "9. PRINT TOTAL HARD DRIVE: $TOTALHD"

#10. TAKE AVAILABLE HARD DRIVE PERCENT
PERCENTHD=$(df -h | awk 'NR==2 {print $5}')
echo "10. PRINT PERCENT OF AVAILEABLE HARD DRIVE: $PERCENTHD"

#11. TAKE SERIAL NUMBER
SERIAL=$(system_profiler SPHardwareDataType | awk '$1=="Serial" {print $4}')
echo "11. PRINT SERIAL NUMBER: $SERIAL"

# Send a rquest to the php server
curl --request POST 'https://cal.csusb.edu/ip/include/add_inventory.php'  --data "tag=$TAG&building=$BUILDING&room=$ROOM&purpose=$PURPOSE&hostname=$HOSTNAME&ip=$IP&mac=$MAC&active=$ACTIVE&os=$OS&TotalMemory=$TOTALMEM&AvailableMemory=$AVAILABLEMEM&SysModel=$SYSMODEL&HD-Total=$TOTALHD&HD-Percent=$PERCENTHD&serial=$SERIAL"