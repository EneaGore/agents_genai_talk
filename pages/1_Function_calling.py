import streamlit as st
from langchain_openai import ChatOpenAI
from functools import reduce
from langchain_core.tools import tool

model = ChatOpenAI(model="gpt-4o-mini")

@tool
def multiply_all(*args):
    """Multiplies all the arguments together."""
    return reduce(lambda x, y: x * y, args, 1)
tools = [multiply_all]
# what is 54895 * 84865 
response = model.invoke("what is 54895 * 84865")

st.write("Normal Calling")
st.write(response.content)
st.divider()
st.write("Real Answer")
st.write(54895 * 84865)

st.divider()
llm_with_tools = model.bind_tools(tools)
response2 = model.invoke("what is 54895 * 84865")
llm_with_tools.invoke("what is 54895 * 84865")

code = """ 
@tool
def multiply_all(*args):
    "Multiplies all the arguments together."
    return reduce(lambda x, y: x * y, args, 1)
llm_with_tools = model.bind_tools(tools)
"""
st.write("Function Calling")
st.write(response2.content)