#!/bin/bash

echo rjanortiz | sudo screen -S MMC -p 0 -X stuff 'stop\n'
sleep 5
echo rjanortiz | sudo screen -S MMC -p 0 -X stuff './run.sh\n'
