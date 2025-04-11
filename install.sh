#!/bin/bash
termux-setup-storage && yes | pkg update && yes | pkg upgrade && yes | pkg i python && yes | pkg install python-pip && pkg install python tsu libexpat openssl -y && pip install requests Flask colorama aiohttp psutil crypto pycryptodome loguru prettytable 
curl -Ls "https://raw.githubusercontent.com/thieusitinks/Rokid-Manager/refs/heads/main/Rokid-UgPhone-Free-Tool" -o /sdcard/Download/Rokid-Rejoin.py
curl -Ls "https://www.floatingapps.net/apk/apk-free-release/4.14/FloatingApps-gnFreeArmeabi-v7aRelease-141400012.apk" -o /sdcard/Download/FloatingApps.apk
curl -Ls "https://raw.githubusercontent.com/thieusitinks/Rokid-Manager/refs/heads/main/Rokid-UgPhone-Free-Tool" -o /sdcard/Download/Rokid-Rejoin.py
curl -LS "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/w-azure.txt" -o /sdcard/Download/w-azure.lua
curl -ls "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/Royxkaitun.txt" -o /sdcard/Download/kaitun.lua
curl -Ls "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/Finder-fruit-turbo.txt" -o /sdcard/Download/fruit.lua
curl -Ls "https://raw.githubusercontent.com/thanh-26009/Ugphone/refs/heads/main/download.py" -o download.py

python3 download.py https://www.mediafire.com/file_premium/xpf1j5jyqc7wjuy/Delta-666.609-01.apk/file
su -c "pm install -r Delta-666.609-01.apk"
echo "Đã cài xong Delta"
