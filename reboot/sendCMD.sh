#!/bin/bash

if [ "$1" = "NTT" ]; then
	echo rjanortiz | sudo screen -S CMD -p 0 -X stuff 'cd ~/boot/NTT/reboot\n'
	echo rjanortiz | sudo screen -S CMD -p 0 -X stuff './rebootNTT.sh\n'
fi

if [ "$1" = "TNT" ]; then
	echo rjanortiz | sudo screen -S TNT -p 0 -X stuff 'stop\n'
	sleep 15
	echo rjanortiz | sudo screen -S TNT -p 0 -X stuff './run.sh\n'
fi

if [ "$1" = "MMC" ]; then
	echo rjanortiz | sudo screen -S MMC -p 0 -X stuff 'stop\n'
	sleep 5
	echo rjanortiz | sudo screen -S MMC -p 0 -X stuff './run.sh\n'
fi
