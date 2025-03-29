"""財務データ可視化アプリケーション"""
import streamlit as st
import plotly.graph_objects as go
from utils.financial_utils import get_normalized_financial_data, format_financial_value

def create_financial_chart(dates, values, title):
    """財務データのチャートを作成"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers'))
    fig.update_layout(
        title=title,
        xaxis_title="日付",
        yaxis_title="金額",
        showlegend=False
    )
    return fig

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

        # 2カラムレイアウト
        col1, col2 = st.columns(2)

        with col1:
            # 売上高のチャート
            st.plotly_chart(
                create_financial_chart(data["dates"], data["revenue"], "売上高"),
                use_container_width=True
            )
            
            # 純利益のチャート
            st.plotly_chart(
                create_financial_chart(data["dates"], data["net_income"], "純利益"),
                use_container_width=True
            )
            
            # EPSのチャート
            st.plotly_chart(
                create_financial_chart(data["dates"], data["eps"], "EPS（一株当たり利益）"),
                use_container_width=True
            )
            
            # DPSのチャート
            if "dps" in data:
                st.plotly_chart(
                    create_financial_chart(data["dates"], data["dps"], "DPS（一株当たり配当金）"),
                    use_container_width=True
                )

        with col2:
            # 営業利益のチャート
            st.plotly_chart(
                create_financial_chart(data["dates"], data["operating_income"], "営業利益"),
                use_container_width=True
            )
            
            # 営業キャッシュフローのチャート
            st.plotly_chart(
                create_financial_chart(data["dates"], data["operating_cash_flow"], "営業キャッシュフロー"),
                use_container_width=True
            )
            
            # BPSのチャート
            st.plotly_chart(
                create_financial_chart(data["dates"], data["bps"], "BPS（一株当たり純資産）"),
                use_container_width=True
            )
            
            # 発行済株式数のチャート
            st.plotly_chart(
                create_financial_chart(data["dates"], data["shares"], "発行済株式数（希薄化後）"),
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