#!/bin/bash

# Rewrite the backup for last update
cp ~/boot/NTT/entity.py backup.py
cp -r  ~/WIP/entity/reboot ~/boot/NTT

# Make sure both json and text files are in sync
cp ~/boot/NTT/files/serverRoles.json ./files/serverRoles.json
cp ~/boot/NTT/files/birthdays.json ./files/birthdays.json
cp ~/boot/NTT/files/theme.txt ./files/theme.txt
cp ~/boot/NTT/files/vcname.json ./files/vcname.json

# Copy folders that need to have same content within them
cp -r ~/WIP/entity/files ~/boot/NTT
cp -r ~/WIP/entity/cogs ~/boot/NTT

# Remove comments and copy code to live version
sed '/^[ \t]*#/d' ~/WIP/entity/entity.py > ~/boot/NTT/entity.py

# Restart the bot
echo rjanortiz | sudo screen -S NTT -p 0 -X stuff '^C\n'
echo rjanortiz | sudo screen -S NTT -p 0 -X stuff 'python3 entity.py\n'
