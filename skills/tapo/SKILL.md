---
name: tapo
description: "TP-Link Tapo デバイスの制御スキル。tapo Pythonライブラリを使用してスマートプラグ(P100/P105/P110)、スマートライト(L510/L530)、テープライト(L900/L920)などをローカルネットワーク経由で制御する。「Tapoのプラグをオンにして」「テープライトを青にして」「消費電力を確認して」などの依頼時に使用。"
---

# TP-Link Tapo 制御スキル

## 環境変数

`.env` に以下を設定:
- `TAPO_EMAIL` - TP-Link アカウントのメールアドレス
- `TAPO_PASSWORD` - TP-Link アカウントのパスワード
- `TAPO_DEVICE_IP` - デバイスのローカルIP（複数ある場合はスクリプト引数で指定）

## インストール

```bash
pip install tapo
```

## 使い方

```bash
# デバイス情報取得
python3 scripts/tapo_control.py info [device_ip]

# プラグ ON/OFF
python3 scripts/tapo_control.py on [device_ip]
python3 scripts/tapo_control.py off [device_ip]

# ライト明るさ設定 (1-100)
python3 scripts/tapo_control.py brightness [device_ip] 80

# ライト色設定 (色相0-360, 彩度1-100)
python3 scripts/tapo_control.py color [device_ip] 240 100

# 消費電力確認 (P110のみ)
python3 scripts/tapo_control.py energy [device_ip]
```

## 対応デバイス

| カテゴリ | モデル |
|---------|--------|
| スマートプラグ | P100, P105, P110, P115 |
| スマートライト | L510, L520, L530, L535, L610, L630 |
| テープライト | L900, L920, L930 |
| パワーストリップ | P300, P304M |

## 注意事項

- ローカルネットワーク経由で通信するため、デバイスと同じLANに接続が必要
- `tapo` ライブラリは Python 3.11 以上が必要
