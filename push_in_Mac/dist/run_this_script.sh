bash ~/Desktop/inventory_setup.sh

sudo cp ~/Desktop/inventory_update.plist /Library/LaunchAgents/
sudo chown root:wheel /Library/LaunchAgents/inventory_update.plist
sudo chmod 600 /Library/LaunchAgents/inventory_update.plist

sudo mv ~/Desktop/inventory_update.app /Users/Shared/
sudo chmod 755 /Users/Shared/inventory_update.app

launchctl load /Library/LaunchAgents/inventory_update.plist
launchctl list | grep csusb