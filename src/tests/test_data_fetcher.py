"""DataFetcherのテスト"""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from data.data_fetcher import DataFetcher
from utils.constants import PERIOD_QUARTERLY, PERIOD_ANNUAL

class TestDataFetcher:
    """DataFetcherのテストクラス"""

    @pytest.fixture
    def mock_ticker(self):
        """Tickerのモック"""
        mock = MagicMock()

        # 損益計算書のモック
        mock.income_stmt = pd.DataFrame({
            '2023-12-31': [100000, 20000, 15000],
            '2023-09-30': [90000, 18000, 13000],
            '2023-06-30': [85000, 17000, 12000],
            '2023-03-31': [80000, 16000, 11000]
        }, index=['Total Revenue', 'Operating Income', 'Net Income'])

        mock.quarterly_income_stmt = mock.income_stmt

        # 貸借対照表のモック
        mock.balance_sheet = pd.DataFrame({
            '2023-12-31': [500000, 300000, 200000],
            '2023-09-30': [480000, 290000, 190000],
            '2023-06-30': [460000, 280000, 180000],
            '2023-03-31': [440000, 270000, 170000]
        }, index=['Total Assets', 'Total Liabilities Net Minority Interest', 'Total Stockholder Equity'])

        mock.quarterly_balance_sheet = mock.balance_sheet

        # キャッシュフロー計算書のモック
        mock.cashflow = pd.DataFrame({
            '2023-12-31': [25000],
            '2023-09-30': [23000],
            '2023-06-30': [22000],
            '2023-03-31': [21000]
        }, index=['Operating Cash Flow'])

        mock.quarterly_cashflow = mock.cashflow

        # 株式数のモック
        mock.info = {'sharesOutstanding': 1000000}

        # 配当のモック
        mock.dividends = pd.Series({
            pd.Timestamp('2023-12-15'): 1.0,
            pd.Timestamp('2023-09-15'): 1.0,
            pd.Timestamp('2023-06-15'): 1.0,
            pd.Timestamp('2023-03-15'): 1.0
        })

        return mock

    @patch('yfinance.Ticker')
    def test_get_income_statement(self, mock_yf_ticker, mock_ticker):
        """損益計算書の取得テスト"""
        mock_yf_ticker.return_value = mock_ticker

        # 四半期データのテスト
        fetcher = DataFetcher('AAPL')
        income_q = fetcher.get_income_statement(PERIOD_QUARTERLY)
        assert income_q is not None
        assert 'Total Revenue' in income_q.index
        assert 'Operating Income' in income_q.index
        assert 'Net Income' in income_q.index

        # 年次データのテスト
        income_a = fetcher.get_income_statement(PERIOD_ANNUAL)
        assert income_a is not None
        assert 'Total Revenue' in income_a.index

    @patch('yfinance.Ticker')
    def test_get_balance_sheet(self, mock_yf_ticker, mock_ticker):
        """貸借対照表の取得テスト"""
        mock_yf_ticker.return_value = mock_ticker

        fetcher = DataFetcher('AAPL')
        balance = fetcher.get_balance_sheet()
        assert balance is not None
        assert 'Total Assets' in balance.index
        assert 'Total Liabilities Net Minority Interest' in balance.index
        assert 'Total Stockholder Equity' in balance.index

    @patch('yfinance.Ticker')
    def test_get_cash_flow(self, mock_yf_ticker, mock_ticker):
        """キャッシュフロー計算書の取得テスト"""
        mock_yf_ticker.return_value = mock_ticker

        fetcher = DataFetcher('AAPL')
        cash_flow = fetcher.get_cash_flow()
        assert cash_flow is not None
        assert 'Operating Cash Flow' in cash_flow.index

    @patch('yfinance.Ticker')
    def test_get_shares_outstanding(self, mock_yf_ticker, mock_ticker):
        """発行済株式数の取得テスト"""
        mock_yf_ticker.return_value = mock_ticker

        fetcher = DataFetcher('AAPL')
        shares = fetcher.get_shares_outstanding()
        assert shares == 1000000

    @patch('yfinance.Ticker')
    def test_get_dividends(self, mock_yf_ticker, mock_ticker):
        """配当データの取得テスト"""
        mock_yf_ticker.return_value = mock_ticker

        fetcher = DataFetcher('AAPL')
        dividends = fetcher.get_dividends()
        assert dividends is not None
        assert len(dividends) == 4
        assert dividends.iloc[0] == 1.0
