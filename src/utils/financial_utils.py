"""財務データ関連のユーティリティ関数"""
from typing import Dict, Optional, Union
import pandas as pd
from models.financial_data import FinancialData


def format_financial_value(value: Union[int, float]) -> str:
    """
    財務数値を見やすい形式にフォーマット
    Args:
        value (Union[int, float]): フォーマットする数値
    Returns:
        str: フォーマットされた文字列
    """
    if abs(value) >= 1_000_000_000_000:
        return f"{value/1_000_000_000_000:.1f}兆円"
    elif abs(value) >= 100_000_000:
        return f"{value/100_000_000:.1f}億円"
    elif abs(value) >= 10000:
        return f"{value/10000:.1f}万円"
    else:
        return f"{value:,.0f}円"


def get_normalized_financial_data(ticker: str, period: str = "quarterly") -> Optional[Dict]:
    """
    正規化された財務データを取得
    Args:
        ticker (str): 銘柄コード
        period (str): "quarterly"（四半期）または"annual"（年次）
    Returns:
        Dict: 正規化された財務データ
    """
    try:
        fd = FinancialData(ticker)
        data = fd.get_financial_data(period)
        if data is None:
            return None

        # 配当データの取得
        dividends = fd.get_dividends()
        if dividends is not None:
            # 同じ期間の配当を合計
            if period == "quarterly":
                dividends = dividends.resample("Q").sum()
            else:
                dividends = dividends.resample("Y").sum()
            data["DPS"] = dividends

        # 日付をインデックスとして使用
        result = {
            "dates": data.index.strftime("%Y-%m-%d").tolist(),
            "revenue": data["売上高"].tolist(),
            "operating_income": data["営業利益"].tolist(),
            "net_income": data["純利益"].tolist(),
            "operating_cash_flow": data["営業キャッシュフロー"].tolist(),
            "eps": data["EPS"].tolist(),
            "bps": data["BPS"].tolist(),
            "dps": data["DPS"].tolist() if "DPS" in data else None
        }

        return result

    except Exception as e:
        print(f"データの正規化中にエラーが発生しました: {str(e)}")
        return None
