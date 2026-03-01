---
name: switchbot
description: "SwitchBot デバイスの制御スキル。SwitchBot REST API v1.1を使用してボット、カーテン、プラグ、ハブ経由の赤外線家電などを操作する。「エアコンつけて」「カーテン開けて」「SwitchBotのデバイス一覧」「温度を確認して」などの依頼時に使用。"
---

# SwitchBot 制御スキル

## 環境変数

`.env` に以下を設定:
- `SWITCHBOT_TOKEN` - SwitchBotアプリの開発者オプションから取得
- `SWITCHBOT_SECRET` - 同上

### トークン取得手順
1. SwitchBot アプリ → プロフィール → 設定 → アプリバージョンを10回タップ
2. 開発者オプション → トークン取得

## 使い方

```bash
# デバイス一覧
python3 scripts/switchbot_control.py list

# デバイスの状態取得
python3 scripts/switchbot_control.py status <device_id>

# コマンド実行
python3 scripts/switchbot_control.py command <device_id> <command> [parameter]

# 例: ボットを押す
python3 scripts/switchbot_control.py command DEVICE_ID press

# 例: エアコンON (赤外線リモコン)
python3 scripts/switchbot_control.py command DEVICE_ID turnOn
```

## 主要コマンド一覧

| デバイス | コマンド | パラメータ |
|---------|---------|-----------|
| Bot | press, turnOn, turnOff | - |
| Curtain | open, close, setPosition | 0-100 |
| Plug Mini | turnOn, turnOff | - |
| 赤外線家電 | turnOn, turnOff | - |
| エアコン | setAll | temp,mode,fanSpeed,powerState |
