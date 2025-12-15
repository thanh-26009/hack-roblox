#!/bin/bash
termux-setup-storage && yes | pkg update && yes | pkg upgrade && yes | pkg i python && yes | pkg install python-pip && pkg install python tsu libexpat openssl -y && pip install requests Flask colorama aiohttp psutil
curl -Ls "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/rejoin.py" -o /sdcard/Download/rejoin.py


