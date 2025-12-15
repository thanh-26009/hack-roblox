import sys
import os
import time
import json
import threading
from datetime import datetime

# ================= AUTO INSTALL =================
def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"[!] Installing missing package: {pkg}")
        os.system(f"pip install {pkg}")

ensure_package("flask")
ensure_package("requests")

from flask import Flask, request
import requests
# ================================================

# ================== CONFIG ==================
PLACE_ID = 2753915549
TARGET_WEBHOOK = "https://discord.com/api/webhooks/1443617207765700701/_3n2NIaDoplc6SPuDumk88xUFcWdDcUtxB9JoT8lDhUJgNKu4YPoZUqmINj_iQuzm2jH"
TIMEOUT = 600  # 10 phút
SCREEN_PATH = "/sdcard/screen.png"
# ============================================

app = Flask(__name__)
last_webhook_time = time.time()
lock = threading.Lock()

# ================== ROBLOX ==================
def restart_roblox():
    global last_webhook_time
    print("[!] Restarting Roblox")

    os.system("su -c 'am force-stop com.roblox.client'")
    time.sleep(3)
    os.system(
        f"su -c \"am start -a android.intent.action.VIEW -d 'roblox://placeId={PLACE_ID}'\""
    )

    with lock:
        last_webhook_time = time.time()

# ================== SCREENSHOT ==================
def take_screenshot():
    os.system(f"su -c 'screencap -p {SCREEN_PATH}'")

# ================== WEBHOOK ==================
@app.route("/webhook", methods=["POST"])
def webhook():
    global last_webhook_time
    data = request.get_json(force=True)

    print("[+] Webhook received")

    # 📸 chụp màn hình
    take_screenshot()

    # thay image bằng attachment
    if "embeds" in data and len(data["embeds"]) > 0:
        data["embeds"][0]["image"] = {
            "url": "attachment://screen.png"
        }

    payload = {
        "payload_json": json.dumps(data, ensure_ascii=False)
    }

    with open(SCREEN_PATH, "rb") as img:
        files = {
            "file": ("screen.png", img, "image/png")
        }

        r = requests.post(
            TARGET_WEBHOOK,
            data=payload,
            files=files,
            timeout=15
        )

    print("[+] Forwarded:", r.status_code)

    with lock:
        last_webhook_time = time.time()

    return "OK", 200

# ================== WATCHDOG ==================
def watchdog():
    global last_webhook_time
    while True:
        time.sleep(5)
        with lock:
            diff = time.time() - last_webhook_time

        if diff > TIMEOUT:
            print("[!] No webhook > 10 minutes")
            restart_roblox()

# ================== MAIN ==================
if __name__ == "__main__":
    restart_roblox()
    threading.Thread(target=watchdog, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
