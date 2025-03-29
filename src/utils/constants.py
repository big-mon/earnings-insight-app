"""定数定義"""

# 期間設定
PERIOD_QUARTERLY = "quarterly"
PERIOD_ANNUAL = "annual"

# 財務データキー
KEY_REVENUE = "売上高"
KEY_OPERATING_INCOME = "営業利益"
KEY_NET_INCOME = "純利益"
KEY_OPERATING_CASH_FLOW = "営業キャッシュフロー"
KEY_SHARES = "発行済株式数"
KEY_EPS = "EPS"
KEY_BPS = "BPS"
KEY_OPERATING_MARGIN = "営業利益率"
KEY_OPERATING_CASH_FLOW_PER_SHARE = "1株あたり営業CF"
KEY_DPS = "DPS"

# 財務諸表キー（yfinance）
YF_REVENUE = "Total Revenue"
YF_OPERATING_INCOME = "Operating Income"
YF_NET_INCOME = "Net Income"
YF_OPERATING_CASH_FLOW = "Operating Cash Flow"
YF_STOCKHOLDER_EQUITY = "Total Stockholder Equity"
YF_TOTAL_ASSETS = "Total Assets"
YF_TOTAL_LIABILITIES = "Total Liabilities Net Minority Interest"

# エラーメッセージ
ERROR_DATA_FETCH = "財務データの取得に失敗しました。ティッカーシンボルを確認してください。"
ERROR_MISSING_DATA = "必要なデータが不足しています。"
ERROR_PROCESSING = "データ処理中にエラーが発生しました。"

# 表示設定
DATE_FORMAT = "%Y/%m"
APP_TITLE = "Earnings Insight App"
APP_DESCRIPTION = "米国株式の財務情報分析アプリケーション"
APP_ICON = "📈"
