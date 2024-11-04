from db_control import ScoreDatabase
from langchain.tools import tool
import streamlit as st

db = ScoreDatabase()

@tool
def insert_score(submissionId, submission, score):
    """Inserts a new record into the scores table."""
    db.insert_score(submissionId, submission, score)

@tool
def get_scores():
    """Displays all records from the scores table."""
    return db.show_scores()

@tool
def plot_something(scores):
    """Plots a simple graph to the Streamlit app."""
    st.write("This is a simple plot:")
    st.line_chart({"data": scores})

@tool
def format_page_links(file_name, page):
    """_summary_: Formats the page links for a given file."""
    print(file_name)

    return "https://www.moodle.tum.de/pluginfile.php/4231110/mod_folder/content/0/ASE22%20Chapter%202.5%20Safety%20in%20Software%20Engineering.pdf?forcedownload=0#page="+str(page)
    
    
    
