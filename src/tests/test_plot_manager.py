"""PlotManagerのテスト"""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from data.plot_manager import PlotManager
from utils.models import ChartConfig, FinancialDataModel


class TestPlotManager:
    """PlotManagerのテストクラス"""

    @pytest.fixture
    def sample_financial_data(self):
        """サンプル財務データモデル"""
        data = {
            "dates": [
                datetime(2023, 12, 31),
                datetime(2023, 9, 30),
                datetime(2023, 6, 30),
                datetime(2023, 3, 31)
            ],
            "revenue": [100000, 90000, 85000, 80000],
            "operating_income": [20000, 18000, 17000, 16000],
            "net_income": [15000, 13000, 12000, 11000],
            "operating_cash_flow": [25000, 23000, 22000, 21000],
            "shares": [1000000, 1000000, 1000000, 1000000],
            "eps": [0.015, 0.013, 0.012, 0.011],
            "bps": [0.2, 0.19, 0.18, 0.17],
            "operating_margin": [20.0, 20.0, 20.0, 20.0],
            "operating_cash_flow_per_share": [0.025, 0.023, 0.022, 0.021],
            "dps": [0.01, 0.01, 0.01, 0.01]
        }
        return FinancialDataModel(data)

    def test_create_financial_chart(self, sample_financial_data):
        """財務チャート作成のテスト"""
        # テスト用のチャート設定
        config = ChartConfig(
            title="テストチャート",
            y1_title="テスト第1軸",
            primary_data={
                "テストデータ1": [100, 90, 80, 70],
                "テストデータ2": [50, 45, 40, 35]
            },
            y2_title="テスト第2軸",
            secondary_data={
                "テストデータ3": [10, 9, 8, 7],
                "発行済株式数": [1000, 1000, 1000, 1000]
            }
        )
        
        # チャート作成
        fig = PlotManager.create_financial_chart(
            dates=sample_financial_data.dates,
            config=config
        )
        
        # 結果の検証
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 4  # 4つのトレースがあることを確認
        
        # レイアウトの検証
        assert fig.layout.title.text == "テストチャート"
        assert fig.layout.yaxis.title.text == "テスト第1軸"
        assert fig.layout.yaxis2.title.text == "テスト第2軸"

    def test_create_performance_chart(self, sample_financial_data):
        """業績確認チャート作成のテスト"""
        fig = PlotManager.create_performance_chart(sample_financial_data)
        
        # 結果の検証
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 4  # 売上高、営業利益、純利益、営業利益率の4つのトレース
        
        # レイアウトの検証
        assert fig.layout.title.text == "業績確認"
        assert fig.layout.yaxis.title.text == "金額"
        assert fig.layout.yaxis2.title.text == "営業利益率 (%)"

    def test_create_per_share_chart(self, sample_financial_data):
        """1株当たりの価値チャート作成のテスト"""
        fig = PlotManager.create_per_share_chart(sample_financial_data)
        
        # 結果の検証
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 4  # EPS、BPS、DPS、発行済株式数の4つのトレース
        
        # レイアウトの検証
        assert fig.layout.title.text == "1株当たりの価値"
        assert fig.layout.yaxis.title.text == "金額"
        assert fig.layout.yaxis2.title.text == "発行済株式数"

    def test_create_earning_power_chart(self, sample_financial_data):
        """稼ぐ力チャート作成のテスト"""
        fig = PlotManager.create_earning_power_chart(sample_financial_data)
        
        # 結果の検証
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 4  # 営業利益、営業CF、EPS、1株あたり営業CFの4つのトレース
        
        # レイアウトの検証
        assert fig.layout.title.text == "稼ぐ力"
        assert fig.layout.yaxis.title.text == "金額"
        assert fig.layout.yaxis2.title.text == "1株当たり金額"
