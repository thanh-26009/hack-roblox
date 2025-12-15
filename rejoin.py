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
# ===============================================

# FIX PATH cho Termux (QUAN TRỌNG)
os.environ["PATH"] = "/data/data/com.termux/files/usr/bin:" + os.environ.get("PATH", "")

# ================== CONFIG ==================
PLACE_ID = 2753915549
TARGET_WEBHOOK = "https://discord.com/api/webhooks/1443617207765700701/_3n2NIaDoplc6SPuDumk88xUFcWdDcUtxB9JoT8lDhUJgNKu4YPoZUqmINj_iQuzm2jH"  # ← đổi webhook
TIMEOUT = 600  # 10 phút
SCREEN_PATH = "/sdcard/screen.png"
SU_BIN = "/data/data/com.termux/files/usr/bin/su"
# ============================================

app = Flask(__name__)
last_webhook_time = time.time()
lock = threading.Lock()

# ================== ROOT RUN ==================
def run_root(cmd):
    full = f"{SU_BIN} -c \"{cmd}\""
    print("[ROOT]", cmd)
    return os.system(full)

# ================== ROBLOX ==================
def restart_roblox():
    global last_webhook_time
    print("[!] Restarting Roblox")

    run_root("am force-stop com.roblox.client")
    time.sleep(3)
    run_root(
        f"am start -a android.intent.action.VIEW -d 'roblox://placeId={PLACE_ID}'"
    )

    with lock:
        last_webhook_time = time.time()

# ================== SCREENSHOT ==================
def take_screenshot():
    run_root(f"screencap -p {SCREEN_PATH}")

# ================== WEBHOOK ==================
@app.route("/webhook", methods=["POST"])
def webhook():
    global last_webhook_time
    data = request.get_json(force=True)

    print("[+] Webhook received")

    # 📸 chụp màn hình (LUÔN ẢNH MỚI)
    take_screenshot()

    # thay image bằng attachment
    if "embeds" in data and len(data["embeds"]) > 0:
        data["embeds"][0]["image"] = {
            "url": "attachment://screen.png"
        }

    payload = {
        "payload_json": json.dumps(data, ensure_ascii=False)
    }

    try:
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
    except Exception as e:
        print("[!] Discord send error:", e)

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
            threading.Thread(target=restart_roblox, daemon=True).start()

# ================== MAIN ==================
if __name__ == "__main__":
    # restart ngay khi chạy
    threading.Thread(target=restart_roblox, daemon=True).start()

    # watchdog nền
    threading.Thread(target=watchdog, daemon=True).start()

    # server webhook
    app.run(host="0.0.0.0", port=5000)
