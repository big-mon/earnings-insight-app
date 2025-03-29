"""フォーマットユーティリティ"""
from typing import List, Optional
import pandas as pd
from datetime import datetime
from utils.constants import DATE_FORMAT

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

def format_dates(dates: List[datetime]) -> List[str]:
    """
    日付リストをフォーマット
    Args:
        dates (List[datetime]): 日付リスト
    Returns:
        List[str]: フォーマットされた日付リスト
    """
    return [pd.to_datetime(date).strftime(DATE_FORMAT) for date in dates]

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    パーセント値をフォーマット
    Args:
        value (float): フォーマットする数値
        decimal_places (int, optional): 小数点以下の桁数. Defaults to 1.
    Returns:
        str: フォーマットされた文字列
    """
    return f"{value:.{decimal_places}f}%"
