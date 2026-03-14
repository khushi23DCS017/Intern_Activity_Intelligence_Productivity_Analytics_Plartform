# pyre-ignore-all-errors
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ================================================================
# GLOBAL CSS
# ================================================================
def inject_css():
    st.markdown("""
    <style>
        .metric-card {
            background: #1e1e2e;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #2d2d44;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #7c83fd;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #aaa;
            margin-top: 4px;
        }
        .section-header {
            font-size: 1.1rem;
            font-weight: 600;
            color: #7c83fd;
            border-bottom: 2px solid #7c83fd33;
            padding-bottom: 6px;
            margin-bottom: 16px;
        }
        .ml-badge-high {
            background: #21c35422;
            border: 1px solid #21c354;
            border-radius: 20px;
            padding: 4px 14px;
            color: #21c354;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .ml-badge-mid {
            background: #f0a50022;
            border: 1px solid #f0a500;
            border-radius: 20px;
            padding: 4px 14px;
            color: #f0a500;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .ml-badge-low {
            background: #ff4b4b22;
            border: 1px solid #ff4b4b;
            border-radius: 20px;
            padding: 4px 14px;
            color: #ff4b4b;
            font-weight: 600;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)

# ================================================================
# METRIC CARD
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
# SIDEBAR
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
