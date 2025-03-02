import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # バックエンドをAggに設定
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import japanize_matplotlib  # 日本語フォントのサポート

class DrawdownCalculator:
    SYMBOLS = {
        'sp500': '^GSPC',       # S&P 500（価格のみ）
        'sp500tr': '^SP500TR',  # S&P 500（配当込み）
        'nasdaq100': '^NDX',    # Nasdaq 100
        'kokusai': 'TOK',       # MSCI Kokusai ETF
        'emerging': 'EEM'       # MSCI Emerging Markets ETF
    }
    
    NAMES = {
        'sp500': 'S&P 500',
        'sp500tr': 'S&P 500 (配当込み)',
        'nasdaq100': 'Nasdaq 100',
        'kokusai': 'MSCI Kokusai ETF',
        'emerging': 'MSCI Emerging Markets ETF'
    }

    def __init__(self, symbol_key='sp500'):
        if symbol_key not in self.SYMBOLS:
            raise ValueError(f"Invalid symbol key: {symbol_key}")
        self.symbol = self.SYMBOLS[symbol_key]
        self.name = self.NAMES[symbol_key]
        
    def fetch_data(self, start_date):
        """
        指定された開始日からS&P500のデータを取得
        """
        try:
            # データをダウンロード
            df = yf.download(self.symbol, start=start_date, progress=False)
            if df.empty:
                print("データが取得できませんでした")
                return None

            # 終値を直接Seriesとして取得
            prices = df['Close']
            prices.name = self.name
            return prices

        except Exception as e:
            print(f"データ取得エラー: {str(e)}")
            return None

    def calculate_drawdown(self, prices):
        """
        価格データからドローダウンを計算
        """
        # 確実に1次元のSeriesに変換
        prices_series = prices.squeeze()
        
        # 累積最大値を計算
        rolling_max = prices_series.expanding().max()
        
        # ドローダウンを計算 （現在価格 - これまでの最大値）/ これまでの最大値
        drawdown = (prices_series - rolling_max) / rolling_max
        
        return pd.Series(drawdown, index=prices.index)

    def plot_price(self, start_date):
        """
        価格推移グラフを生成
        """
        try:
            # データ取得
            prices = self.fetch_data(start_date)
            if prices is None or len(prices) == 0:
                print("データが取得できませんでした")
                return None

            # グラフ設定
            fig, ax = plt.subplots(figsize=(12, 4.2))
            ax.plot(prices.index, prices.values, 'b-', label=self.name)
            ax.set_ylabel('価格 ($)')
            ax.grid(True)
            ax.legend(loc='upper left')

            # Y軸のフォーマット設定（価格）
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

            # X軸の設定
            num_months = len(pd.date_range(start=prices.index[0], end=prices.index[-1], freq='M'))
            if num_months <= 6:
                interval = 1  # 1ヶ月おき
            elif num_months <= 12:
                interval = 2  # 2ヶ月おき
            elif num_months <= 24:
                interval = 3  # 3ヶ月おき
            else:
                interval = 12  # 6ヶ月おき

            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
            date_format = '%Y/%m/%d' if num_months <= 12 else '%Y/%m'
            ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

            # X軸ラベルの設定
            plt.xticks(rotation=45, ha='right')
            
            # X軸の範囲を厳密に設定（余白なし）
            ax.set_xlim(prices.index[0], prices.index[-1])

            plt.tight_layout()

            # タイトル設定
            ax.set_title(f'{self.name} 価格推移', fontsize=12, pad=20)

            return fig

        except Exception as e:
            print(f"価格グラフ作成エラー: {e}")
            return None

    def plot_drawdown(self, start_date):
        """
        ドローダウングラフを生成
        """
        try:
            # データ取得とドローダウン計算
            prices = self.fetch_data(start_date)
            if prices is None or len(prices) == 0:
                print("データが取得できませんでした")
                return None

            drawdown = self.calculate_drawdown(prices)

            # グラフ設定
            fig, ax = plt.subplots(figsize=(12, 4.2))
            ax.fill_between(drawdown.index, drawdown.values * 100, 0, color='red', alpha=0.3)
            ax.plot(drawdown.index, drawdown.values * 100, 'r-', label='ドローダウン')
            ax.set_ylabel('ドローダウン (%)')
            ax.grid(True)
            ax.legend(loc='upper left')

            # ドローダウンの範囲を設定
            max_drawdown = abs(min(drawdown.values)) * 100
            ax.set_ylim(min(drawdown.values) * 100, 0)
            ax.set_yticks([-i for i in range(0, int(max_drawdown) + 5, 5)])

            # X軸の設定
            num_months = len(pd.date_range(start=drawdown.index[0], end=drawdown.index[-1], freq='M'))
            if num_months <= 6:
                interval = 1  # 1ヶ月おき
            elif num_months <= 12:
                interval = 2  # 2ヶ月おき
            elif num_months <= 24:
                interval = 3  # 3ヶ月おき
            else:
                interval = 12  # 6ヶ月おき

            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
            date_format = '%Y/%m/%d' if num_months <= 12 else '%Y/%m'
            ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

            # X軸ラベルの設定
            plt.xticks(rotation=45, ha='right')
            
            # X軸の範囲を厳密に設定（余白なし）
            ax.set_xlim(drawdown.index[0], drawdown.index[-1])

            plt.tight_layout()

            # タイトル設定
            ax.set_title(f'{self.name} ドローダウン', fontsize=12, pad=20)

            return fig

        except Exception as e:
            print(f"ドローダウングラフ作成エラー: {e}")
            return None

def main():
    import argparse
    from datetime import datetime

    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description='S&P500のドローダウン分析')
    parser.add_argument('--start_date', type=str, 
                      help='開始日（YYYY-MM-DD形式）',
                      default='2024-01-01')
    
    args = parser.parse_args()

    try:
        # 日付形式の検証
        datetime.strptime(args.start_date, '%Y-%m-%d')
    except ValueError:
        print("エラー: 開始日は'YYYY-MM-DD'形式で指定してください")
        return

    # グラフの生成
    calculator = DrawdownCalculator()
    
    # 価格推移グラフ
    fig_price = calculator.plot_price(args.start_date)
    if fig_price:
        plt.savefig('sp500_price.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("価格推移グラフを'sp500_price.png'として保存しました。")
    
    # ドローダウングラフ
    fig_drawdown = calculator.plot_drawdown(args.start_date)
    if fig_drawdown:
        plt.savefig('sp500_drawdown.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("ドローダウングラフを'sp500_drawdown.png'として保存しました。")
    
    print(f"開始日: {args.start_date}")

if __name__ == "__main__":
    main()