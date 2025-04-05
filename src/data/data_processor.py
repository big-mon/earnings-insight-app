"""財務データ処理モジュール"""
from typing import Dict, List, Optional, Union
import pandas as pd
from datetime import datetime
from data.data_fetcher import DataFetcher
from utils.models import FinancialDataModel
from utils.constants import (
    PERIOD_QUARTERLY, PERIOD_ANNUAL,
    YF_REVENUE, YF_OPERATING_INCOME, YF_NET_INCOME, YF_OPERATING_CASH_FLOW,
    YF_STOCKHOLDER_EQUITY, YF_TOTAL_ASSETS, YF_TOTAL_LIABILITIES
)


class DataProcessor:
    """財務データ処理クラス"""

    def __init__(self, data_fetcher: DataFetcher):
        """
        初期化
        Args:
            data_fetcher (DataFetcher): データ取得クラスのインスタンス
        """
        self.data_fetcher = data_fetcher

    def process_financial_data(self, period: str = PERIOD_QUARTERLY) -> Optional[FinancialDataModel]:
        """
        財務データを処理
        Args:
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            Optional[FinancialDataModel]: 処理済み財務データモデル
        """
        try:
            # 財務諸表の取得
            income = self.data_fetcher.get_income_statement(period)
            balance = self.data_fetcher.get_balance_sheet(period)
            cash = self.data_fetcher.get_cash_flow(period)
            shares = self.data_fetcher.get_shares_outstanding()

            # データの検証
            if income is None or balance is None or cash is None or shares is None:
                print("財務データが不完全です")
                return None

            # 必要なデータを抽出
            data = {
                "売上高": income.loc[YF_REVENUE] if YF_REVENUE in income.index else None,
                "営業利益": income.loc[YF_OPERATING_INCOME] if YF_OPERATING_INCOME in income.index else None,
                "純利益": income.loc[YF_NET_INCOME] if YF_NET_INCOME in income.index else None,
                "営業キャッシュフロー": cash.loc[YF_OPERATING_CASH_FLOW] if YF_OPERATING_CASH_FLOW in cash.index else None,
            }

            # Noneの値をチェック
            if any(v is None for v in data.values()):
                missing_items = [k for k, v in data.items() if v is None]
                print(f"以下の項目が取得できませんでした: {', '.join(missing_items)}")
                return None

            # 株式数の設定（各時点の値を取得）
            shares_data = self.data_fetcher.get_shares_outstanding_history(period)
            if shares_data is None:
                print("株式数の履歴データが取得できませんでした")
                return None
            
            # 株式数データのインデックスをfinancial dataのインデックスに合わせる
            shares_data = shares_data.reindex(data["売上高"].index, method="ffill")
            data["発行済株式数"] = shares_data

            # データフレームに変換
            df = pd.DataFrame(data)

            # 一株あたり指標の計算
            df["EPS"] = df["純利益"] / df["発行済株式数"]
            df["営業利益率"] = df["営業利益"] / df["売上高"] * 100
            df["1株あたり営業CF"] = df["営業キャッシュフロー"] / df["発行済株式数"]

            # BPSの計算（純資産 / 発行済株式数）
            stockholder_equity = balance.loc[YF_STOCKHOLDER_EQUITY] if YF_STOCKHOLDER_EQUITY in balance.index else None
            if stockholder_equity is not None:
                df["BPS"] = stockholder_equity / df["発行済株式数"]
            else:
                # 代替計算：（総資産 - 総負債）/ 発行済株式数
                total_assets = balance.loc[YF_TOTAL_ASSETS] if YF_TOTAL_ASSETS in balance.index else None
                total_liabilities = balance.loc[YF_TOTAL_LIABILITIES] if YF_TOTAL_LIABILITIES in balance.index else None

                if total_assets is not None and total_liabilities is not None:
                    df["BPS"] = (total_assets - total_liabilities) / df["発行済株式数"]
                else:
                    print("BPSの計算に必要なデータが取得できません")
                    return None

            # 正規化データの作成
            normalized_data = self._normalize_data(df)

            # 配当データの処理
            normalized_data = self._process_dividends(normalized_data, period)

            return FinancialDataModel(normalized_data)

        except Exception as e:
            print(f"財務データの処理中にエラーが発生しました: {str(e)}")
            return None

    def _normalize_data(self, df: pd.DataFrame) -> Dict:
        """
        データを正規化
        Args:
            df (pd.DataFrame): 財務データフレーム
        Returns:
            Dict: 正規化されたデータ（日付昇順でソート済み）
        """
        # 日付を変換（タイムゾーンを統一）
        dates = pd.to_datetime(df.index).tz_localize(None)
        
        # 日付でソート
        df = df.sort_index(ascending=True)
        dates = dates.sort_values()

        # データを正規化
        normalized_data = {
            "dates": dates,
            "revenue": df["売上高"].values,
            "operating_income": df["営業利益"].values,
            "net_income": df["純利益"].values,
            "operating_cash_flow": df["営業キャッシュフロー"].values,
            "shares": df["発行済株式数"].values,
            "eps": df["EPS"].values,
            "bps": df["BPS"].values,
            "operating_margin": df["営業利益率"].values,
            "operating_cash_flow_per_share": df["1株あたり営業CF"].values
        }

        return normalized_data

    def _process_dividends(self, normalized_data: Dict, period: str) -> Dict:
        """
        配当データを処理
        Args:
            normalized_data (Dict): 正規化されたデータ
            period (str): "quarterly"（四半期）または"annual"（年次）
        Returns:
            Dict: 配当データを含む正規化されたデータ
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
