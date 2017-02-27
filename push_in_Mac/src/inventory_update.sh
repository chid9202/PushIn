echo $('date') >> /Users/Shared/$('whoami')_log_inv.txt

curl --request POST 'https://caltech.csusb.edu/ip/include/update_inventory.php'  --data "hostname=$(hostname -s)&ip=$(ifconfig en0 | awk '$1 == "inet" {print $2}')&mac=$(ifconfig en0 | awk '$1 == "ether" {print $2}')&AvailableMemory=$(top -l 1 -s 0 | grep PhysMem | awk '$1=="PhysMem:"{print $6}')&HD-Percent=(df -h | awk 'NR==2 {print $5}')" >> /Users/Shared/$('whoami')_log_inv.txt
