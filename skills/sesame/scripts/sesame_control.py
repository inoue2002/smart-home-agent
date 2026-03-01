#!/usr/bin/env python3
"""SESAME スマートロック制御スクリプト (CANDY HOUSE Web API)"""

import base64
import json
import os
import struct
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SESAME_API_KEY", "")
SECRET = os.getenv("SESAME_SECRET", "")
UUID = os.getenv("SESAME_UUID", "")
BASE_URL = "https://app.candyhouse.co/api/sesame2"


def headers():
    return {"x-api-key": API_KEY}


def generate_sign():
    """AES-CMAC署名を生成（簡易版: HMAC代替）"""
    # SESAME APIはtimestampベースの署名を要求
    ts = int(time.time())
    # タイムスタンプを1バイト(秒の下位32bit)に変換
    ts_bytes = struct.pack("<I", ts)[:4]
    # 本来はAES-CMACだが、簡易版としてbase64エンコード
    # 実運用では pycryptodome の AES-CMAC を使用すること
    try:
        from Crypto.Cipher import AES
        from Crypto.Hash import CMAC

        secret_bytes = bytes.fromhex(SECRET)
        cobj = CMAC.new(secret_bytes, ciphermod=AES)
        cobj.update(ts_bytes)
        sign = cobj.hexdigest()
    except ImportError:
        print("WARNING: pycryptodome未インストール。署名生成にはインストールが必要:")
        print("  pip install pycryptodome")
        sign = base64.b64encode(ts_bytes).decode()
    return sign


def get_status():
    """デバイスの状態を取得"""
    r = requests.get(f"{BASE_URL}/{UUID}", headers=headers(), timeout=10)
    data = r.json()
    if r.status_code == 200:
        battery = data.get("batteryPercentage", "?")
        position = data.get("CHSesame2Status", "?")
        print(f"  バッテリー: {battery}%")
        print(f"  状態: {position}")
    else:
        print(f"エラー: {r.status_code} {data}")


def send_command(cmd_id, history_name="smart-home-agent"):
    """コマンドを送信 (83=施錠, 88=解錠)"""
    sign = generate_sign()
    payload = {
        "cmd": cmd_id,
        "history": base64.b64encode(history_name.encode()).decode(),
        "sign": sign,
    }
    r = requests.post(
        f"{BASE_URL}/{UUID}/cmd",
        headers={**headers(), "Content-Type": "application/json"},
        json=payload,
        timeout=10,
    )
    return r


def lock():
    """施錠"""
    print("施錠中...")
    r = send_command(82)
    print(f"  結果: {r.status_code}")


def unlock():
    """解錠（確認あり）"""
    confirm = input("本当に解錠しますか？ (y/N): ")
    if confirm.lower() != "y":
        print("キャンセルしました")
        return
    print("解錠中...")
    r = send_command(83)
    print(f"  結果: {r.status_code}")


def get_history():
    """操作履歴を取得"""
    r = requests.get(f"{BASE_URL}/{UUID}/history", headers=headers(), timeout=10)
    if r.status_code == 200:
        for entry in r.json():
            ts = entry.get("timeStamp", "")
            type_name = entry.get("type", "")
            history_tag = entry.get("historyTag", "")
            if history_tag:
                history_tag = base64.b64decode(history_tag).decode(errors="replace")
            print(f"  {ts}  {type_name}  by {history_tag}")
    else:
        print(f"エラー: {r.status_code}")


def main():
    if len(sys.argv) < 2:
        print("Usage: sesame_control.py <command>")
        print("Commands: status, lock, unlock, history")
        return

    cmd = sys.argv[1]

    if cmd == "status":
        get_status()
    elif cmd == "lock":
        lock()
    elif cmd == "unlock":
        unlock()
    elif cmd == "history":
        get_history()
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
