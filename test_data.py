import yfinance as yf
import pandas as pd

def test_data_structure():
    # S&P500のデータを取得（期間を短く設定）
    symbol = "^GSPC"
    df = yf.download(symbol, start='2024-01-01', end='2024-02-01', progress=False)
    
    print("\n=== 取得したデータの情報 ===")
    print("データフレームの形状:", df.shape)
    print("\nデータフレームの先頭:")
    print(df.head())
    
    # Closeカラムの抽出とシリーズ変換
    prices = df['Close'].squeeze()
    print("\n=== 価格データの情報 ===")
    print("データ型:", type(prices))
    print("データの形状:", prices.shape if hasattr(prices, 'shape') else "一次元データ")
    print("\n価格データの先頭:")
    print(prices.head())

if __name__ == "__main__":
    test_data_structure()