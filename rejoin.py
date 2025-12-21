import os
import re
import json
import time
import requests
import threading
import subprocess
from flask import Flask, request


# ============================================
app = Flask(__name__)
last_webhook_time = time.time()
lock = threading.Lock()

# ================== CONFIG ==================
TIMEOUT = 600
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1443617207765700701/_3n2NIaDoplc6SPuDumk88xUFcWdDcUtxB9JoT8lDhUJgNKu4YPoZUqmINj_iQuzm2jH"
AUTO_EXEC_FOLDER = "/sdcard/Delta/Autoexecute"
AUTO_EXEC_FILE = f"{AUTO_EXEC_FOLDER}/auto-bounty.lua"
REMOTE_FILE_URL = "https://raw.githubusercontent.com/thanh-26009/hack-roblox/refs/heads/main/auto-bounty.lua"
CLOUDFLARE_BIN = "/data/data/com.termux/files/usr/bin/cloudflared"
DOWNLOAD_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"

#===============DOWNlOAD CLOUDFLARED================================

def download_cloudflared():
    print("[+] Downloading cloudflared latest...")

    try:
        r = requests.get(DOWNLOAD_URL, stream=True, timeout=300)

        if r.status_code != 200:
            print("[-] Download failed:", r.status_code)
            return False

        # ghi binary
        with open(CLOUDFLARE_BIN, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        os.system(f"chmod +x {CLOUDFLARE_BIN}")

        print("[✓] Installed cloudflared →", CLOUDFLARE_BIN)

        # test phiên bản
        try:
            result = subprocess.check_output([CLOUDFLARE_BIN, "-v"])
            print("[+] Version:", result.decode().strip())
        except:
            print("[!] installed but cannot check version")

        return True

    except Exception as e:
        print("[-] Error downloading:", e)
        return False

def start_tunnel():
    global PUBLIC_URL

    print("[+] Starting cloudflared tunnel...")

    # chạy và bắt output
    proc = subprocess.Popen(
        [CLOUDFLARE_BIN, "tunnel", "--url", "http://localhost:5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # đọc output để trích link public
    while True:
        line = proc.stdout.readline()
        if not line:
            break

        print("[CF] ", line.strip())

        if "trycloudflare.com" in line:
            PUBLIC_URL = line.strip().split(" ")[-1]
            print("[+] Tunnel URL:", PUBLIC_URL)
            return PUBLIC_URL

    return None

#=============DOWNLOAD SCRIPT=====================

def auto_execute_file():
    global PUBLIC_URL   # dùng URL global từ start_tunnel()

    """Kiểm tra auto-bounty.lua có tồn tại chưa, chưa có thì tải."""

    if not os.path.exists(AUTO_EXEC_FOLDER):
        try:
            os.makedirs(AUTO_EXEC_FOLDER)
            print("[+] Created AUTO_EXECUTE folder")
        except Exception as e:
            print("[-] Failed create folder:", e)
            return
    
    # nếu file đã tồn tại → sửa webhook luôn
    if os.path.exists(AUTO_EXEC_FILE):
        print("[✓] AUTO_EXECUTE script already exists")
    else:
        print("[!] AUTO_EXECUTE script missing → downloading...")

        try:
            r = requests.get(REMOTE_FILE_URL, timeout=10)
            if r.status_code == 200:
                with open(AUTO_EXEC_FILE, "w", encoding="utf8") as f:
                    f.write(r.text)

                print("[+] Downloaded auto-bounty.lua successfully")
            else:
                print("[-] Download failed:", r.status_code)

        except Exception as e:
            print("[-] Error downloading auto script:", e)
            return

    # ==== PATCH WEBHOOK URL TRONG LUA FILE ====
    try:
        if PUBLIC_URL:
            with open(AUTO_EXEC_FILE, "r", encoding="utf8") as f:
                content = f.read()

            endpoint = PUBLIC_URL.rstrip("/") + "/webhook"
            content = re.sub(
                r'Url\s*=\s*".*?"',
                f'Url = "{endpoint}"',
                content
            )

            with open(AUTO_EXEC_FILE, "w", encoding="utf8") as f:
                f.write(content)

            print("[✓] Patched webhook Url with public tunnel")

        else:
            print("[!] PUBLIC_URL not ready → skip patch")

    except Exception as e:
        print("[-] error patching lua webhook:", e)

# ================== ROBLOX ==================
def restart_roblox():
    print("[!] Restarting Roblox")
    subprocess.run('su -c "am force-stop com.roblox.client"', shell=True)
    time.sleep(1)
    subprocess.run('su -c "am start -a android.intent.action.VIEW -d roblox://placeId=2753915549"', shell=True)


# ================== SCREENSHOT ==================
def screen():
    timestamp = str(int(time.time() * 1000))
    path = f"/sdcard/screen_{timestamp}.png"
    subprocess.run(f'su -c "screencap -p {path}"', shell=True)
    return path


@app.route("/webhook", methods=["POST"])
def webhook_receiver():
    global last_webhook_time

    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return {"error": "Invalid JSON"}, 400

    print("[+] Nhận webhook")

    with lock:
        last_webhook_time = time.time()

    SCREEN_PATH = screen()
    file_name = os.path.basename(SCREEN_PATH)

    IMAGE_EXISTS = os.path.exists(SCREEN_PATH)

    # ================== chỉ sửa embed nếu có ảnh ==================
    if IMAGE_EXISTS and "embeds" in payload and payload["embeds"]:
        try:
            embed = payload["embeds"][0]

            embed.pop("image", None)  # bỏ url gốc
            embed["image"] = {"url": f"attachment://{file_name}"}  # thay url

            print("[+] embed image replaced with local screenshot")

        except Exception as e:
            print("[-] embed modify error:", e)

    else:
        print("[!] No screenshot available → keep original embed")

    # prepare payload
    data = {"payload_json": json.dumps(payload, ensure_ascii=False)}

    try:
        if IMAGE_EXISTS:
            print("[+] Screenshot exists → sending with file")

            with open(SCREEN_PATH, "rb") as f:
                files = {"file": (file_name, f)}
                r = requests.post(DISCORD_WEBHOOK, data=data, files=files)

        else:
            print("[-] Screenshot missing → send only payload json")
            r = requests.post(DISCORD_WEBHOOK, data=data)

        print("[+] Forward status:", r.status_code)

    except Exception as e:
        print("[-] Error forward discord:", e)

    return {"status": "forwarded"}, 200

# ====== WATCHDOG ======
def watchdog():
    global last_webhook_time
    print("[Watchdog] started")

    while True:
        time.sleep(5)

        with lock:
            diff = time.time() - last_webhook_time

        if diff > TIMEOUT:
            print(f"[Watchdog] No webhook {diff:.0f}s → restarting Roblox")

            threading.Thread(target=restart_roblox, daemon=True).start()

            with lock:
                last_webhook_time = time.time()



if __name__ == "__main__":

    # ====== DOWNLOAD CLOUDFLARED IF MISSING ======
    if not os.path.exists(CLOUDFLARE_BIN):
        ok = download_cloudflared()
        if not ok:
            print("[-] cannot install cloudflared → exit")
            exit()

    # ====== START CLOUDFLARED TUNNEL ======
    PUBLIC_URL = start_tunnel()
    if not PUBLIC_URL:
        print("[-] cannot detect tunnel URL → exit")
        exit()

    # ====== PATCH LUA WITH PUBLIC URL ======
    auto_execute_file()

    # ====== START ROBLOX REST WATCH ======
    threading.Thread(target=restart_roblox, daemon=True).start()
    threading.Thread(target=watchdog, daemon=True).start()

    print("Webhook forward server đang chạy port 5000...")
    app.run(host="0.0.0.0", port=5000)
