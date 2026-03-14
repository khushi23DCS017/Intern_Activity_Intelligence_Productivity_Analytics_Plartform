import streamlit as st

def kpi_card(title, value, icon, trend_value=None, trend_type="neutral"):
    """
    Renders a custom HTML/CSS KPI card.
    trend_type can be: 'up', 'down', 'netural'
    """
    
    if trend_type == 'up':
        trend_class = "trend-up"
        trend_icon = "↑"
    elif trend_type == 'down':
        trend_class = "trend-down"
        trend_icon = "↓"
    else:
         trend_class = "trend-neutral"
         trend_icon = "→"
         
    trend_html = ""
    if trend_value:
        trend_html = f"""
        <div class="kpi-trend {trend_class}">
            <span>{trend_icon}</span>
            <span>{trend_value}</span>
        </div>
        """

    html = f"""
    <div class="kpi-wrapper">
        <div class="kpi-header">
            <span>{title}</span>
            <span class="kpi-icon">{icon}</span>
        </div>
        <div class="kpi-value">{value}</div>
        {trend_html}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def alert_card(title, message, severity="warning"):
    """
    Renders a custom styled alert.
    severity: 'critical', 'warning', 'normal'
    """
    icons = {'critical': '🚨', 'warning': '⚠️', 'normal': '✅'}
    icon = icons.get(severity, 'ℹ️')
    
    html = f"""
    <div class="alert-card alert-{severity}">
        <h4 style="margin: 0; display: flex; align-items: center; gap: 8px;">
            <span>{icon}</span> {title}
        </h4>
        <p style="margin: 8px 0 0 0; color: var(--text-muted); font-size: 0.9rem;">{message}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
