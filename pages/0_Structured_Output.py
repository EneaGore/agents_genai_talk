import streamlit as st
import graphviz
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
class Joke(BaseModel):
    """A joke format, reply in a joke with this format"""
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    why_funny:str = Field(..., description="The reason why the joke is funny")

code = """
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
structured_llm = model.with_structured_output(Joke)
"""
st.code(code, language='python')
structured_llm = model.with_structured_output(Joke)
prompt =  st.text_input("Your message ")
if prompt:
    response = structured_llm.invoke(prompt)
    st.write(response)
    
st.write("JSON") 

st.latex("""G=(V,Σ,R,S) 
""")
st.latex("V (Nonterminals): Joke,String, Whitespace")
st.latex('Σ (Terminals): \{, \:  ",", \: \}, \: setup, \:punchline,\: :')
st.latex('R (Rules): Production rules that describe how the JSON object is structured.')
st.latex("S (Start Symbol): \{")


dot = graphviz.Digraph()
dot.node('whitespace1', '" "')
dot.node('whitespace2', '" "')
dot.node('whitespace3', '" "')
dot.node('setup_colon', ':')
dot.node('setup_value', '"value"')
dot.node('comma', '","')

# First level (JSON object braces)
dot.node('{', '{')
dot.node('}', '}')
dot.edge('{', 'whitespace1')
dot.edge('whitespace1', '}')


dot.node("string", "string")
dot.edge('{', 'whitespace2')
dot.edge('whitespace2', 'string')
dot.edge('string', 'whitespace3')
dot.edge('whitespace3', 'setup_colon')
dot.edge('setup_colon', 'setup_value')
dot.edge('setup_value', '}')
dot.edge('setup_value', 'comma')
dot.edge('comma', 'string')

# Display the graph in Streamlit
st.graphviz_chart(dot,True)