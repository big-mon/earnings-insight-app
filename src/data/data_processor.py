"""財務データ処理モジュール"""
from typing import Dict, List, Optional, Union
import pandas as pd
from utils.constants import PERIOD_QUARTERLY, PERIOD_ANNUAL


class DataProcessor:
    """財務データ処理クラス"""

    def __init__(self, data_fetcher):
        """
        初期化
        Args:
            data_fetcher: データ取得クラスのインスタンス
        """
        self.data_fetcher = data_fetcher

    def process_financial_data(self, period: str = PERIOD_QUARTERLY) -> Optional[Dict[str, List]]:
        """
        財務データを処理
        Args:
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            Optional[Dict[str, List]]: 処理済み財務データ
        """
        # 財務諸表を取得
        income = self.data_fetcher.get_income_statement(period)
        balance = self.data_fetcher.get_balance_sheet(period)
        cash = self.data_fetcher.get_cash_flow(period)
        shares = self.data_fetcher.get_shares_outstanding()

        # データが取得できない場合はNoneを返す
        if income is None or balance is None or cash is None or shares is None:
            return None

        # 日付順に並び替え
        income = income.sort_index()
        balance = balance.sort_index()
        cash = cash.sort_index()

        # 共通の日付を取得
        dates = income.index.intersection(balance.index).intersection(cash.index)

        # データを正規化
        normalized_data = {
            "dates": dates,
            "revenue": income.loc[dates, "Total Revenue"],
            "operating_income": income.loc[dates, "Operating Income"],
            "net_income": income.loc[dates, "Net Income"],
            "operating_cash_flow": cash.loc[dates, "Operating Cash Flow"],
            "shares": pd.Series([shares] * len(dates), index=dates),
            "eps": income.loc[dates, "Net Income"] / shares,
            "bps": balance.loc[dates, "Stockholders Equity"] / shares,
            "operating_margin": income.loc[dates, "Operating Income"] / income.loc[dates, "Total Revenue"] * 100,
            "operating_cash_flow_per_share": cash.loc[dates, "Operating Cash Flow"] / shares,
        }

        # 配当データを処理
        normalized_data = self._process_dividends(normalized_data, period)

        return normalized_data

    def _process_dividends(self, normalized_data: Dict[str, List], period: str) -> Dict[str, List]:
        """
        配当データを処理
        Args:
            normalized_data (Dict[str, List]): 正規化済み財務データ
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            Dict[str, List]: 配当データを追加した財務データ
        """
        try:
            # 配当データを取得
            dividends = self.data_fetcher.get_dividends()
            if dividends is None:
                return normalized_data

            # 配当データのタイムゾーンを統一
            dividends.index = dividends.index.tz_localize(None)

            # 期間に応じて配当データを集計
            if period == PERIOD_QUARTERLY:
                dps = dividends.resample("QE").sum()
            else:
                # 年次の場合、各年の配当を合計
                dps = dividends.resample("YE").sum()

            # インデックスを財務データに合わせる
            dps = dps.reindex(normalized_data["dates"], method="ffill")

            # 配当データを追加
            if not dps.empty:
                normalized_data["dps"] = dps.values

            return normalized_data

        except Exception as e:
            print(f"配当データの処理中にエラーが発生しました: {str(e)}")
            return normalized_data