"""財務データ処理ユーティリティ"""
from typing import Dict, Optional
import pandas as pd
from models.financial_data import FinancialData


def format_financial_value(value: float) -> str:
    """
    財務数値を見やすい形式にフォーマット
    Args:
        value (float): フォーマットする数値
    Returns:
        str: フォーマットされた文字列
    """
    if abs(value) >= 1_000_000_000:
        return f"¥{value/1_000_000_000:.1f}B"
    elif abs(value) >= 1_000_000:
        return f"¥{value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"¥{value/1_000:.1f}K"
    else:
        return f"¥{value:.2f}"


def get_normalized_financial_data(ticker: str, period: str = "quarterly") -> Optional[Dict]:
    """
    正規化された財務データを取得
    Args:
        ticker (str): ティッカーシンボル
        period (str): "quarterly"（四半期）または"annual"（年次）
    Returns:
        Dict: 正規化された財務データ
    """
    try:
        fd = FinancialData(ticker)
        data = fd.get_financial_data(period)

        if data is None:
            return None

        # 日付を変換（タイムゾーンを統一）
        dates = pd.to_datetime(data.index).tz_localize(None)

        # 配当データを取得
        dividends = fd.get_dividends()
        dps = None
        if dividends is not None and not dividends.empty:
            # 配当データのタイムゾーンを統一
            dividends.index = dividends.index.tz_localize(None)
            # 期間に応じて配当データを集計
            if period == "quarterly":
                dps = dividends.resample("QE").sum()
            else:
                dps = dividends.resample("YE").sum()
            # インデックスを財務データに合わせる
            dps = dps.reindex(dates, method="ffill")

        # データを正規化
        normalized_data = {
            "dates": dates,
            "revenue": data["売上高"].values,
            "operating_income": data["営業利益"].values,
            "net_income": data["純利益"].values,
            "operating_cash_flow": data["営業キャッシュフロー"].values,
            "shares": data["発行済株式数"].values,
            "eps": data["EPS"].values,
            "bps": data["BPS"].values,
            "operating_margin": data["営業利益率"].values,
            "operating_cash_flow_per_share": data["1株あたり営業CF"].values
        }

        # 配当データがある場合は追加
        if dps is not None and not dps.empty:
            normalized_data["dps"] = dps.values

        return normalized_data

    except Exception as e:
        print(f"財務データの正規化に失敗しました: {str(e)}")
        return None
