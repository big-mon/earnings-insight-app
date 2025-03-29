# API仕様書

## 外部APIの利用

### Yahoo Finance API (yfinance)

#### 概要
- パッケージ名: yfinance
- バージョン: 0.2.37
- 用途: 米国株式の財務データ取得

#### 主要なエンドポイント

1. 財務諸表データ
```python
ticker.financials  # 年次財務諸表
ticker.quarterly_financials  # 四半期財務諸表
```

2. キャッシュフロー
```python
ticker.cashflow  # 年次キャッシュフロー
ticker.quarterly_cashflow  # 四半期キャッシュフロー
```

3. 貸借対照表
```python
ticker.balance_sheet  # 年次貸借対照表
ticker.quarterly_balance_sheet  # 四半期貸借対照表
```

4. 株式情報
```python
ticker.info  # 企業情報、株価情報など
```

#### エラーハンドリング
- 接続エラー: ネットワーク接続の問題
- データ未取得: 指定した期間のデータが存在しない
- 無効なティッカー: 存在しないティッカーシンボル

#### レート制限
- 過度なリクエストを避けるため、適切なインターバルを設定
- キャッシュの活用を検討

## 内部API

### データ取得サービス
- 場所: `src/services/finance.py`
- 機能: 財務データの取得と正規化

### グラフ生成サービス
- 場所: `src/services/graph.py`
- 機能: Plotlyを使用したグラフの生成

### ユーティリティ関数
- 場所: `src/utils/`
- 機能: データ変換、フォーマット処理など