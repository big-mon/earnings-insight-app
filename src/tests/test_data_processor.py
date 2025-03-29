"""DataProcessorのテスト"""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from data.data_processor import DataProcessor
from data.data_fetcher import DataFetcher
from utils.constants import PERIOD_QUARTERLY, PERIOD_ANNUAL

class TestDataProcessor:
    """DataProcessorのテストクラス"""

    @pytest.fixture
    def mock_data_fetcher(self):
        """DataFetcherのモック"""
        mock = MagicMock(spec=DataFetcher)

        # 損益計算書のモック
        income_data = pd.DataFrame({
            '2023-12-31': [100000, 20000, 15000],
            '2023-09-30': [90000, 18000, 13000],
            '2023-06-30': [85000, 17000, 12000],
            '2023-03-31': [80000, 16000, 11000]
        }, index=['Total Revenue', 'Operating Income', 'Net Income'])

        # 貸借対照表のモック
        balance_data = pd.DataFrame({
            '2023-12-31': [500000, 300000, 200000],
            '2023-09-30': [480000, 290000, 190000],
            '2023-06-30': [460000, 280000, 180000],
            '2023-03-31': [440000, 270000, 170000]
        }, index=['Total Assets', 'Total Liabilities Net Minority Interest', 'Total Stockholder Equity'])

        # キャッシュフロー計算書のモック
        cash_flow_data = pd.DataFrame({
            '2023-12-31': [25000],
            '2023-09-30': [23000],
            '2023-06-30': [22000],
            '2023-03-31': [21000]
        }, index=['Operating Cash Flow'])

        # 配当データのモック
        dividends_data = pd.Series({
            pd.Timestamp('2023-12-15'): 1.0,
            pd.Timestamp('2023-09-15'): 1.0,
            pd.Timestamp('2023-06-15'): 1.0,
            pd.Timestamp('2023-03-15'): 1.0
        })

        # モックメソッドの設定
        mock.get_income_statement.return_value = income_data
        mock.get_balance_sheet.return_value = balance_data
        mock.get_cash_flow.return_value = cash_flow_data
        mock.get_shares_outstanding.return_value = 1000000
        mock.get_dividends.return_value = dividends_data

        return mock

    def test_process_financial_data(self, mock_data_fetcher):
        """財務データ処理のテスト"""
        processor = DataProcessor(mock_data_fetcher)

        # 四半期データのテスト
        financial_data = processor.process_financial_data(PERIOD_QUARTERLY)

        # 結果の検証
        assert financial_data is not None
        assert len(financial_data.dates) == 4
        assert len(financial_data.revenue) == 4
        assert len(financial_data.operating_income) == 4
        assert len(financial_data.net_income) == 4
        assert len(financial_data.operating_cash_flow) == 4
        assert len(financial_data.shares) == 4
        assert len(financial_data.eps) == 4
        assert len(financial_data.bps) == 4
        assert len(financial_data.operating_margin) == 4
        assert len(financial_data.operating_cash_flow_per_share) == 4

        # 計算結果の検証
        assert financial_data.eps[0] == financial_data.net_income[0] / financial_data.shares[0]
        assert financial_data.operating_margin[0] == financial_data.operating_income[0] / financial_data.revenue[0] * 100
        assert financial_data.operating_cash_flow_per_share[0] == financial_data.operating_cash_flow[0] / financial_data.shares[0]

        # 配当データの検証
        assert financial_data.dps is not None
        assert len(financial_data.dps) == 4

    def test_normalize_data(self, mock_data_fetcher):
        """データ正規化のテスト"""
        processor = DataProcessor(mock_data_fetcher)

        # テスト用のデータフレーム
        df = pd.DataFrame({
            '売上高': [100000, 90000, 85000, 80000],
            '営業利益': [20000, 18000, 17000, 16000],
            '純利益': [15000, 13000, 12000, 11000],
            '営業キャッシュフロー': [25000, 23000, 22000, 21000],
            '発行済株式数': [1000000, 1000000, 1000000, 1000000],
            'EPS': [0.015, 0.013, 0.012, 0.011],
            'BPS': [0.2, 0.19, 0.18, 0.17],
            '営業利益率': [20.0, 20.0, 20.0, 20.0],
            '1株あたり営業CF': [0.025, 0.023, 0.022, 0.021]
        }, index=pd.DatetimeIndex(['2023-12-31', '2023-09-30', '2023-06-30', '2023-03-31']))

        # 正規化の実行
        normalized = processor._normalize_data(df)

        # 結果の検証
        assert 'dates' in normalized
        assert 'revenue' in normalized
        assert 'operating_income' in normalized
        assert 'net_income' in normalized
        assert 'operating_cash_flow' in normalized
        assert 'shares' in normalized
        assert 'eps' in normalized
        assert 'bps' in normalized
        assert 'operating_margin' in normalized
        assert 'operating_cash_flow_per_share' in normalized

        assert len(normalized['dates']) == 4
        assert len(normalized['revenue']) == 4
        assert normalized['revenue'][0] == 100000
        assert normalized['operating_income'][0] == 20000

    def test_process_dividends(self, mock_data_fetcher):
        """配当データ処理のテスト"""
        processor = DataProcessor(mock_data_fetcher)

        # テスト用の正規化データ
        normalized_data = {
            'dates': pd.DatetimeIndex(['2023-12-31', '2023-09-30', '2023-06-30', '2023-03-31']),
            'revenue': [100000, 90000, 85000, 80000],
            'operating_income': [20000, 18000, 17000, 16000],
            'net_income': [15000, 13000, 12000, 11000],
            'operating_cash_flow': [25000, 23000, 22000, 21000],
            'shares': [1000000, 1000000, 1000000, 1000000],
            'eps': [0.015, 0.013, 0.012, 0.011],
            'bps': [0.2, 0.19, 0.18, 0.17],
            'operating_margin': [20.0, 20.0, 20.0, 20.0],
            'operating_cash_flow_per_share': [0.025, 0.023, 0.022, 0.021]
        }

        # 配当データ処理の実行
        result = processor._process_dividends(normalized_data, PERIOD_QUARTERLY)

        # 結果の検証
        assert 'dps' in result
        assert len(result['dps']) == 4
