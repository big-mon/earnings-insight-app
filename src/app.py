import streamlit as st

def main():
    st.set_page_config(
        page_title="Earnings Insight App",
        page_icon="📈",
        layout="wide"
    )
    
    st.title("Earnings Insight App")
    st.write("米国株式の財務情報分析アプリケーション")
    
    # ティッカーシンボル入力
    ticker = st.text_input("ティッカーシンボルを入力してください（例：AAPL）", "")
    
    if ticker:
        st.info(f"'{ticker}'の財務データを取得中...")
        # TODO: 財務データの取得と表示機能を実装
    else:
        st.info("分析したい企業のティッカーシンボルを入力してください。")

if __name__ == "__main__":
    main()