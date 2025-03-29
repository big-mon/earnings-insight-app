"""財務データ取得モジュール"""
from typing import Dict, List, Optional, Union
import yfinance as yf
import pandas as pd
from utils.constants import (
    YF_REVENUE, YF_OPERATING_INCOME, YF_NET_INCOME, YF_OPERATING_CASH_FLOW,
    YF_STOCKHOLDER_EQUITY, YF_TOTAL_ASSETS, YF_TOTAL_LIABILITIES,
    PERIOD_ANNUAL, PERIOD_QUARTERLY
)


class DataFetcher:
    """財務データ取得クラス"""

    def __init__(self, ticker: str):
        """
        初期化
        Args:
            ticker (str): 銘柄コード（例: "AAPL"）
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_income_statement(self, period: str = PERIOD_QUARTERLY) -> Optional[pd.DataFrame]:
        """
        損益計算書を取得
        Args:
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            Optional[pd.DataFrame]: 損益計算書
        """
        try:
            income = self.stock.income_stmt if period == PERIOD_ANNUAL else self.stock.quarterly_income_stmt
            if income.empty:
                print(f"損益計算書が取得できませんでした: {self.ticker}")
                return None
            return income
        except Exception as e:
            print(f"損益計算書の取得に失敗しました: {str(e)}")
            return None

    def get_balance_sheet(self, period: str = PERIOD_QUARTERLY) -> Optional[pd.DataFrame]:
        """
        貸借対照表を取得
        Args:
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            Optional[pd.DataFrame]: 貸借対照表
        """
        try:
            balance = self.stock.balance_sheet if period == PERIOD_ANNUAL else self.stock.quarterly_balance_sheet
            if balance.empty:
                print(f"貸借対照表が取得できませんでした: {self.ticker}")
                return None
            return balance
        except Exception as e:
            print(f"貸借対照表の取得に失敗しました: {str(e)}")
            return None

    def get_cash_flow(self, period: str = PERIOD_QUARTERLY) -> Optional[pd.DataFrame]:
        """
        キャッシュフロー計算書を取得
        Args:
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            Optional[pd.DataFrame]: キャッシュフロー計算書
        """
        try:
            cash = self.stock.cashflow if period == PERIOD_ANNUAL else self.stock.quarterly_cashflow
            if cash.empty:
                print(f"キャッシュフロー計算書が取得できませんでした: {self.ticker}")
                return None
            return cash
        except Exception as e:
            print(f"キャッシュフロー計算書の取得に失敗しました: {str(e)}")
            return None

    def get_shares_outstanding(self) -> Optional[int]:
        """
        発行済株式数を取得
        Returns:
            Optional[int]: 発行済株式数
        """
        try:
            shares = self.stock.info.get("sharesOutstanding")
            if not shares:
                print(f"発行済株式数が取得できませんでした: {self.ticker}")
                return None
            return shares
        except Exception as e:
            print(f"発行済株式数の取得に失敗しました: {str(e)}")
            return None

    def get_dividends(self) -> Optional[pd.Series]:
        """
        配当データを取得
        Returns:
            Optional[pd.Series]: 配当データ
        """
        try:
            dividends = self.stock.dividends
            if dividends.empty:
                print(f"配当データが取得できませんでした: {self.ticker}")
                return None
            return dividends
        except Exception as e:
            print(f"配当データの取得に失敗しました: {str(e)}")
            return None
