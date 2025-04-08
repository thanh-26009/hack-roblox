#!/bin/bash
termux-setup-storage && yes | pkg update && yes | pkg upgrade && yes | pkg i python && yes | pkg install python-pip && pkg install python tsu libexpat openssl -y && pip install requests Flask colorama aiohttp psutil crypto pycryptodome loguru prettytable 
curl -Ls "https://raw.githubusercontent.com/thieusitinks/Rokid-Manager/refs/heads/main/Rokid-UgPhone-Free-Tool" -o /sdcard/Download/Rokid-Rejoin.py
curl -Ls "https://www.floatingapps.net/apk/apk-free-release/4.14/FloatingApps-gnFreeArmeabi-v7aRelease-141400012.apk" -o /sdcard/Download/FloatingApps.apk
curl -Ls "https://download2434.mediafire.com/o6ic80g761lglRaTUXnCAq4lp52lhORJx3Wx0G3vNFua6_djizTy21mMopTeU2VmvLnBsS8Mtpfn8AbI7cWn7BFGXAhe5jLyIAogUZgCv9XJpVKy054kW22uxLkwJpud843H_WQXL5CKZ7llZuiNPpBKWzxpzt2nporENH-qaL7_1g/rknq0g7dgymxh3z/Delta-665.684-02.apk" -o /sdcard/Download/Delta.apk
curl -Ls "https://raw.githubusercontent.com/thieusitinks/Rokid-Manager/refs/heads/main/Rokid-UgPhone-Free-Tool" -o /sdcard/Download/Rokid-Rejoin.py
curl -LS "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/w-azure.txt" -o /sdcard/Download/w-azure.lua
curl -ls "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/Royxkaitun.txt" -o /sdcard/Download/kaitun.lua
curl -Ls "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/Finder-fruit-turbo.txt" -o /sdcard/Download/fruit.lua

su -c "pm install -r /sdcard/Download/FloatingApps.apk"
echo "Đã cài xong app1.apk"
su -c "pm install -r /sdcard/Download/Delta.apk"
echo "Đã cài xong app2.apk"

