# pyre-ignore-all-errors
import streamlit as st
import pandas as pd
import plotly.express as px

import json, os
from database import get_ml_features, run_query
from components import metric_card, section_header
from predictor import get_ml_predictions
from config import BASE_DIR

# ================================================================
# HELPER — load model evaluation metrics
# ================================================================
def load_eval_metrics():
    eval_path = os.path.join(BASE_DIR, "models", "model_evaluation.json")
    if os.path.exists(eval_path):
        with open(eval_path) as f:
            return json.load(f)
    return {}

# ================================================================
# MANAGER ML INSIGHTS
# ================================================================
def manager_ml_insights():
    st.title("🤖 ML Insights — Manager View")
    st.caption("AI-powered predictions for all 40 interns.")

    df_features = get_ml_features()
    df_ml       = get_ml_predictions(df_features)

    # -------------------------------------------
    # MODEL PERFORMANCE CARDS
    # -------------------------------------------
    section_header("📐 Model Performance")
    metrics = load_eval_metrics()

    c1, c2, c3, c4 = st.columns(4)
    reg  = metrics.get('Productivity_Regression', {})
    clst = metrics.get('Intern_Segmentation_KMeans', {})
    clf  = metrics.get('At_Risk_Classification', {})

    metric_card("Regression R²",        reg.get('Accuracy_Percentage', 'N/A'),    c1)
    metric_card("Clustering Silhouette", str(clst.get('Silhouette_Score', 'N/A')), c2)
    metric_card("Classifier Accuracy",  clf.get('Accuracy_Percentage', 'N/A'),    c3)
    metric_card("Classifier ROC-AUC",   str(clf.get('ROC_AUC', 'N/A')),           c4)
    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------
    # CLUSTER DISTRIBUTION
    # -------------------------------------------
    section_header("👥 Intern Cluster Distribution")
    col1, col2 = st.columns(2)

    with col1:
        cat_counts = df_ml['category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig_pie = px.pie(
            cat_counts, names='Category', values='Count',
            color='Category',
            color_discrete_map={
                'High Performer'        : '#21c354',
                'Consistent Contributor': '#f0a500',
                'Learning Phase'        : '#ff4b4b'
            },
            hole=0.4, title='Intern Segments'
        )
        fig_pie.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = px.bar(
            cat_counts.sort_values('Count'),
            x='Count', y='Category', orientation='h',
            color='Category',
            color_discrete_map={
                'High Performer'        : '#21c354',
                'Consistent Contributor': '#f0a500',
                'Learning Phase'        : '#ff4b4b'
            },
            text_auto=True, title='Count per Cluster'
        )
        fig_bar.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)',
                              paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------------------------
    # PRODUCTIVITY SCATTER (Hours vs Score, colored by cluster)
    # -------------------------------------------
    section_header("📊 Productivity Clusters — Hours vs Score")
    fig_scatter = px.scatter(
        df_ml, x='hours_spent', y='avg_score',
        color='category', size='productivity_score',
        hover_name='intern_id',
        hover_data={'predicted_productivity': ':.1f',
                    'at_risk_label': True,
                    'hours_spent': ':.0f',
                    'avg_score': ':.1f'},
        color_discrete_map={
            'High Performer'        : '#21c354',
            'Consistent Contributor': '#f0a500',
            'Learning Phase'        : '#ff4b4b'
        },
        title='Intern Clusters — EOD Hours vs Avg Score',
        labels={'hours_spent': 'Total EOD Hours', 'avg_score': 'Avg Score %'}
    )
    fig_scatter.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)',
                              paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)

    # -------------------------------------------
    # AT-RISK PREDICTION TABLE
    # -------------------------------------------
    section_header("🚨 At-Risk Prediction (ML Classification)")
    at_risk_ml = df_ml[df_ml['at_risk'] == 1].sort_values(
        'at_risk_probability', ascending=False
    )[['intern_id','category','productivity_score',
       'avg_score','at_risk_label','at_risk_probability']].round(2)

    safe_count = int((df_ml['at_risk'] == 0).sum())
    risk_count = int((df_ml['at_risk'] == 1).sum())
    c1, c2 = st.columns(2)
    metric_card("✅ Safe Interns",   safe_count, c1)
    metric_card("⚠️ At-Risk Interns", risk_count, c2)
    st.markdown("<br>", unsafe_allow_html=True)

    if at_risk_ml.empty:
        st.success("✅ No interns predicted as at-risk.")
    else:
        st.warning(f"⚠️ {risk_count} interns predicted as at-risk by ML model.")
        st.dataframe(
            at_risk_ml, use_container_width=True,
            column_config={
                'intern_id'           : 'Intern',
                'category'            : 'Cluster',
                'productivity_score'  : st.column_config.NumberColumn('Productivity Score', format='%.1f'),
                'avg_score'           : st.column_config.NumberColumn('Avg Score %', format='%.1f%%'),
                'at_risk_label'       : 'ML Prediction',
                'at_risk_probability' : st.column_config.NumberColumn('Risk Probability %', format='%.1f%%'),
            }
        )

    # -------------------------------------------
    # TOP 10 LEADERBOARD
    # -------------------------------------------
    section_header("🏆 Productivity Leaderboard (ML Predicted)")
    top10 = df_ml.nlargest(10, 'predicted_productivity')[
        ['intern_id','predicted_productivity','productivity_score','category']
    ].round(2)

    fig_lb = px.bar(
        top10.sort_values('predicted_productivity'),
        x='predicted_productivity', y='intern_id',
        orientation='h', color='category',
        color_discrete_map={
            'High Performer'        : '#21c354',
            'Consistent Contributor': '#f0a500',
            'Learning Phase'        : '#ff4b4b'
        },
        text_auto='.1f',
        title='Top 10 Interns by Predicted Productivity',
        labels={'predicted_productivity': 'Predicted Productivity', 'intern_id': ''}
    )
    fig_lb.update_layout(height=380, plot_bgcolor='rgba(0,0,0,0)',
                         paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_lb, use_container_width=True)

    # -------------------------------------------
    # FEATURE IMPORTANCE
    # -------------------------------------------
    if clf.get('Feature_Importance'):
        section_header("🔍 Feature Importance (At-Risk Classifier)")
        fi = pd.DataFrame(
            clf['Feature_Importance'].items(),
            columns=['Feature', 'Importance']
        ).sort_values('Importance', ascending=True)

        fig_fi = px.bar(fi, x='Importance', y='Feature', orientation='h',
                        color_discrete_sequence=['#7c83fd'], text_auto='.3f',
                        title='Which features matter most for at-risk prediction?')
        fig_fi.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)',
                             paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_fi, use_container_width=True)

    # -------------------------------------------
    # FULL INTERN ML TABLE
    # -------------------------------------------
    section_header("📋 All Interns — Full ML Summary")
    display_cols = ['intern_id','productivity_score','predicted_productivity',
                    'category','at_risk_label','at_risk_probability','hours_spent','avg_score']
    st.dataframe(
        df_ml[display_cols].sort_values('predicted_productivity', ascending=False).round(2),
        use_container_width=True,
        column_config={
            'intern_id'              : 'Intern',
            'productivity_score'     : st.column_config.NumberColumn('Actual Productivity',   format='%.1f'),
            'predicted_productivity' : st.column_config.NumberColumn('Predicted Productivity',format='%.1f'),
            'category'               : 'Cluster',
            'at_risk_label'          : 'Risk Status',
            'at_risk_probability'    : st.column_config.NumberColumn('Risk %', format='%.1f%%'),
            'hours_spent'            : st.column_config.NumberColumn('EOD Hours', format='%.0f'),
            'avg_score'              : st.column_config.NumberColumn('Avg Score %', format='%.1f%%'),
        }
    )

