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
            if period == "quarterly":
                financials = self.stock.quarterly_financials
                balance_sheet = self.stock.quarterly_balance_sheet
                cashflow = self.stock.quarterly_cashflow
            else:
                financials = self.stock.financials
                balance_sheet = self.stock.balance_sheet
                cashflow = self.stock.cashflow

            if financials.empty or balance_sheet.empty or cashflow.empty:
                raise ValueError(f"財務データが取得できません: {self.ticker}")

            # 必要なデータを抽出
            data = {
                "売上高": financials.loc["Total Revenue"],
                "営業利益": financials.loc["Operating Income"],
                "純利益": financials.loc["Net Income"],
                "営業キャッシュフロー": cashflow.loc["Operating Cash Flow"],
                "発行済株式数": balance_sheet.loc["Share Issued"],
            }

            # データフレームに変換
            df = pd.DataFrame(data)

            # 一株あたり指標の計算
            df["EPS"] = df["純利益"] / df["発行済株式数"]
            df["BPS"] = balance_sheet.loc["Total Stockholder Equity"] / df["発行済株式数"]

            # インデックスを日付型に変換
            df.index = pd.to_datetime(df.index)

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
