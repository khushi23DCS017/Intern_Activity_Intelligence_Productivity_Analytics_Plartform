import streamlit as st
import base64
from pathlib import Path

def init_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        
# Mock user database
USERS = {
    'hr1': {'password': 'password', 'role': 'HR_Manager', 'name': 'Alice HR'},
    'mgr1': {'password': 'password', 'role': 'Team_Manager', 'name': 'Bob Manager'},
    'mentor1': {'password': 'password', 'role': 'Mentor', 'name': 'Charlie Mentor'},
    'intern1': {'password': 'password', 'role': 'Intern', 'name': 'Intern_1'},  # Must match an ID from mock data
    'intern2': {'password': 'password', 'role': 'Intern', 'name': 'Intern_2'},
}

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def login():
    # Load background image
    try:
        img_base64 = get_base64_of_bin_file('C:/Intern_AI/assets/login_bg.png')
        bg_image_css = f"background-image: url('data:image/png;base64,{img_base64}');"
    except:
        # Fallback gradient if image is missing
        bg_image_css = "background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);"

    st.markdown(f"""
        <style>
        /* Hide navbar during login if you have one */
        .top-navbar {{ display: none; }}
        
        /* The main outer container that breaks out of streamlit defaults */
        .login-super-container {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: #E2E8F0;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999999;
        }}
        
        /* The Card */
        .login-card {{
            display: flex;
            width: 1000px;
            height: 600px;
            background-color: white;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            border-radius: 8px;
            overflow: hidden;
            animation: fadeIn 0.5s ease forwards;
        }}
        
        /* Left Side: Form */
        .login-left {{
            flex: 1;
            padding: 40px 50px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}
        
        /* Right Side: Image/Illustration */
        .login-right {{
            flex: 1.2;
            {bg_image_css}
            background-size: cover;
            background-position: center;
        }}
        
        /* Typography */
        .brand-logo {{
            font-size: 1.5rem;
            font-weight: 800;
            color: #2563EB;
            margin-bottom: 60px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .welcome-text {{
            font-size: 1.8rem;
            color: #1E293B;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        .subtitle-text {{
            font-size: 1.2rem;
            color: #64748B;
            font-weight: 600;
            margin-bottom: 40px;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Hide standard streamlit blocks */
        .stApp [data-testid="stHeader"] {{ display: none; }}
        .block-container {{ padding: 0 !important; max-width: 100% !important; }}
        </style>
    """, unsafe_allow_html=True)

    # We build the split UI using standard Streamlit columns, BUT we wrap the interactive 
    # form in a container and float it on top of the native UI hack to ensure buttons work.
    
    col1, col2, col3 = st.columns([1, 4, 1]) # Center block
    
    with col2:
        st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
        # Use a container that looks like the card
        container = st.container()
        with container:
            # We recreate the layout using an embedded form
            scol_form, scol_image = st.columns([1, 1.2], gap="large")
            
            with scol_form:
                st.markdown("""
                <div class='brand-logo'>
                    <div style='background: #2563EB; color: white; border-radius: 4px; padding: 2px 6px; font-size: 1.2rem;'>K</div> 
                    Kenexai
                </div>
                <div class='welcome-text'>Welcome to Kenexai</div>
                <div class='subtitle-text'>Sign into your account</div>
                """, unsafe_allow_html=True)
                
                with st.form("login_form", border=False):
                    username = st.text_input("Username", placeholder="Username or email address")
                    password = st.text_input("Password", type="password", placeholder="Password")
                    
                    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
                    # For demo purposes
                    selected_role = st.selectbox("Mock Role", ['HR_Manager', 'Team_Manager', 'Mentor', 'Intern'])
                    
                    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                    submit = st.form_submit_button("Log In", use_container_width=True)
                    
                    st.markdown("<p style='font-size: 0.8rem; color: #3B82F6; margin-top: 10px; cursor: pointer;'>Forgot password?</p>", unsafe_allow_html=True)
                    
                    if submit:
                        if username == 'admin' and password == 'password':
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.role = selected_role
                            if selected_role == 'Intern':
                                st.session_state.user_display_name = 'Intern_1' 
                            elif selected_role == 'Mentor':
                                st.session_state.user_display_name = 'Mentor_1'
                            else:
                                st.session_state.user_display_name = f"Demo {selected_role}"
                            st.rerun()
                        elif username in USERS and USERS[username]['password'] == password:
                            user_data = USERS[username]
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.role = user_data['role']
                            st.session_state.user_display_name = user_data['name']
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                            
            with scol_image:
                 # We just inject a div that fills the space with the background image
                 st.markdown(f"""
                 <div style="height: 100%; min-height: 500px; width: 100%; border-radius: 0 12px 12px 0; {bg_image_css} background-size: cover; background-position: center; margin-left: -2rem; padding: 0;">
                 </div>
                 """, unsafe_allow_html=True)
                 
                 
    # Force the background wrapper around the centered columns
    st.markdown("""
        <script>
        // Use a script injection to target parent containers for the card look
        var blocks = window.parent.document.querySelectorAll('[data-testid="stHorizontalBlock"]');
        if (blocks.length > 0) {
            blocks[0].style.backgroundColor = 'white';
            blocks[0].style.borderRadius = '12px';
            blocks[0].style.boxShadow = '0 25px 50px -12px rgba(0, 0, 0, 0.25)';
            blocks[0].style.overflow = 'hidden';
            blocks[0].style.minHeight = '550px';
        }
        var app = window.parent.document.querySelector('.stApp');
        if(app) {
           app.style.backgroundColor = '#E5E7EB'; // Light gray backdrop
        }
        </script>
        <style>
            /* Make sure the form button mimics the reference image: blue, rounded */
            div[data-testid="stForm"] button[kind="primary"] {
                background-color: #0EA5E9 !important;
                border-color: #0EA5E9 !important;
                border-radius: 8px !important;
                color: white !important;
                padding: 0.5rem 2rem !important;
                width: auto !important;
                min-width: 120px;
                display: block;
            }
            .stTextInput>div>div>input {
                border-radius: 8px;
                border: 1px solid #E2E8F0;
                background-color: #F8FAFC;
                padding: 10px 15px;
            }
        </style>
    """, unsafe_allow_html=True)

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_display_name = None
    st.rerun()
