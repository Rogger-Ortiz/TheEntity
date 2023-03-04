#!/bin/bash
cp ~/WIP/entity/backup.py ~/boot/NTT/entity.py

echo rjanortiz | sudo screen -S NTT -p 0 -X stuff '^C\n'
echo rjanortiz | sudo screen -S NTT -p 0 -X stuff 'python3 entity.py\n'
