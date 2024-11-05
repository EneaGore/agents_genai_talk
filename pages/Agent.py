import streamlit as st
from agents import TutorAgent
st.set_page_config(
    page_title="Cool Stuff",
    page_icon=":llama:",
)
option = st.selectbox(
    "How would you like to be contacted?",
    ("What is safety in the context of software engineering?", "What is security in the context of software engineering?", "Mobile phone"),
    index=0,
    # placeholder="Select contact method...",
)

st.write("You selected:", option)
problem_statement = """ What is safety in the context of software engineering?"""
st.write(f"## {option}")

grading_instructions =""" 1 point for anything that makes any sense """
system_message = f"""
You are a tutor at a prestigious university. An excellent univeristy one might say.
You are tasked with grading student submissions. You have access to the database to answer more queries.
Your goal it to communicate with the students and provide them with feedback which will guide them to find the correct solution.
The problem statement of the task is as follows: {option}
The maximum score for this task is 10 points.
If they are given you can use this grading instructions from the professor to orient yourself in how to grade: {grading_instructions}
If no grading instructions are given you can use your own judgement to grade the submission using the Retrieval Augmented generation method provided.
Keep in mind that your answers are shown in streamlit, which can read markdown.
If the user asks for page numbers use the correct format for the page number with the provided function.
"""

if 'agent' not in st.session_state:
    st.session_state.agent = TutorAgent()
    st.session_state.history = []
    
    
prompt =  st.chat_input("Your message ")

if(prompt):
    st.write(st.session_state.agent.call_agent(prompt,system_message), unsafe_allow_html=True)
    
with st.expander("View History"):
    st.write(st.session_state.agent.memory)