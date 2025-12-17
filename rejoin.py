import os
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


def auto_execute_file():
    """Kiểm tra auto-bounty.lua có tồn tại chưa, chưa có thì tải."""
    
    # tạo folder nếu chưa có
    if not os.path.exists(AUTO_EXEC_FOLDER):
        try:
            os.makedirs(AUTO_EXEC_FOLDER)
            print("[+] Created AUTO_EXECUTE folder")
        except Exception as e:
            print("[-] Failed create folder:", e)
            return
    
    # nếu file đã tồn tại
    if os.path.exists(AUTO_EXEC_FILE):
        print("[✓] AUTO_EXECUTE script already exists → skip download")
        return
    
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

    auto_execute_file()

    threading.Thread(target=restart_roblox, daemon=True).start()

    threading.Thread(target=watchdog, daemon=True).start()

    print("Webhook forward server đang chạy port 5000...")
    app.run(host="0.0.0.0", port=5000)
