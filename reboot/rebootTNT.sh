#!/bin/bash

echo rjanortiz | sudo screen -S TNT -p 0 -X stuff 'stop\n'
sleep 300
echo rjanortiz | sudo screen -S TNT -p 0 -X stuff './run.sh\n'
