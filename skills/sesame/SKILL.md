---
name: sesame
description: "SESAME スマートロックの制御スキル。CANDY HOUSE Web APIを使用して施錠/解錠、状態確認、操作履歴の取得を行う。「鍵かけて」「玄関を開錠して」「鍵の状態確認」「施錠履歴を見せて」などの依頼時に使用。"
---

# SESAME スマートロック制御スキル

## 環境変数

`.env` に以下を設定:
- `SESAME_API_KEY` - CANDY HOUSE Web API キー
- `SESAME_SECRET` - デバイスのシークレットキー
- `SESAME_UUID` - デバイスのUUID

### 取得手順
1. SESAME アプリ → デバイス設定 → 「鍵をシェア」からQRコードでシークレットキーとUUIDを確認
2. https://partners.candyhouse.co/ でAPIキーを取得

## 使い方

```bash
# 状態確認
python3 scripts/sesame_control.py status

# 施錠
python3 scripts/sesame_control.py lock

# 解錠
python3 scripts/sesame_control.py unlock

# 履歴取得
python3 scripts/sesame_control.py history
```

## 注意事項

- 解錠コマンドは安全確認のため実行前に確認プロンプトを表示する
- APIコマンド送信にはシークレットキーのAES-CMAC署名が必要
