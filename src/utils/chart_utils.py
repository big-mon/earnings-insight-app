"""チャートユーティリティ"""
import plotly.graph_objects as go
from typing import Dict, Optional
import pandas as pd


def create_financial_chart(dates, primary_data: Dict, secondary_data: Optional[Dict] = None,
                         title: str = "", y1_title: str = "金額", y2_title: Optional[str] = None):
    """財務データのチャートを作成"""
    fig = go.Figure()

    # 日付のフォーマットを変更
    formatted_dates = [pd.to_datetime(date).strftime("%Y/%m") for date in dates]

    # 第1軸のデータを追加（棒グラフ）
    for name, values in primary_data.items():
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
    if secondary_data:
        for name, values in secondary_data.items():
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
        "title": title,
        "xaxis": {"title": "日付"},
        "yaxis": {"title": y1_title},
        "showlegend": True,
        "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        "barmode": "group"  # 棒グラフをグループ化
    }

    # 第2軸が存在する場合、レイアウトに追加
    if secondary_data:
        layout.update({
            "yaxis2": {
                "title": y2_title,
                "overlaying": "y",
                "side": "right"
            }
        })

    fig.update_layout(**layout)
    return fig
