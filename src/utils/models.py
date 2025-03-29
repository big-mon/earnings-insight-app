"""財務データの型定義"""
from typing import Dict, List, Optional, Union
import pandas as pd
from datetime import datetime


class FinancialDataModel:
    """財務データモデル"""
    dates: List[datetime]
    revenue: List[float]
    operating_income: List[float]
    net_income: List[float]
    operating_cash_flow: List[float]
    shares: List[int]
    eps: List[float]
    bps: List[float]
    operating_margin: List[float]
    operating_cash_flow_per_share: List[float]
    dps: Optional[List[float]] = None

    def __init__(self, data: Dict[str, List]):
        """
        初期化
        Args:
            data (Dict[str, List]): 財務データ辞書
        """
        self.dates = data.get("dates", [])
        self.revenue = data.get("revenue", [])
        self.operating_income = data.get("operating_income", [])
        self.net_income = data.get("net_income", [])
        self.operating_cash_flow = data.get("operating_cash_flow", [])
        self.shares = data.get("shares", [])
        self.eps = data.get("eps", [])
        self.bps = data.get("bps", [])
        self.operating_margin = data.get("operating_margin", [])
        self.operating_cash_flow_per_share = data.get("operating_cash_flow_per_share", [])
        self.dps = data.get("dps", None)

    def to_dict(self) -> Dict[str, List]:
        """
        辞書形式に変換
        Returns:
            Dict[str, List]: 財務データ辞書
        """
        result = {
            "dates": self.dates,
            "revenue": self.revenue,
            "operating_income": self.operating_income,
            "net_income": self.net_income,
            "operating_cash_flow": self.operating_cash_flow,
            "shares": self.shares,
            "eps": self.eps,
            "bps": self.bps,
            "operating_margin": self.operating_margin,
            "operating_cash_flow_per_share": self.operating_cash_flow_per_share
        }
        
        if self.dps is not None:
            result["dps"] = self.dps
            
        return result


class ChartConfig:
    """チャート設定"""
    title: str
    y1_title: str
    y2_title: Optional[str]
    primary_data: Dict[str, List[float]]
    secondary_data: Optional[Dict[str, List[float]]]
    
    def __init__(
        self,
        title: str,
        y1_title: str,
        primary_data: Dict[str, List[float]],
        y2_title: Optional[str] = None,
        secondary_data: Optional[Dict[str, List[float]]] = None
    ):
        """
        初期化
        Args:
            title (str): チャートタイトル
            y1_title (str): 第1軸のタイトル
            primary_data (Dict[str, List[float]]): 第1軸のデータ
            y2_title (Optional[str], optional): 第2軸のタイトル. Defaults to None.
            secondary_data (Optional[Dict[str, List[float]]], optional): 第2軸のデータ. Defaults to None.
        """
        self.title = title
        self.y1_title = y1_title
        self.y2_title = y2_title
        self.primary_data = primary_data
        self.secondary_data = secondary_data
