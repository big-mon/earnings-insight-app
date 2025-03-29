"""財務データ取得のテスト"""
import yfinance as yf
import pandas as pd
pd.set_option('display.max_rows', None)

def test_financial_data():
    """財務データの構造を確認"""
    ticker = "AAPL"
    stock = yf.Ticker(ticker)

    print("データ取得中...")

    # 基本情報の取得
    info = stock.info
    print("\n=== 基本情報 ===")
    print(f"会社名: {info.get('longName')}")
    print(f"セクター: {info.get('sector')}")
    print(f"時価総額: {info.get('marketCap')}")
    print(f"発行済株式数: {info.get('sharesOutstanding')}")

    # 利用可能なメソッドとプロパティの確認
    print("\n=== 利用可能なメソッドとプロパティ ===")
    print([attr for attr in dir(stock) if not attr.startswith('_')])

    # 財務諸表の取得（異なるメソッドを試す）
    print("\n=== 財務諸表（四半期） ===")
    try:
        financials = stock.financials
        print("\n財務諸表（financials）:")
        print(financials.head() if not financials.empty else "データなし")
    except Exception as e:
        print(f"financialsの取得エラー: {str(e)}")

    try:
        quarterly = stock.quarterly_financials
        print("\n四半期財務諸表（quarterly_financials）:")
        print(quarterly.head() if not quarterly.empty else "データなし")
    except Exception as e:
        print(f"quarterly_financialsの取得エラー: {str(e)}")

    try:
        income = stock.income_stmt
        print("\n損益計算書（income_stmt）:")
        print(income.head() if not income.empty else "データなし")
    except Exception as e:
        print(f"income_stmtの取得エラー: {str(e)}")

    try:
        quarterly_income = stock.quarterly_income_stmt
        print("\n四半期損益計算書（quarterly_income_stmt）:")
        print(quarterly_income.head() if not quarterly_income.empty else "データなし")
    except Exception as e:
        print(f"quarterly_income_stmtの取得エラー: {str(e)}")

    # キャッシュフロー計算書
    print("\n=== キャッシュフロー計算書 ===")
    try:
        cashflow = stock.cashflow
        print("\nキャッシュフロー計算書（cashflow）:")
        print(cashflow.head() if not cashflow.empty else "データなし")
    except Exception as e:
        print(f"cashflowの取得エラー: {str(e)}")

    # 貸借対照表
    print("\n=== 貸借対照表 ===")
    try:
        balance = stock.balance_sheet
        print("\n貸借対照表（balance_sheet）:")
        print(balance.head() if not balance.empty else "データなし")
    except Exception as e:
        print(f"balance_sheetの取得エラー: {str(e)}")

if __name__ == "__main__":
    test_financial_data()
