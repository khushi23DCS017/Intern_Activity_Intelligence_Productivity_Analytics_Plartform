import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

from utils.db_config import get_db_uri

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_sql_agent(role: str, username: str, db_uri: str = None):
    """
    Creates a LangChain SQL agent connected to the specified database URI.
    Uses Groq for the LLM. It injects custom system prompts based on the user's role to restrict data access.
    
    In the future, simply change the db_uri to your Postgres connection string:
    'postgresql+psycopg2://user:password@localhost/dbname'
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        raise ValueError("Groq API Key is missing. Add GROQ_API_KEY to your .env file (see .env.example)")

    if db_uri is None:
        db_uri = get_db_uri()

    # Connect to PostgreSQL
    db = SQLDatabase.from_uri(db_uri)

    # Initialize the LLM (Groq - fast, free tier available)
    llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

    # Define Role-Based System Prompts for Security and Context
    base_instructions = """
    You are a helpful, professional AI analytics assistant for the 'Kenexai Intern Activity Intelligence Platform'.
    Your job is to answer questions by querying the SQL database. 
    The database tracks intern learning progress, courses, mentors, and daily activities logged in hours.
    Always return your final answer in clean, readable Markdown format. Do NOT expose internal IDs, use the actual names (e.g., intern_name, course_name).
    """

    if role == "HR_Manager":
        role_instructions = """
        The current user is an HR Manager. They have full access to all organization data.
        Feel free to run aggregate queries comparing different interns, mentors, and departments.
        """
    elif role == "Team_Manager":
        role_instructions = """
        The current user is a Team Manager. Focus primarily on productivity and the 'fact_activity' table.
        You can analyze time allocation across different task types (Coding, Debugging, etc.).
        """
    elif role == "Mentor":
        role_instructions = f"""
        The current user is a Mentor named '{username}'. 
        CRITICAL SECURITY RULE: You MUST ONLY query data for interns where the mentor is '{username}'. 
        If you join the dim_intern or dim_mentor tables, always include `WHERE mentor_name = '{username}'`. 
        If the user asks about an intern assigned to a different mentor, respectfully decline to answer citing privacy constraints.
        """
    elif role == "Intern":
        # Note: In our mock auth, the username for interns is like 'intern1', but the display name is 'Intern_1'
        # We assume `username` passed here is the Display Name matching the dimension table.
        role_instructions = f"""
        The current user is an Intern named '{username}'. 
        CRITICAL SECURITY RULE: You MUST ONLY query data where the intern_name is '{username}'.
        Always append `WHERE intern_name = '{username}'` or equivalent joins to restrict the data.
        Refuse any request to view another intern's data, test scores, or activities. You are their personal study buddy.
        """
    else:
        role_instructions = "You have standard read-only access to the analytics."

    system_message = base_instructions + "\n" + role_instructions

    # Create the Agent using tool-calling (Groq supports Llama tool use)
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=True,
        agent_executor_kwargs={
            "handle_parsing_errors": True,
        }
    )

    # We attach the specialized system prompt dynamically
    def safe_query(question: str):
        full_prompt = f"System Instructions: {system_message}\n\nUser Question: {question}"
        try:
            result = agent_executor.invoke({"input": full_prompt})
            return result["output"]
        except Exception as e:
            return f"⚠️ I encountered an error running that query: {str(e)}"

    return safe_query
