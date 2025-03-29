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
    st.set_page_config(
        page_title="Earnings Insight App",
        page_icon="📈",
        layout="wide"
    )

    st.title("Earnings Insight App")
    st.write("米国株式の財務情報分析アプリケーション")

    # サイドバー設定
    with st.sidebar:
        st.header("設定")
        ticker = st.text_input("ティッカーシンボルを入力してください（例：AAPL）", "AAPL")
        period = st.selectbox(
            "期間",
            ["quarterly", "annual"],
            format_func=lambda x: "四半期" if x == "quarterly" else "年次"
        )

    if ticker:
        st.info(f"'{ticker}'の財務データを取得中...")
        
        # 財務データの取得
        data = get_normalized_financial_data(ticker, period)
        
        if data:
            # データの表示
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

            # DPSの表示（データがある場合のみ）
            if data["dps"]:
                st.subheader("配当情報")
                st.plotly_chart(
                    create_financial_chart(data["dates"], data["dps"], "DPS（一株当たり配当金）"),
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

        else:
            st.error("財務データの取得に失敗しました。ティッカーシンボルを確認してください。")
    else:
        st.info("分析したい企業のティッカーシンボルを入力してください。")

if __name__ == "__main__":
    main()