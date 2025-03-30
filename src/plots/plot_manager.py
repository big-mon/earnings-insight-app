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
                                mode="lines",
                                fill="tozeroy",
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
            y2_title="営業利益率 (%)",
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
        primary_data = {
            "EPS": data.eps,
            "BPS": data.bps
        }
        
        # 配当データがある場合は追加
        if data.dps is not None:
            primary_data["DPS"] = data.dps
            
        config = ChartConfig(
            title="1株当たりの価値",
            y1_title="金額",
            primary_data=primary_data,
            y2_title="株式数",
            secondary_data={
                "発行済株式数": data.shares
            }
        )
        
        return PlotManager.create_financial_chart(data.dates, config)

    @staticmethod
    def create_shares_chart(data: FinancialDataModel) -> go.Figure:
        """
        発行済株式数チャートを作成
        Args:
            data (FinancialDataModel): 財務データモデル
        Returns:
            go.Figure: Plotlyのグラフオブジェクト
        """
        primary_data = {
            "発行済株式数": data.shares
        }
        
        # 配当データがある場合は追加
        if data.dps is not None:
            # 配当性向を計算（DPS / EPS * 100）
            payout_ratio = [
                (d / e * 100) if e != 0 else 0
                for d, e in zip(data.dps, data.eps)
            ]
            
            config = ChartConfig(
                title="配当と配当性向",
                y1_title="金額",
                primary_data={"DPS": data.dps},
                y2_title="配当性向 (%)",
                secondary_data={"配当性向": payout_ratio}
            )
        else:
            config = ChartConfig(
                title="発行済株式数",
                y1_title="株式数",
                primary_data=primary_data
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