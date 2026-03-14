import streamlit as st
from utils.auth import login, logout, init_auth
from components.chatbot import ai_chatbot_sidebar

# Initialize pages/views (to be created next)
import views.executive as executive
import views.productivity as productivity
import views.tech_insights as tech_insights
import views.time_allocation as time_allocation
import views.projects as projects
import views.ai_insights as ai_insights
import views.learning as learning
import views.alerts as alerts
import views.intern_personal as intern_personal
import views.mentor as mentor

from streamlit_option_menu import option_menu
from utils.style import apply_custom_css, render_navbar

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Intern Analytics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    init_auth()
    apply_custom_css()
    
    if not st.session_state.authenticated:
        # Load the new login UI from auth.py (we will update auth.py next)
        login()
        return

    # User is logged in
    role = st.session_state.role
    name = st.session_state.user_display_name
    
    # Top Navbar Injection
    render_navbar(name, role.replace('_', ' '))
    
    # Role-based pages mapping
    pages = {}
    options = []
    icons = []
    
    if role == 'HR_Manager':
        options = ["Executive Overview", "Intern Productivity", "Technology Insights", "AI Insights", "Manager Alerts"]
        icons = ["house", "people", "laptop", "robot", "exclamation-triangle"]
        pages = {
            "Executive Overview": executive.render,
            "Intern Productivity": productivity.render,
            "Technology Insights": tech_insights.render,
            "AI Insights": ai_insights.render,
            "Manager Alerts": alerts.render
        }
    elif role == 'Team_Manager':
        options = ["Team Productivity", "Time Allocation", "Project Contributions", "Manager Alerts"]
        icons = ["people", "clock", "folder", "exclamation-triangle"]
        pages = {
             "Team Productivity": productivity.render,
             "Time Allocation": time_allocation.render,
             "Project Contributions": projects.render,
             "Manager Alerts": alerts.render
        }
    elif role == 'Mentor':
        options = ["Mentorship Overview", "Learning Progress", "Intern Productivity"]
        icons = ["person-video3", "book", "graph-up"]
        pages = {
            "Mentorship Overview": mentor.render,
            "Learning Progress": learning.render,
            "Intern Productivity": productivity.render
        }
    elif role == 'Intern':
        options = ["My Dashboard", "My Learning"]
        icons = ["person-badge", "book"]
        pages = {
            "My Dashboard": intern_personal.render,
            "My Learning": learning.render
        }
        
    with st.sidebar:
        st.markdown("<div style='padding-top: 1rem; padding-bottom: 1rem; font-weight: 700; color: #64748B;'>PLATFORM MENU</div>", unsafe_allow_html=True)
        selection = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#64748B", "font-size": "1.1rem"}, 
                "nav-link": {"font-size": "0.95rem", "text-align": "left", "margin":"0px", "--hover-color": "#F1F5F9", "color": "#1E293B"},
                "nav-link-selected": {"background-color": "#EFF6FF", "color": "#2563EB", "font-weight": "600", "border-left": "4px solid #2563EB"},
            }
        )
        st.markdown("---")
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()
    
    # Add chatbot to sidebar for all users
    ai_chatbot_sidebar()
    
    # Render selected page
    pages[selection]()

if __name__ == "__main__":
    main()
