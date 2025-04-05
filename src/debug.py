"""yFinanceデータ確認用デバッグページ

このモジュールは、yFinanceから取得したデータを確認するためのデバッグページを提供します。
指定したティッカーシンボルで取得可能なデータを閲覧できます。
"""
import streamlit as st
import pandas as pd
import yfinance as yf
from data.data_fetcher import DataFetcher
from utils.constants import (
    PERIOD_QUARTERLY, PERIOD_ANNUAL,
    APP_ICON
)


def main():
    """デバッグページのメイン関数"""
    st.set_page_config(
        page_title="yFinanceデータ確認ツール",
        page_icon=APP_ICON,
        layout="wide"
    )

    st.title("yFinanceデータ確認ツール")
    st.write("指定したティッカーシンボルのyFinanceデータを確認できます。")

    # サイドバーの設定
    with st.sidebar:
        st.header("設定")
        ticker = st.text_input("ティッカーシンボルを入力してください（例：AAPL）", "AAPL")

    if ticker:
        try:
            # ローディング表示
            with st.spinner(f"'{ticker}'のデータを取得中..."):
                # yfinanceからデータを取得
                stock = yf.Ticker(ticker)
                data_fetcher = DataFetcher(ticker)

            try:
                # 配当、株式分割、その他アクションの履歴データ
                st.header("Ticker.actions")
                st.dataframe(stock.actions)
            except Exception as e:
                st.error(f"actionsの取得に失敗しました: {str(e)}")

            try:
                # アナリストの推奨価格
                st.header("Ticker.analyst_price_targets")
                st.dataframe(stock.analyst_price_targets)
            except Exception as e:
                st.error(f"analyst_price_targetsの取得に失敗しました: {str(e)}")

            try:
                # 貸借対照表
                st.header("Ticker.balance_sheet")
                st.dataframe(stock.balance_sheet)
            except Exception as e:
                st.error(f"balance_sheetの取得に失敗しました: {str(e)}")

            try:
                # 貸借対照表
                st.header("Ticker.balancesheet")
                st.dataframe(stock.balancesheet)
            except Exception as e:
                st.error(f"balancesheetの取得に失敗しました: {str(e)}")

            try:
                # 基本的な企業情報
                st.header("Ticker.basic_info")
                st.dataframe(stock.basic_info)
            except Exception as e:
                st.error(f"basic_infoの取得に失敗しました: {str(e)}")

            try:
                # 決算日、配当日、その他イベントの日程情報
                st.header("Ticker.calendar")
                st.dataframe(stock.calendar)
            except Exception as e:
                st.error(f"calendarの取得に失敗しました: {str(e)}")

            try:
                # キャピタルゲイン
                st.header("Ticker.capital_gains")
                st.dataframe(stock.capital_gains)
            except Exception as e:
                st.error(f"capital_gainsの取得に失敗しました: {str(e)}")

            try:
                # キャッシュフロー計算書
                st.header("Ticker.cash_flow")
                st.dataframe(stock.cash_flow)
            except Exception as e:
                st.error(f"cash_flowの取得に失敗しました: {str(e)}")

            try:
                # キャッシュフロー計算書
                st.header("Ticker.cashflow")
                st.dataframe(stock.cashflow)
            except Exception as e:
                st.error(f"cashflowの取得に失敗しました: {str(e)}")

            try:
                # 配当データ
                st.header("Ticker.dividends")
                st.dataframe(stock.dividends)
            except Exception as e:
                st.error(f"dividendsの取得に失敗しました: {str(e)}")

            try:
                # 決算データ
                st.header("Ticker.earnings")
                st.dataframe(stock.earnings)
            except Exception as e:
                st.error(f"earningsの取得に失敗しました: {str(e)}")

            try:
                # 決算日
                st.header("Ticker.earnings_dates")
                st.dataframe(stock.earnings_dates)
            except Exception as e:
                st.error(f"earnings_datesの取得に失敗しました: {str(e)}")

            try:
                # アナリストによる決算見通し
                st.header("Ticker.earnings_estimate")
                st.dataframe(stock.earnings_estimate)
            except Exception as e:
                st.error(f"earnings_estimateの取得に失敗しました: {str(e)}")

            try:
                # 決算実績
                st.header("Ticker.earnings_history")
                st.dataframe(stock.earnings_history)
            except Exception as e:
                st.error(f"earnings_historyの取得に失敗しました: {str(e)}")

            try:
                # EPSの変更履歴
                st.header("Ticker.eps_revisions")
                st.dataframe(stock.eps_revisions)
            except Exception as e:
                st.error(f"eps_revisionsの取得に失敗しました: {str(e)}")

            try:
                # EPSの推移
                st.header("Ticker.eps_trend")
                st.dataframe(stock.eps_trend)
            except Exception as e:
                st.error(f"eps_trendの取得に失敗しました: {str(e)}")

            try:
                # 基本市場情報
                st.header("Ticker.fast_info")
                st.dataframe(stock.fast_info)
            except Exception as e:
                st.error(f"fast_infoの取得に失敗しました: {str(e)}")

            try:
                # 損益計算書
                st.header("Ticker.financials")
                st.dataframe(stock.financials)
            except Exception as e:
                st.error(f"financialsの取得に失敗しました: {str(e)}")

            try:
                # ファンド関連
                st.header("Ticker.funds_data")
                st.dataframe(stock.funds_data)
            except Exception as e:
                st.error(f"funds_dataの取得に失敗しました: {str(e)}")

            try:
                # 売上や利益の成長率の見通し
                st.header("Ticker.growth_estimates")
                st.dataframe(stock.growth_estimates)
            except Exception as e:
                st.error(f"growth_estimatesの取得に失敗しました: {str(e)}")

            try:
                # 株価時系列データ
                st.header("Ticker.history_metadata")
                st.dataframe(stock.history_metadata)
            except Exception as e:
                st.error(f"history_metadataの取得に失敗しました: {str(e)}")

            try:
                # 損益計算書
                st.header("Ticker.income_stmt")
                st.dataframe(stock.income_stmt)
            except Exception as e:
                st.error(f"income_stmtの取得に失敗しました: {str(e)}")

            try:
                # 損益計算書
                st.header("Ticker.incomestmt")
                st.dataframe(stock.incomestmt)
            except Exception as e:
                st.error(f"incomestmtの取得に失敗しました: {str(e)}")

            try:
                # 企業情報
                st.header("Ticker.info")
                st.dataframe(stock.info)
            except Exception as e:
                st.error(f"infoの取得に失敗しました: {str(e)}")

            try:
                # インサイダー購入
                st.header("Ticker.insider_purchases")
                st.dataframe(stock.insider_purchases)
            except Exception as e:
                st.error(f"insider_purchasesの取得に失敗しました: {str(e)}")

            try:
                # インサイダーの保有情報
                st.header("Ticker.insider_roster_holders")
                st.dataframe(stock.insider_roster_holders)
            except Exception as e:
                st.error(f"insider_roster_holdersの取得に失敗しました: {str(e)}")

            try:
                # インサイダーの取引履歴
                st.header("Ticker.insider_transactions")
                st.dataframe(stock.insider_transactions)
            except Exception as e:
                st.error(f"insider_transactionsの取得に失敗しました: {str(e)}")

            try:
                # 機関投資家の保有状況
                st.header("Ticker.institutional_holders")
                st.dataframe(stock.institutional_holders)
            except Exception as e:
                st.error(f"institutional_holdersの取得に失敗しました: {str(e)}")

            try:
                # 国際証券識別番号
                st.header("Ticker.isin")
                st.dataframe(stock.isin)
            except Exception as e:
                st.error(f"isinの取得に失敗しました: {str(e)}")

            try:
                # 主要株主
                st.header("Ticker.major_holders")
                st.dataframe(stock.major_holders)
            except Exception as e:
                st.error(f"major_holdersの取得に失敗しました: {str(e)}")

            try:
                # 投資信託による保有情報
                st.header("Ticker.mutualfund_holders")
                st.dataframe(stock.mutualfund_holders)
            except Exception as e:
                st.error(f"mutualfund_holdersの取得に失敗しました: {str(e)}")

            try:
                # 関連ニュース記事
                st.header("Ticker.news")
                st.dataframe(stock.news)
            except Exception as e:
                st.error(f"newsの取得に失敗しました: {str(e)}")

            try:
                # オプションの満期日
                st.header("Ticker.options")
                st.dataframe(stock.options)
            except Exception as e:
                st.error(f"optionsの取得に失敗しました: {str(e)}")

            try:
                # アナリストの推奨
                st.header("Ticker.recommendations")
                st.dataframe(stock.recommendations)
            except Exception as e:
                st.error(f"recommendationsの取得に失敗しました: {str(e)}")

            try:
                # 推奨情報のサマリー
                st.header("Ticker.recommendations_summary")
                st.dataframe(stock.recommendations_summary)
            except Exception as e:
                st.error(f"recommendations_summaryの取得に失敗しました: {str(e)}")

            try:
                # 売上高に関する見通し
                st.header("Ticker.revenue_estimate")
                st.dataframe(stock.revenue_estimate)
            except Exception as e:
                st.error(f"revenue_estimateの取得に失敗しました: {str(e)}")

            try:
                # SECへの報告書
                st.header("Ticker.sec_filings")
                st.dataframe(stock.sec_filings)
            except Exception as e:
                st.error(f"sec_filingsの取得に失敗しました: {str(e)}")

            try:
                # 発行済株式数
                st.header("Ticker.shares")
                st.dataframe(stock.shares)
            except Exception as e:
                st.error(f"sharesの取得に失敗しました: {str(e)}")

            try:
                # 発行済株式数
                st.header("Ticker.get_shares()")
                st.dataframe(stock.get_shares())
            except Exception as e:
                st.error(f"get_sharesの取得に失敗しました: {str(e)}")

            try:
                # 発行済株式数
                st.header("Ticker.get_shares_full()")
                st.dataframe(stock.get_shares_full())
            except Exception as e:
                st.error(f"get_shares_fullの取得に失敗しました: {str(e)}")

            try:
                # 株式分割
                st.header("Ticker.splits")
                st.dataframe(stock.splits)
            except Exception as e:
                st.error(f"splitsの取得に失敗しました: {str(e)}")

            try:
                # ESG・サステナビリティに関する評価
                st.header("Ticker.sustainability")
                st.dataframe(stock.sustainability)
            except Exception as e:
                st.error(f"sustainabilityの取得に失敗しました: {str(e)}")

            try:
                st.header("Ticker.ttm_cash_flow")
                st.dataframe(stock.ttm_cash_flow)
            except Exception as e:
                st.error(f"ttm_cash_flowの取得に失敗しました: {str(e)}")

            try:
                st.header("Ticker.ttm_cashflow")
                st.dataframe(stock.ttm_cashflow)
            except Exception as e:
                st.error(f"ttm_cashflowの取得に失敗しました: {str(e)}")

            try:
                st.header("Ticker.ttm_financials")
                st.dataframe(stock.ttm_financials)
            except Exception as e:
                st.error(f"ttm_financialsの取得に失敗しました: {str(e)}")

            try:
                st.header("Ticker.ttm_income_stmt")
                st.dataframe(stock.ttm_income_stmt)
            except Exception as e:
                st.error(f"ttm_income_stmtの取得に失敗しました: {str(e)}")

            try:
                st.header("Ticker.ttm_incomestmt")
                st.dataframe(stock.ttm_incomestmt)
            except Exception as e:
                st.error(f"ttm_incomestmtの取得に失敗しました: {str(e)}")

            try:
                # アナリストによる格付けのアップ／ダウングレード
                st.header("Ticker.upgrades_downgrades")
                st.dataframe(stock.upgrades_downgrades)
            except Exception as e:
                st.error(f"upgrades_downgradesの取得に失敗しました: {str(e)}")

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