# ================================================================
# EMPLOYEE ML INSIGHTS
# ================================================================
def employee_ml_insights(mentor_id):
    st.title("🤖 ML Insights — Mentor View")

    if mentor_id is None:
        st.error("No mentor linked to this account.")
        return

    mentor_info = run_query(
        "SELECT mentor_name FROM dim_mentor WHERE mentor_id = %s",
        params=(mentor_id,)
    )
    if mentor_info.empty:
        st.error("Mentor not found.")
        return

    mentor_name = str(mentor_info.iloc[0]['mentor_name'])
    st.caption(f"ML predictions for **{mentor_name}'s** interns.")

    df_features = get_ml_features()
    df_ml       = get_ml_predictions(df_features)

    # Filter to mentor's interns
    from database import get_all_progress
    df_lms = get_all_progress()
    my_interns = df_lms[df_lms['mentor_name'] == mentor_name]['intern_name'].unique()
    df_ml = df_ml[df_ml['intern_id'].isin(my_interns)].copy()

    if df_ml.empty:
        st.info("No ML data available for your interns.")
        return

    # -------------------------------------------
    # KPI CARDS
    # -------------------------------------------
    section_header("📌 Your Interns — ML Overview")
    c1, c2, c3, c4 = st.columns(4)
    metric_card("Total Interns",    int(len(df_ml)),                                          c1)
    metric_card("High Performers",  int((df_ml['category'] == 'High Performer').sum()),       c2)
    metric_card("At-Risk (ML)",     int(df_ml['at_risk'].sum()),                              c3)
    metric_card("Avg Productivity", f"{df_ml['predicted_productivity'].mean():.1f}",          c4)
    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------
    # CLUSTER BREAKDOWN
    # -------------------------------------------
    section_header("👥 Your Interns by Cluster")
    cat_counts = df_ml['category'].value_counts().reset_index()
    cat_counts.columns = ['Category', 'Count']
    fig_pie = px.pie(
        cat_counts, names='Category', values='Count',
        color='Category',
        color_discrete_map={
            'High Performer'        : '#21c354',
            'Consistent Contributor': '#f0a500',
            'Learning Phase'        : '#ff4b4b'
        },
        hole=0.4
    )
    fig_pie.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

    # -------------------------------------------
    # AT-RISK PREDICTION
    # -------------------------------------------
    section_header("🚨 At-Risk Prediction (Your Interns)")
    my_risk = df_ml[df_ml['at_risk'] == 1].sort_values(
        'at_risk_probability', ascending=False
    )[['intern_id','category','productivity_score','avg_score',
       'at_risk_label','at_risk_probability']].round(2)

    if my_risk.empty:
        st.success("✅ None of your interns are predicted as at-risk.")
    else:
        st.warning(f"⚠️ {len(my_risk)} of your interns are predicted at-risk.")
        st.dataframe(my_risk, use_container_width=True,
            column_config={
                'intern_id'          : 'Intern',
                'category'           : 'Cluster',
                'productivity_score' : st.column_config.NumberColumn('Productivity', format='%.1f'),
                'avg_score'          : st.column_config.NumberColumn('Avg Score %', format='%.1f%%'),
                'at_risk_label'      : 'ML Prediction',
                'at_risk_probability': st.column_config.NumberColumn('Risk %', format='%.1f%%'),
            }
        )

    # -------------------------------------------
    # FULL TABLE
    # -------------------------------------------
    section_header("📋 All Your Interns — ML Summary")
    display_cols = ['intern_id','predicted_productivity','category',
                    'at_risk_label','at_risk_probability','hours_spent','avg_score']
    st.dataframe(
        df_ml[display_cols].sort_values('predicted_productivity', ascending=False).round(2),
        use_container_width=True,
        column_config={
            'intern_id'              : 'Intern',
            'predicted_productivity' : st.column_config.NumberColumn('Predicted Productivity', format='%.1f'),
            'category'               : 'Cluster',
            'at_risk_label'          : 'Risk Status',
            'at_risk_probability'    : st.column_config.NumberColumn('Risk %', format='%.1f%%'),
            'hours_spent'            : st.column_config.NumberColumn('EOD Hours', format='%.0f'),
            'avg_score'              : st.column_config.NumberColumn('Avg Score %', format='%.1f%%'),
        }
    )

# ================================================================
# MAIN ROUTER
# ================================================================
def ml_insights_page(user):
    if user['role'] == 'manager':
        manager_ml_insights()
    elif user['role'] == 'employee':
        employee_ml_insights(user['mentor_id'])
    else:
        st.error("ML Insights not available for intern role.")
