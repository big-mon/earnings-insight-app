"""財務データ可視化アプリケーション"""
import streamlit as st
from utils.financial_utils import get_normalized_financial_data, format_financial_value
from utils.chart_utils import create_financial_chart


def main():
    """メインアプリケーション"""
    st.set_page_config(
        page_title="Earnings Insight App",
        page_icon="📈",
        layout="wide"
    )

    st.title("Earnings Insight App")
    st.write("米国株式の財務情報分析アプリケーション")

    # サイドバーの設定
    with st.sidebar:
        st.header("設定")
        ticker = st.text_input("ティッカーシンボルを入力してください（例：AAPL）", "AAPL")
        period = st.selectbox(
            "期間",
            ["quarterly", "annual"],
            format_func=lambda x: "四半期" if x == "quarterly" else "年次"
        )

    if ticker:
        # ローディング表示
        with st.spinner(f"'{ticker}'の財務データを取得中..."):
            data = get_normalized_financial_data(ticker, period)

        if data is None:
            st.error("財務データの取得に失敗しました。ティッカーシンボルを確認してください。")
            return

        # 業績確認グラフ
        st.plotly_chart(
            create_financial_chart(
                dates=data["dates"],
                primary_data={
                    "売上高": data["revenue"],
                    "営業利益": data["operating_income"],
                    "純利益": data["net_income"]
                },
                secondary_data={
                    "営業利益率": data["operating_margin"]
                },
                title="業績確認",
                y1_title="金額",
                y2_title="営業利益率 (%)"
            ),
            use_container_width=True
        )

        # 1株当たりの価値グラフ
        st.plotly_chart(
            create_financial_chart(
                dates=data["dates"],
                primary_data={
                    "EPS": data["eps"],
                    "BPS": data["bps"],
                    "DPS": data["dps"] if "dps" in data else None
                    },
                    secondary_data={
                        "発行済株式数": data["shares"]
                    },
                title="1株当たりの価値",
                y1_title="金額",
                y2_title="発行済株式数"
            ),
            use_container_width=True
        )

        # 稼ぐ力グラフ
        st.plotly_chart(
            create_financial_chart(
                dates=data["dates"],
                primary_data={
                    "営業利益": data["operating_income"],
                    "営業CF": data["operating_cash_flow"]
                },
                secondary_data={
                    "EPS": data["eps"],
                    "1株あたり営業CF": data["operating_cash_flow_per_share"]
                },
                title="稼ぐ力",
                y1_title="金額",
                y2_title="1株当たり金額"
            ),
            use_container_width=True
        )

        # 最新の財務指標
        st.subheader("最新の財務指標")
        latest_metrics = {
            "売上高": data["revenue"][-1],
            "営業利益": data["operating_income"][-1],
            "純利益": data["net_income"][-1],
            "EPS": data["eps"][-1],
            "BPS": data["bps"][-1],
        }

        cols = st.columns(len(latest_metrics))
        for col, (metric, value) in zip(cols, latest_metrics.items()):
            col.metric(metric, format_financial_value(value))


if __name__ == "__main__":
    main()