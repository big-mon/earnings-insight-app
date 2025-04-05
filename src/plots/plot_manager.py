"""チャート管理モジュール"""
from typing import Dict, List, Optional
import plotly.graph_objects as go
from utils.models import ChartConfig, FinancialDataModel
from utils.formatting import format_dates


class PlotManager:
    """チャート管理クラス"""

    @staticmethod
    def create_financial_chart(
        dates: List,
        config: ChartConfig
    ) -> go.Figure:
        """
        財務データのチャートを作成
        Args:
            dates (List): 日付リスト
            config (ChartConfig): チャート設定
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        fig = go.Figure()

        # 日付のフォーマットを変更
        formatted_dates = format_dates(dates)

        # 第1軸のデータを追加（棒グラフ）
        for name, values in config.primary_data.items():
            if values is not None:  # Noneチェックを追加
                fig.add_trace(
                    go.Bar(
                        x=formatted_dates,
                        y=values,
                        name=name,
                        yaxis="y"
                    )
                )

        # 第2軸のデータを追加（存在する場合）
        if config.secondary_data:
            for name, values in config.secondary_data.items():
                if values is not None:  # Noneチェックを追加
                    if "発行済株式数" in name:
                        fig.add_trace(
                            go.Scatter(
                                x=formatted_dates,
                                y=values,
                                name=name,
                                mode="lines+markers",  # マーカーを追加して時間軸毎の変化を明確に
                                yaxis="y2"
                            )
                        )
                        # 発行済株式数の軸範囲を0から設定
                        fig.update_layout(
                            yaxis2={
                                "rangemode": "tozero"
                            }
                        )
                    elif "配当性向" in name:
                        fig.add_trace(
                            go.Scatter(
                                x=formatted_dates,
                                y=values,
                                name=name,
                                mode="lines+markers",  # マーカーを追加して時間軸毎の変化を明確に
                                yaxis="y2"
                            )
                        )
                    else:
                        fig.add_trace(
                            go.Scatter(
                                x=formatted_dates,
                                y=values,
                                name=name,
                                mode="lines",
                                yaxis="y2"
                            )
                        )

        # レイアウトの設定
        layout = {
            "title": config.title,
            "xaxis": {"title": "日付"},
            "yaxis": {"title": config.y1_title},
            "showlegend": True,
            "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
            "barmode": "group"  # 棒グラフをグループ化
        }

        # 第2軸が存在する場合、レイアウトに追加
        if config.secondary_data:
            layout.update({
                "yaxis2": {
                    "title": config.y2_title,
                    "overlaying": "y",
                    "side": "right"
                }
            })

        fig.update_layout(**layout)
        return fig

    @staticmethod
    def create_performance_chart(data: FinancialDataModel) -> go.Figure:
        """
        業績確認チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        config = ChartConfig(
            title="業績確認",
            y1_title="金額",
            primary_data={
                "売上高": data.revenue,
                "営業利益": data.operating_income,
                "純利益": data.net_income
            },
            y2_title="マージン (%)",
            secondary_data={
                "営業利益率": data.operating_margin
            }
        )

        return PlotManager.create_financial_chart(data.dates, config)

    @staticmethod
    def create_per_share_chart(data: FinancialDataModel) -> go.Figure:
        """
        1株当たりの価値チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        config = ChartConfig(
            title="1株当たりの価値",
            y1_title="金額",
            primary_data={
                "EPS": data.eps,
                "BPS": data.bps,
                "DPS": data.dps
            },
            y2_title="発行済株式数",
            secondary_data={
                "発行済株式数": data.shares
            }
        )

        return PlotManager.create_financial_chart(data.dates, config)

    @staticmethod
    def create_dividend_chart(data: FinancialDataModel) -> go.Figure:
        """
        配当チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        # 配当性向の計算（DPS / EPS * 100）
        payout_ratio = []
        if data.dps is not None and data.eps is not None:
            for dps, eps in zip(data.dps, data.eps):
                if eps != 0:
                    payout_ratio.append((dps / eps) * 100)
                else:
                    payout_ratio.append(0)

        config = ChartConfig(
            title="配当",
            y1_title="金額",
            primary_data={
                "DPS": data.dps
            },
            y2_title="配当性向 (%)",
            secondary_data={
                "配当性向": payout_ratio
            }
        )
        return PlotManager.create_financial_chart(data.dates, config)

    @staticmethod
    def create_earning_power_chart(data: FinancialDataModel) -> go.Figure:
        """
        稼ぐ力チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        config = ChartConfig(
            title="稼ぐ力",
            y1_title="金額",
            primary_data={
                "営業利益": data.operating_income,
                "営業CF": data.operating_cash_flow
            },
            y2_title="1株当たり金額",
            secondary_data={
                "EPS": data.eps,
                "1株あたり営業CF": data.operating_cash_flow_per_share
            }
        )

        return PlotManager.create_financial_chart(data.dates, config)

    @staticmethod
    def create_earning_power_profit_chart(data: FinancialDataModel) -> go.Figure:
        """
        稼ぐ力（利益）チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        config = ChartConfig(
            title="営業利益とCF",
            y1_title="金額",
            primary_data={
                "営業利益": data.operating_income,
                "営業CF": data.operating_cash_flow
            }
        )
        return PlotManager.create_financial_chart(data.dates, config)

    @staticmethod
    def create_earning_power_per_share_chart(data: FinancialDataModel) -> go.Figure:
        """
        稼ぐ力（1株当たり）チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        fig = go.Figure()
        formatted_dates = format_dates(data.dates)

        fig.add_trace(go.Bar(
            x=formatted_dates,
            y=data.eps,
            name="EPS"
        ))

        fig.add_trace(go.Scatter(
            x=formatted_dates,
            y=data.operating_cash_flow_per_share,
            name="営業CF/株",
            mode="lines+markers"
        ))

        fig.update_layout(
            title="1株当たり指標",
            showlegend=True,
            yaxis_title="$/株",
            xaxis_title="日付",
            legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
        )

        return fig

    @staticmethod
    def create_earning_power_margin_chart(data: FinancialDataModel) -> go.Figure:
        """
        稼ぐ力（マージン）チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        # FCFマージンの計算
        fcf_margin = None
        if data.operating_cash_flow is not None and data.revenue is not None:
            fcf_margin = data.operating_cash_flow / data.revenue * 100

        fig = go.Figure()

        # 日付のフォーマットを変更
        formatted_dates = format_dates(data.dates)

        # マージン指標を追加
        fig.add_trace(
            go.Scatter(
                x=formatted_dates,
                y=data.operating_margin,
                name="営業利益率",
                mode="lines"
            )
        )

        # 営業CFマージンを計算して追加
        if data.operating_cash_flow is not None and data.revenue is not None:
            cf_margin = data.operating_cash_flow / data.revenue * 100
            fig.add_trace(
                go.Scatter(
                    x=formatted_dates,
                    y=cf_margin,
                    name="営業CFマージン",
                    mode="lines"
                )
            )

        # FCFマージンを追加
        if fcf_margin is not None:
            fig.add_trace(
                go.Scatter(
                    x=formatted_dates,
                    y=fcf_margin,
                    name="FCFマージン",
                    mode="lines"
                )
            )

        # 15%の参考線を追加
        fig.add_hline(y=15, line_dash="dash", line_color="gray", annotation_text="15%")

        # レイアウトの設定
        fig.update_layout(
            title="収益性指標",
            xaxis={"title": "日付"},
            yaxis={"title": "マージン (%)"},
            showlegend=True,
            legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
        )

        return fig