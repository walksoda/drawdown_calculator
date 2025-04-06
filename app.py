from flask import Flask, render_template, request, send_file, url_for, jsonify
from datetime import datetime
import os
from drawdown_calculator import DrawdownCalculator
import matplotlib.pyplot as plt

app = Flask(__name__)

# 静的ファイル用のディレクトリを作成
UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    """メインページのレンダリング"""
    return render_template('index.html')

@app.route('/api/generate_graphs', methods=['POST'])
def generate_graphs():
    """グラフ生成APIエンドポイント"""
    # レスポンスの初期化
    response = {
        'success': False,
        'graph_filenames': {'price': None, 'drawdown': None},
        'error': None
    }
    
    try:
        # フォームデータの取得
        start_date = request.form.get('start_date', '')
        selected_symbol = request.form.get('symbol', 'sp500')
        
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
            response['graph_filenames']['price'] = price_filename
        
        # ドローダウングラフ
        fig_drawdown = calculator.plot_drawdown(start_date)
        if fig_drawdown:
            drawdown_filename = f'{selected_symbol}_drawdown_{timestamp}.png'
            plt.savefig(os.path.join(UPLOAD_FOLDER, drawdown_filename), dpi=300, bbox_inches='tight')
            plt.close()
            response['graph_filenames']['drawdown'] = drawdown_filename
        
        if not any(response['graph_filenames'].values()):
            response['error'] = "グラフの生成に失敗しました。"
        else:
            response['success'] = True
    
    except ValueError as e:
        response['error'] = "正しい日付形式（YYYY-MM-DD）で入力してください。"
    except Exception as e:
        response['error'] = f"エラーが発生しました: {str(e)}"
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)