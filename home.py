import streamlit as st
import dotenv

dotenv.load_dotenv()
st.set_page_config(
    page_title="Words and Stuff",
    page_icon=":llama:",
)
code = '''def hello():
    print("Hello, Streamlit!")'''

code_pydnatic = '''class Irony(BaseModel):
    print("Hello, Streamlit!")'''

st.write("# Welcome")
st.divider()
st.write("## Structured Output")
st.write("## Function Calling")
st.write("## Agent Demo")
