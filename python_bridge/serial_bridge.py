import os
import time
import requests
import serial
import serial.tools.list_ports

# Configuration (set via environment variables or replace placeholders locally)
HA_HOST = os.getenv("HA_HOST", "YOUR_HOME_ASSISTANT_IP_OR_TAILSCALE_IP")
HA_PORT = os.getenv("HA_PORT", "8123")
WEBHOOK_ID = os.getenv("HA_WEBHOOK_ID", "YOUR_HA_WEBHOOK_ID")
HA_URL = f"http://{HA_HOST}:{HA_PORT}/api/webhook/{WEBHOOK_ID}"

# Paste your deployed Google Apps Script Web App URL here (or set GSHEET_WEBAPP_URL env var)
GSHEET_WEBAPP_URL = os.getenv(
    "GSHEET_WEBAPP_URL",
    "YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL"
)

BAUD_RATE = 115200


def find_microbit_port():
    """Finds the BBC micro:bit serial port on Windows or Linux/Raspberry Pi."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "micro:bit" in port.description.lower() or port.vid == 0x0D28:
            return port.device
        if "COM" in port.device or "ttyACM" in port.device:
            return port.device
    return None


def send_to_google_sheet(student_id, answer):
    """Logs the student's answer directly into the active row of the QandA Google Sheet."""
    if not GSHEET_WEBAPP_URL or "YOUR_GOOGLE_APPS_SCRIPT" in GSHEET_WEBAPP_URL:
        return
    try:
        payload = {"student_id": student_id, "answer": answer}
        res = requests.post(GSHEET_WEBAPP_URL, json=payload, timeout=5)
        if res.status_code == 200:
            print(f"[SHEET OK] Logged to QandA -> {student_id}: {answer}")
        else:
            print(f"[SHEET WARN] HTTP {res.status_code}")
    except Exception as e:
        print(f"[SHEET ERR] {e}")


def send_to_home_assistant(data_string):
    """Parses serial payload (e.g., ID1_ANS:A) and dispatches to Home Assistant & Google Sheets."""
    try:
        if "_ANS:" in data_string:
            student_id, answer = data_string.split("_ANS:")
            s_id = student_id.strip()
            ans = answer.strip()
            payload = {
                "student_id": s_id,
                "answer": ans,
                "raw": data_string.strip(),
            }

            # 1. Send to Home Assistant (real-time classroom dashboard)
            response = requests.post(HA_URL, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[HA OK] Sent -> Student: {s_id} | Answer: {ans}")
            else:
                print(f"[HA WARN] HTTP {response.status_code}: {response.text}")

            # 2. Simultaneous logging to Google Sheets
            send_to_google_sheet(s_id, ans)

    except Exception as e:
        print(f"[ERR] Failed to process payload: {e}")


def main():
    print("=== School Edge Node: micro:bit Gateway -> Home Assistant & Google Sheets ===")

    ser = None
    while True:
        try:
            if ser is None or not ser.is_open:
                port = find_microbit_port()
                if port:
                    print(f"[INFO] Connecting to Gateway micro:bit on {port}...")
                    ser = serial.Serial(port, BAUD_RATE, timeout=1)
                    print(f"[SUCCESS] Gateway connected on {port}. Waiting for votes...")
                else:
                    print("[INFO] Waiting for Gateway micro:bit to be plugged in...")
                    time.sleep(3)
                    continue

            if ser and ser.in_waiting > 0:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    print(f"[SERIAL DATA] {line}")
                    send_to_home_assistant(line)

        except (serial.SerialException, OSError) as e:
            print(f"[WARN] Connection lost: {e}. Reconnecting in 3s...")
            if ser:
                ser.close()
            ser = None
            time.sleep(3)
        except Exception as e:
            print(f"[ERR] Unexpected error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
