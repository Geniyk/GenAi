from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables

import streamlit as st 
import os
import sqlite3
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 🔧 Updated function to load Gemini model and clean the SQL response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt[0], question])
    
    # 🔧 Clean up Gemini's output to remove ```sql or ``` formatting
    cleaned_response = response.text.strip()
    if "```" in cleaned_response:
        parts = cleaned_response.split("```")
        # Extract the SQL part inside ``` blocks
        for part in parts:
            if "SELECT" in part.upper():  # crude check for actual SQL
                cleaned_response = part.strip()
                break
    return cleaned_response

# 🔧 Updated function with error handling for SQL execution
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        rows = []
        st.error(f"SQL Error: {e}")
    finally:
        conn.close()
    return rows

# Define the Prompt
prompt = [
    """
    You are expert in converting English question to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS,
    SECTION and MARKS.

    Example 1 - How many entries of records are present?
    SQL: SELECT COUNT(*) FROM STUDENT;

    Example 2 - Tell me all the students studying in Ece(IoT) class?
    SQL: SELECT * FROM STUDENT WHERE CLASS = "Ece(IoT)";

    Only return the SQL query. Do not wrap it in ``` or use markdown.
    """
]


# Streamlit app UI
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini APP to Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    
    # 🔧 Displaying the SQL query before executing
    st.subheader("Generated SQL Query:")
    st.code(response, language='sql')

    # Run the query and display results
    data = read_sql_query(response, "student.db")
    
    st.subheader("The Response is")
    if data:
        for row in data:
            st.write(row)
    else:
        st.warning("No data found or there was an error.")
