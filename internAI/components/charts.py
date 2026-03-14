# pyre-ignore-all-errors
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def kpi_card(title, value, delta=None):
    st.metric(label=title, value=value, delta=delta)

def plot_line_chart(df, x_col, y_col, title, color_col=None):
    if df.empty:
        st.warning("No data available for chart.")
        return None
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def plot_bar_chart(df, x_col, y_col, title, color_col=None, orientation='v', barmode='relative'):
    if df.empty:
        st.warning("No data available for chart.")
        return None
    fig = px.bar(df, x=x_col, y=y_col, color=color_col, orientation=orientation, title=title, barmode=barmode)
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def plot_pie_chart(df, names_col, values_col, title, hole=0):
    if df.empty:
        st.warning("No data available for chart.")
        return None
    fig = px.pie(df, names=names_col, values=values_col, title=title, hole=hole)
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def plot_scatter_clusters(df, x_col, y_col, color_col, title):
     if df.empty:
        return None
     fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=title, hover_data=df.columns)
     fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
     return fig
     
def plot_radar_chart(df, categories_col, values_col, title):
    if df.empty:
        return None
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df[values_col],
        theta=df[categories_col],
        fill='toself',
        name='Skills'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title=title,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig
