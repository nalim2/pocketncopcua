# pocketncopcua

Configfile for the default deployment over pycharm

- Create a shell script such as sudo nano /usr/bin/opcuaserver.sh:

		#!/bin/bash

		# start the python programm with sudo because of deployment config
		sudo python /tmp/pycharm_project_pocketnc/main.py 

Make the script executabel:
		sudo chmod +x /usr/bin/opcuaserver.sh

Note that the first line is critical.

- Create a service file in  /lib/systemd/opcserver.service such as:

		[Unit]
		DescriptionPPocketNC OPC UA Server

		[Service]
		Type=simple
		ExecStart=/usr/bin/opcuaserver.sh

		[Install]
		WantedBy=multi-user.target
	
- Create a symbolic link between your script and a special location under /etc:

		ln -s /lib/systemd/opcserver.service /etc/systemd/system/opcserver.service
	
- Make systemd aware of your new service

		systemctl daemon-reload
		systemctl enable opcserver.service
		systemctl start opcserver.service

- Reboot the BeagleBone Black to see your script in action

- If you wish to control the service at runtime, you can use systemctl commands:	

		systemctl status opcserver.service
		systemctl stop opcserver.service
		systemctl start opcserver.service
		systemctl disable opcserver.service
