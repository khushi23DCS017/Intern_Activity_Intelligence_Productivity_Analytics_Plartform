# pyre-ignore-all-errors
"""
Components package — backward-compatible re-exports from _legacy.py
plus new component modules (chatbot, charts, kpi_cards).
"""
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.style import apply_custom_css

# ================================================================
# GLOBAL CSS — delegates to the new premium theme
# ================================================================
def inject_css():
    apply_custom_css()

# ================================================================
# METRIC CARD (legacy — used by pages/ml_insights.py, pages/manager.py, etc.)
# ================================================================
def metric_card(label, value, col):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# SECTION HEADER
# ================================================================
def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>',
                unsafe_allow_html=True)

# ================================================================
# SAFE FLOAT FORMAT
# ================================================================
def safe_float_fmt(val, fmt=".1f"):
    """NaN/None → 'N/A', else formatted string."""
    if val is None:
        return "N/A"
    try:
        import pandas as pd
        if pd.isna(val):
            return "N/A"
    except (TypeError, ValueError):
        pass
    return f"{float(val):{fmt}}%"

# ================================================================
# CATEGORY BADGE
# ================================================================
def category_badge(category):
    badges = {
        'High Performer'        : 'ml-badge-high',
        'Consistent Contributor': 'ml-badge-mid',
        'Learning Phase'        : 'ml-badge-low'
    }
    css_class = badges.get(category, 'ml-badge-mid')
    return f'<span class="{css_class}">{category}</span>'

# ================================================================
# SIDEBAR (updated for new session state structure)
# ================================================================
def show_sidebar(user):
    with st.sidebar:
        st.markdown(f"### 👤 {user['full_name']}")
        st.markdown(f"**Role:** `{user['role'].capitalize()}`")
        st.markdown("---")

        # Navigation
        st.markdown("**Navigation**")
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

        # ML Insights available for manager and employee only
        if user['role'] in ('manager', 'employee'):
            if st.button("🤖 ML Insights", use_container_width=True):
                st.session_state['page'] = 'ml_insights'
                st.rerun()

        st.markdown("---")
        st.caption("Intern Analytics Platform")
        st.markdown("---")
        if st.button("🚪 Sign Out", use_container_width=True):
            del st.session_state['user']
            st.session_state['page'] = 'dashboard'
            st.rerun()
