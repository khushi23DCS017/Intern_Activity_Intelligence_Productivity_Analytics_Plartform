import streamlit as st
from utils.genai_agent import get_sql_agent

def ai_chatbot_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 AI Data Assistant (Groq)")
    st.sidebar.success("✅ GenAI Ready")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I can query our SQL database. What would you like to know?"}]
        
    # Display chat history
    for message in st.session_state.chat_history:
        with st.sidebar.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.sidebar.chat_input("Ask me a question about the data...")
    if prompt:
        # Echo user prompt
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.sidebar.chat_message("user"):
            st.markdown(prompt)
            
        with st.sidebar.chat_message("assistant"):
            with st.spinner("Analyzing data..."):
                try:
                    # Get user context for security
                    role = st.session_state.get('role', 'Unknown')
                    username = st.session_state.get('user_display_name', 'Unknown')
                    
                    # Initialize the agent (uses PostgreSQL from .env)
                    agent_query = get_sql_agent(role, username)
                        
                    # Get the response
                    response = agent_query(prompt)
                    st.markdown(response)
                except Exception as e:
                    response = f"Error: {str(e)}"
                    st.error(response)
        
        # Save assistant response
        st.session_state.chat_history.append({"role": "assistant", "content": response})
