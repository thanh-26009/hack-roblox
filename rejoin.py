import os
import time
import json
import threading
from datetime import datetime

from flask import Flask, request
import requests

# ================= CONFIG =========================
PLACE_ID = 2753915549

TARGET_WEBHOOK = "https://discord.com/api/webhooks/1443617207765700701/_3n2NIaDoplc6SPuDumk88xUFcWdDcUtxB9JoT8lDhUJgNKu4YPoZUqmINj_iQuzm2jH"  # ĐỔI
SCREEN_PATH = "/sdcard/screen.png"

WEBHOOK_TIMEOUT = 600          # 10 phút
CRASH_CHECK_INTERVAL = 5       # giây
RESTART_COOLDOWN = 10          # chống loop restart

# ================= GLOBAL =========================
app = Flask(__name__)

last_webhook_time = time.time()
last_restart_time = 0
lock = threading.Lock()

# ================= UTILS ==========================
def now():
    return datetime.now().strftime("%H:%M:%S")

def run_root(cmd: str):
    full_cmd = f'su -c "{cmd}"'
    print(f"[{now()}] [ROOT] {cmd}")
    return os.system(full_cmd)

# ================= ROBLOX CONTROL =================
def restart_roblox(force=False):
    global last_restart_time, last_webhook_time

    current = time.time()
    if not force and current - last_restart_time < RESTART_COOLDOWN:
        return

    last_restart_time = current
    print(f"[{now()}] 🔁 Restart Roblox")

    run_root("am force-stop com.roblox.client")
    time.sleep(3)

    run_root(
        f"am start -a android.intent.action.VIEW "
        f"-d 'roblox://placeId={PLACE_ID}'"
    )

    with lock:
        last_webhook_time = time.time()

def is_roblox_running():
    pid = os.popen('su -c "pidof com.roblox.client"').read().strip()
    return bool(pid)

# ================= SCREENSHOT =====================
def take_screenshot():
    run_root(f"screencap -p {SCREEN_PATH}")

# ================= CRASH MONITOR ==================
def crash_monitor():
    while True:
        time.sleep(CRASH_CHECK_INTERVAL)

        if not is_roblox_running():
            print(f"[{now()}] ❌ Roblox crash detected")
            restart_roblox()

# ================= WATCHDOG =======================
def webhook_watchdog():
    while True:
        time.sleep(5)

        with lock:
            diff = time.time() - last_webhook_time

        if diff > WEBHOOK_TIMEOUT:
            print(f"[{now()}] ⏱ No webhook > timeout")
            restart_roblox()

# ================= WEBHOOK SERVER =================
@app.route("/webhook", methods=["POST"])
def receive_webhook():
    global last_webhook_time

    print(f"[{now()}] 📩 Webhook received")

    try:
        data = request.get_json(force=True)
    except:
        return "Invalid JSON", 400

    take_screenshot()

    if "embeds" in data and data["embeds"]:
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

        print(f"[{now()}] ✅ Forwarded to Discord ({r.status_code})")

    except Exception as e:
        print(f"[{now()}] ❌ Discord error:", e)

    with lock:
        last_webhook_time = time.time()

    return "OK", 200

# ================= MAIN ===========================
def start_threads():
    threading.Thread(target=restart_roblox, args=(True,), daemon=True).start()
    threading.Thread(target=crash_monitor, daemon=True).start()
    threading.Thread(target=webhook_watchdog, daemon=True).start()

if __name__ == "__main__":
    print("🚀 Roblox Watchdog v3 (Clean Root Mode)")
    start_threads()
    app.run(host="0.0.0.0", port=5000, debug=False)
