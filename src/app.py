"""財務データ可視化アプリケーション"""
import streamlit as st
from data.data_fetcher import DataFetcher
from data.data_processor import DataProcessor
from plots.plot_manager import PlotManager
from utils.constants import (
    PERIOD_QUARTERLY, PERIOD_ANNUAL,
    APP_TITLE, APP_DESCRIPTION, APP_ICON,
    ERROR_DATA_FETCH
)
from utils.formatting import format_financial_value


def main():
    """メインアプリケーション"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide"
    )

    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)

    # サイドバーの設定
    with st.sidebar:
        st.header("設定")
        ticker = st.text_input("ティッカーシンボルを入力してください（例：AAPL）", "AAPL")
        period = st.selectbox(
            "期間",
            [PERIOD_QUARTERLY, PERIOD_ANNUAL],
            format_func=lambda x: "四半期" if x == PERIOD_QUARTERLY else "年次"
        )

    if ticker:
        try:
            # ローディング表示
            with st.spinner(f"'{ticker}'の財務データを取得中..."):
                # データ取得と処理
                data_fetcher = DataFetcher(ticker)
                data_processor = DataProcessor(data_fetcher)
                financial_data = data_processor.process_financial_data(period)

            if financial_data is None:
                st.error(ERROR_DATA_FETCH)
                return

            # プロット管理クラスを使用してチャートを作成
            plot_manager = PlotManager()

            # 業績確認グラフ
            st.subheader("業績確認グラフ")
            st.plotly_chart(
                plot_manager.create_performance_chart(financial_data),
                use_container_width=True
            )

            # 1株当たりの価値グラフ
            st.subheader("1株当たりの価値グラフ")
            cols = st.columns(2)
            with cols[0]:
                st.plotly_chart(
                    plot_manager.create_per_share_chart(financial_data),
                    use_container_width=True
                )
            with cols[1]:
                st.plotly_chart(
                    plot_manager.create_dividend_chart(financial_data),
                    use_container_width=True
                )

            # 稼ぐ力グラフ
            st.subheader("稼ぐ力グラフ")
            st.plotly_chart(
                plot_manager.create_earning_power_chart(financial_data),
                use_container_width=True
            )

            # 最新の財務指標
            st.subheader("最新の財務指標")
            latest_metrics = {
                "売上高": financial_data.revenue[-1],
                "営業利益": financial_data.operating_income[-1],
                "純利益": financial_data.net_income[-1],
                "EPS": financial_data.eps[-1],
                "BPS": financial_data.bps[-1],
            }

            cols = st.columns(len(latest_metrics))
            for col, (metric, value) in zip(cols, latest_metrics.items()):
                col.metric(metric, format_financial_value(value))

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()