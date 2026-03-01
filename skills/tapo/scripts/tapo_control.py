#!/usr/bin/env python3
"""TP-Link Tapo ローカル制御スクリプト"""

import asyncio
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("TAPO_EMAIL", "")
PASSWORD = os.getenv("TAPO_PASSWORD", "")
DEFAULT_IP = os.getenv("TAPO_DEVICE_IP", "")


async def get_client(device_ip):
    """Tapo APIクライアントを取得（デバイスタイプを自動判別）"""
    from tapo import ApiClient

    client = ApiClient(EMAIL, PASSWORD)
    # まずGenericDeviceとして接続を試みる
    return client, device_ip


async def device_info(device_ip):
    """デバイス情報を取得"""
    from tapo import ApiClient

    client = ApiClient(EMAIL, PASSWORD)
    try:
        # P100系（プラグ）として試行
        device = await client.p100(device_ip)
        info = await device.get_device_info()
        print(json.dumps(info.to_dict(), indent=2, ensure_ascii=False, default=str))
    except Exception:
        try:
            # L530系（ライト）として試行
            device = await client.l530(device_ip)
            info = await device.get_device_info()
            print(json.dumps(info.to_dict(), indent=2, ensure_ascii=False, default=str))
        except Exception as e:
            print(f"デバイス接続エラー: {e}")


async def turn_on(device_ip):
    """デバイスをONにする"""
    from tapo import ApiClient

    client = ApiClient(EMAIL, PASSWORD)
    try:
        device = await client.p100(device_ip)
        await device.on()
        print(f"ON: {device_ip}")
    except Exception:
        try:
            device = await client.l530(device_ip)
            await device.on()
            print(f"ON: {device_ip}")
        except Exception as e:
            print(f"エラー: {e}")


async def turn_off(device_ip):
    """デバイスをOFFにする"""
    from tapo import ApiClient

    client = ApiClient(EMAIL, PASSWORD)
    try:
        device = await client.p100(device_ip)
        await device.off()
        print(f"OFF: {device_ip}")
    except Exception:
        try:
            device = await client.l530(device_ip)
            await device.off()
            print(f"OFF: {device_ip}")
        except Exception as e:
            print(f"エラー: {e}")


async def set_brightness(device_ip, level):
    """明るさを設定 (1-100) ※ライトデバイスのみ"""
    from tapo import ApiClient

    client = ApiClient(EMAIL, PASSWORD)
    try:
        device = await client.l530(device_ip)
        await device.set_brightness(int(level))
        print(f"Brightness → {level}: {device_ip}")
    except Exception as e:
        print(f"エラー（ライトデバイスでない可能性）: {e}")


async def set_color(device_ip, hue, saturation):
    """色を設定 (色相0-360, 彩度1-100) ※カラーライトのみ"""
    from tapo import ApiClient

    client = ApiClient(EMAIL, PASSWORD)
    try:
        device = await client.l530(device_ip)
        await device.set_hue_saturation(int(hue), int(saturation))
        print(f"Color → hue={hue} sat={saturation}: {device_ip}")
    except Exception as e:
        print(f"エラー（カラーライトでない可能性）: {e}")


async def get_energy(device_ip):
    """消費電力を取得 ※P110のみ"""
    from tapo import ApiClient

    client = ApiClient(EMAIL, PASSWORD)
    try:
        device = await client.p110(device_ip)
        usage = await device.get_energy_usage()
        print(json.dumps(usage.to_dict(), indent=2, ensure_ascii=False, default=str))
    except Exception as e:
        print(f"エラー（P110でない可能性）: {e}")


async def main_async():
    if len(sys.argv) < 2:
        print("Usage: tapo_control.py <command> [device_ip] [args]")
        print("Commands: info, on, off, brightness, color, energy")
        return

    cmd = sys.argv[1]
    device_ip = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_IP

    if not device_ip:
        print("デバイスIPを指定するか TAPO_DEVICE_IP を .env に設定してください")
        return

    if cmd == "info":
        await device_info(device_ip)
    elif cmd == "on":
        await turn_on(device_ip)
    elif cmd == "off":
        await turn_off(device_ip)
    elif cmd == "brightness" and len(sys.argv) > 3:
        await set_brightness(device_ip, sys.argv[3])
    elif cmd == "color" and len(sys.argv) > 4:
        await set_color(device_ip, sys.argv[3], sys.argv[4])
    elif cmd == "energy":
        await get_energy(device_ip)
    else:
        print(f"Unknown command or missing args: {cmd}")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
