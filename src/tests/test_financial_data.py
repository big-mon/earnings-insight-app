"""財務データ取得のテスト"""
import yfinance as yf
import time

def test_financial_data():
    """財務データの構造を確認"""
    ticker = "AAPL"
    stock = yf.Ticker(ticker)
    
    print("データ取得中...")
    time.sleep(5)  # データ取得のための待機

    # 基本情報の取得
    info = stock.info
    print("\n=== 基本情報 ===")
    print(f"会社名: {info.get('longName')}")
    print(f"セクター: {info.get('sector')}")
    print(f"時価総額: {info.get('marketCap')}")
    
    # 財務諸表の取得
    financials = stock.quarterly_financials
    balance_sheet = stock.quarterly_balance_sheet
    cashflow = stock.quarterly_cashflow

    # データ構造の確認
    print("\n=== 財務諸表のインデックス ===")
    if not financials.empty:
        print(financials.index.tolist())
    else:
        print("データが取得できませんでした")
    
    print("\n=== 貸借対照表のインデックス ===")
    if not balance_sheet.empty:
        print(balance_sheet.index.tolist())
    else:
        print("データが取得できませんでした")
    
    print("\n=== キャッシュフロー計算書のインデックス ===")
    if not cashflow.empty:
        print(cashflow.index.tolist())
    else:
        print("データが取得できませんでした")

    # データのサンプルを表示
    print("\n=== データサンプル ===")
    if not financials.empty:
        print("\n財務諸表の最初の行:")
        print(financials.iloc[0])
    
    if not balance_sheet.empty:
        print("\n貸借対照表の最初の行:")
        print(balance_sheet.iloc[0])
    
    if not cashflow.empty:
        print("\nキャッシュフロー計算書の最初の行:")
        print(cashflow.iloc[0])

    # より詳細なデータ表示
    print("\n=== 財務諸表 ===")
    income_stmt = stock.income_stmt
    balance = stock.balance_sheet
    cashflow = stock.cashflow
    
    if not income_stmt.empty:
        print("\n収益計算書の項目:")
        print(income_stmt.index.tolist())
        print("\n最新の収益データ:")
        print(income_stmt.iloc[:, 0])
    else:
        print("収益データが取得できませんでした")
    
    if not balance.empty:
        print("\n貸借対照表の項目:")
        print(balance.index.tolist())
        print("\n最新の貸借対照表データ:")
        print(balance.iloc[:, 0])
    else:
        print("貸借対照表データが取得できませんでした")
    
    if not cashflow.empty:
        print("\nキャッシュフロー計算書の項目:")
        print(cashflow.index.tolist())
        print("\n最新のキャッシュフローデータ:")
        print(cashflow.iloc[:, 0])
    else:
        print("キャッシュフローデータが取得できませんでした")

if __name__ == "__main__":
    test_financial_data()
