#!/usr/bin/env python3
"""Philips Hue Bridge ローカル制御スクリプト (CLIP API v2)"""

import json
import os
import sys
import urllib3

import requests
from dotenv import load_dotenv

# 自己署名証明書の警告を抑制
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

BRIDGE_IP = os.getenv("HUE_BRIDGE_IP")
API_KEY = os.getenv("HUE_API_KEY")


def base_url():
    return f"https://{BRIDGE_IP}/clip/v2/resource"


def headers():
    return {"hue-application-key": API_KEY}


def discover():
    """mDNS/UPnP でBridgeを探す"""
    print("Hue Bridge を探しています...")
    try:
        r = requests.get("https://discovery.meethue.com", timeout=5)
        bridges = r.json()
        if bridges:
            for b in bridges:
                print(f"  Bridge IP: {b['internalipaddress']}  ID: {b['id']}")
        else:
            print("  Bridge が見つかりませんでした")
    except Exception as e:
        print(f"  エラー: {e}")


def register():
    """Hue Bridge にアプリケーションを登録してAPIキーを取得"""
    if not BRIDGE_IP:
        print("HUE_BRIDGE_IP を .env に設定してください")
        return
    print("Hue Bridge の物理ボタンを押してから Enter を押してください...")
    input()
    r = requests.post(
        f"https://{BRIDGE_IP}/api",
        json={"devicetype": "smart-home-agent#cli", "generateclientkey": True},
        verify=False,
        timeout=5,
    )
    result = r.json()
    if isinstance(result, list) and "success" in result[0]:
        username = result[0]["success"]["username"]
        clientkey = result[0]["success"].get("clientkey", "")
        print(f"APIキー取得成功!")
        print(f"  HUE_API_KEY={username}")
        if clientkey:
            print(f"  Client Key={clientkey}")
        print(".env に HUE_API_KEY を追記してください")
    else:
        print(f"登録失敗: {json.dumps(result, indent=2)}")


def list_lights():
    """全ライト一覧を表示"""
    r = requests.get(f"{base_url()}/light", headers=headers(), verify=False, timeout=5)
    data = r.json().get("data", [])
    for light in data:
        name = light["metadata"]["name"]
        on = light["on"]["on"]
        brightness = light.get("dimming", {}).get("brightness", "N/A")
        print(f"  [{light['id'][:8]}...] {name}  ON={on}  Brightness={brightness}")
    return data


def turn_on(light_id):
    """ライトをONにする"""
    r = requests.put(
        f"{base_url()}/light/{light_id}",
        headers=headers(),
        json={"on": {"on": True}},
        verify=False,
        timeout=5,
    )
    print(f"ON: {r.status_code}")


def turn_off(light_id):
    """ライトをOFFにする"""
    r = requests.put(
        f"{base_url()}/light/{light_id}",
        headers=headers(),
        json={"on": {"on": False}},
        verify=False,
        timeout=5,
    )
    print(f"OFF: {r.status_code}")


def set_brightness(light_id, brightness):
    """明るさを設定 (0-100)"""
    r = requests.put(
        f"{base_url()}/light/{light_id}",
        headers=headers(),
        json={"on": {"on": True}, "dimming": {"brightness": float(brightness)}},
        verify=False,
        timeout=5,
    )
    print(f"Brightness → {brightness}: {r.status_code}")


def set_color_temp(light_id, mirek):
    """色温度を設定 (153=冷白色 〜 500=暖色)"""
    r = requests.put(
        f"{base_url()}/light/{light_id}",
        headers=headers(),
        json={"on": {"on": True}, "color_temperature": {"mirek": int(mirek)}},
        verify=False,
        timeout=5,
    )
    print(f"Color temp → {mirek} mirek: {r.status_code}")


def all_off():
    """全ライトをOFFにする"""
    r = requests.get(f"{base_url()}/light", headers=headers(), verify=False, timeout=5)
    data = r.json().get("data", [])
    for light in data:
        if light["on"]["on"]:
            turn_off(light["id"])
            print(f"  {light['metadata']['name']} → OFF")


def main():
    if len(sys.argv) < 2:
        print("Usage: hue_control.py <command> [args]")
        print("Commands: discover, register, list, on, off, brightness, color_temp, all_off")
        return

    cmd = sys.argv[1]

    if cmd == "discover":
        discover()
    elif cmd == "register":
        register()
    elif cmd == "list":
        list_lights()
    elif cmd == "on" and len(sys.argv) > 2:
        turn_on(sys.argv[2])
    elif cmd == "off" and len(sys.argv) > 2:
        turn_off(sys.argv[2])
    elif cmd == "brightness" and len(sys.argv) > 3:
        set_brightness(sys.argv[2], sys.argv[3])
    elif cmd == "color_temp" and len(sys.argv) > 3:
        set_color_temp(sys.argv[2], sys.argv[3])
    elif cmd == "all_off":
        all_off()
    else:
        print(f"Unknown command or missing args: {cmd}")


if __name__ == "__main__":
    main()
