# Drawdown Calculator

株価指数のドローダウン（最高値からの下落率）を分析・可視化するWebアプリケーション

## 機能

- 各種株価指数の価格推移とドローダウンをグラフ表示
- 任意の開始日からの分析が可能
- レスポンシブデザインのWebインターフェース

### 対応指数

- S&P 500（価格のみ）
- S&P 500（配当込み）
- Nasdaq 100
- MSCI Kokusai ETF (TOK)
- MSCI Emerging Markets ETF (EEM)

## インストール

```bash
# リポジトリのクローン
git clone https://github.com/walksoda/drawdown_calculator.git
cd drawdown_calculator

# 仮想環境の作成と有効化
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 必要なパッケージのインストール
pip install -r requirements.txt
```

## 使用方法

1. Webアプリケーションの起動：
```bash
python app.py
```

2. ブラウザで以下のURLにアクセス：
```
http://127.0.0.1:5000
```

3. 分析したい指数と開始日を選択してグラフを生成

## 注意事項

- データは[Yahoo Finance](https://finance.yahoo.com/)から取得
- 株価データの取得には安定したインターネット接続が必要
- 長期間のデータ取得は時間がかかる場合があります

## 開発環境

- Python 3.10+
- Flask
- yfinance
- pandas
- matplotlib
- japanize-matplotlib

## ライセンス

MITライセンス

## 作者

[walksoda](https://github.com/walksoda)