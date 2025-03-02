from flask import Flask, render_template, request, send_file, url_for
from datetime import datetime
import os
from drawdown_calculator import DrawdownCalculator
import matplotlib.pyplot as plt

app = Flask(__name__)

# 静的ファイル用のディレクトリを作成
UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    graph_filenames = {'price': None, 'drawdown': None}
    start_date = None
    selected_symbol = None

    if request.method == 'POST':
        start_date = request.form.get('start_date', '')
        selected_symbol = request.form.get('symbol', 'sp500')
        
        try:
            # 日付形式の検証
            datetime.strptime(start_date, '%Y-%m-%d')
            
            # グラフの生成
            calculator = DrawdownCalculator(symbol_key=selected_symbol)
            
            # 古いグラフファイルを削除
            for filename in os.listdir(UPLOAD_FOLDER):
                if any(filename.startswith((f"{symbol}_price_", f"{symbol}_drawdown_")) for symbol in DrawdownCalculator.SYMBOLS.keys()):
                    os.remove(os.path.join(UPLOAD_FOLDER, filename))
            
            # タイムスタンプ
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # 価格推移グラフ
            fig_price = calculator.plot_price(start_date)
            if fig_price:
                price_filename = f'{selected_symbol}_price_{timestamp}.png'
                plt.savefig(os.path.join(UPLOAD_FOLDER, price_filename), dpi=300, bbox_inches='tight')
                plt.close()
                graph_filenames['price'] = price_filename
            
            # ドローダウングラフ
            fig_drawdown = calculator.plot_drawdown(start_date)
            if fig_drawdown:
                drawdown_filename = f'{selected_symbol}_drawdown_{timestamp}.png'
                plt.savefig(os.path.join(UPLOAD_FOLDER, drawdown_filename), dpi=300, bbox_inches='tight')
                plt.close()
                graph_filenames['drawdown'] = drawdown_filename
            
            if not any(graph_filenames.values()):
                error_message = "グラフの生成に失敗しました。"
        
        except ValueError as e:
            error_message = "正しい日付形式（YYYY-MM-DD）で入力してください。"
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    # デフォルト値の設定
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    if not selected_symbol:
        selected_symbol = 'sp500'

    # 利用可能な銘柄一覧
    symbols = {
        'sp500': 'S&P 500',
        'sp500tr': 'S&P 500 (配当込み)',
        'nasdaq100': 'Nasdaq 100',
        'kokusai': 'MSCI Kokusai ETF',
        'emerging': 'MSCI Emerging Markets ETF'
    }

    return render_template('index.html',
                         error_message=error_message,
                         graph_filenames=graph_filenames,
                         start_date=start_date,
                         selected_symbol=selected_symbol,
                         symbols=symbols)

if __name__ == '__main__':
    app.run(debug=True)