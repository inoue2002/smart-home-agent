#!/usr/bin/env python3
"""SwitchBot REST API v1.1 制御スクリプト"""

import hashlib
import hmac
import base64
import json
import os
import sys
import time
import uuid

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SWITCHBOT_TOKEN", "")
SECRET = os.getenv("SWITCHBOT_SECRET", "")
BASE_URL = "https://api.switch-bot.com/v1.1"


def make_headers():
    """HMAC署名付きヘッダーを生成"""
    t = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    string_to_sign = f"{TOKEN}{t}{nonce}"
    sign = base64.b64encode(
        hmac.new(
            SECRET.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    ).decode("utf-8")
    return {
        "Authorization": TOKEN,
        "sign": sign,
        "nonce": nonce,
        "t": t,
        "Content-Type": "application/json",
    }


def list_devices():
    """デバイス一覧を取得"""
    r = requests.get(f"{BASE_URL}/devices", headers=make_headers(), timeout=10)
    data = r.json()
    if data.get("statusCode") != 100:
        print(f"エラー: {data}")
        return

    print("=== 物理デバイス ===")
    for d in data["body"].get("deviceList", []):
        print(f"  [{d['deviceId']}] {d['deviceName']} ({d['deviceType']})")

    print("\n=== 赤外線リモコンデバイス ===")
    for d in data["body"].get("infraredRemoteList", []):
        print(f"  [{d['deviceId']}] {d['deviceName']} ({d['remoteType']})")


def get_status(device_id):
    """デバイスの状態を取得"""
    r = requests.get(
        f"{BASE_URL}/devices/{device_id}/status",
        headers=make_headers(),
        timeout=10,
    )
    data = r.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))


def send_command(device_id, command, parameter="default"):
    """デバイスにコマンドを送信"""
    payload = {
        "command": command,
        "parameter": parameter,
        "commandType": "command",
    }
    r = requests.post(
        f"{BASE_URL}/devices/{device_id}/commands",
        headers=make_headers(),
        json=payload,
        timeout=10,
    )
    data = r.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        print("Usage: switchbot_control.py <command> [args]")
        print("Commands: list, status <id>, command <id> <cmd> [param]")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        list_devices()
    elif cmd == "status" and len(sys.argv) > 2:
        get_status(sys.argv[2])
    elif cmd == "command" and len(sys.argv) > 3:
        param = sys.argv[4] if len(sys.argv) > 4 else "default"
        send_command(sys.argv[2], sys.argv[3], param)
    else:
        print(f"Unknown command or missing args: {cmd}")


if __name__ == "__main__":
    main()
