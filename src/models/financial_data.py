"""財務データ取得モジュール"""
from typing import Dict, List, Optional, Union
import yfinance as yf
import pandas as pd


class FinancialData:
    """財務データ取得クラス"""

    def __init__(self, ticker: str):
        """
        初期化
        Args:
            ticker (str): 銘柄コード（例: "7203.T"）
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_financial_data(self, period: str = "quarterly") -> Optional[pd.DataFrame]:
        """
        財務データを取得
        Args:
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            pd.DataFrame: 財務データ
        """
        try:
            # 財務諸表の取得
            income = self.stock.income_stmt if period == "annual" else self.stock.quarterly_income_stmt
            balance = self.stock.balance_sheet if period == "annual" else self.stock.quarterly_balance_sheet
            cash = self.stock.cashflow if period == "annual" else self.stock.quarterly_cashflow

            if income.empty or balance.empty or cash.empty:
                print(f"財務データが不完全です: income={not income.empty}, balance={not balance.empty}, cash={not cash.empty}")
                return None

            # 必要なデータを抽出
            data = {
                "売上高": income.loc["Total Revenue"] if "Total Revenue" in income.index else None,
                "営業利益": income.loc["Operating Income"] if "Operating Income" in income.index else None,
                "純利益": income.loc["Net Income"] if "Net Income" in income.index else None,
                "営業キャッシュフロー": cash.loc["Operating Cash Flow"] if "Operating Cash Flow" in cash.index else None,
            }

            # 株式数の取得（infoから取得）
            try:
                shares = self.stock.info.get("sharesOutstanding")
                if shares:
                    # 全期間で同じ株式数を使用
                    data["発行済株式数"] = pd.Series([shares] * len(data["売上高"].index), index=data["売上高"].index)
                else:
                    print("発行済株式数が取得できません")
                    return None
            except Exception as e:
                print(f"株式数の取得に失敗しました: {str(e)}")
                return None

            # Noneの値をチェック
            if any(v is None for v in data.values()):
                missing_items = [k for k, v in data.items() if v is None]
                print(f"以下の項目が取得できませんでした: {', '.join(missing_items)}")
                return None

            # データフレームに変換
            df = pd.DataFrame(data)

            # 一株あたり指標の計算
            df["EPS"] = df["純利益"] / df["発行済株式数"]

            # BPSの計算（総資産 - 総負債）/ 発行済株式数
            total_assets = balance.loc["Total Assets"] if "Total Assets" in balance.index else None
            total_liabilities = balance.loc["Total Liabilities Net Minority Interest"] if "Total Liabilities Net Minority Interest" in balance.index else None

            if total_assets is not None and total_liabilities is not None:
                df["BPS"] = (total_assets - total_liabilities) / df["発行済株式数"]
            else:
                print("BPSの計算に必要なデータが取得できません")
                return None

            return df

        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            return None

    def get_dividends(self) -> Optional[pd.Series]:
        """
        配当データを取得
        Returns:
            pd.Series: 配当データ
        """
        try:
            dividends = self.stock.dividends
            if dividends.empty:
                return None
            return dividends
        except Exception as e:
            print(f"配当データの取得に失敗しました: {str(e)}")
            return None
