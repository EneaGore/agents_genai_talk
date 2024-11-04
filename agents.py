from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from helper_tools import insert_score, get_scores,plot_something,format_page_links
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
import openai
from pydantic import BaseModel, Field
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.tools import tool
@tool
class Joke(BaseModel):
    """Any time the user asks for a joke this tool will be called and a joke will be returned in json format"""
    setup:str = Field(..., description="The setup of the joke")
    punchline:str = Field(..., description="The setup of the joke")
    why_funny:str = Field(..., description="The reason why the joke is funny")

class TutorAgent:
    def __init__(self,system_message, session_id="test-session"):
        print("initilaizing")
        # Initialize model, memory, and tools
        self.system_message = system_message
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.memory = InMemoryChatMessageHistory(session_id=session_id)
        all_docs = []
        file_paths = ["pdfs/reuse_ase.pdf", "pdfs/safety.pdf"]

        for file_path in file_paths:
            loader = PyPDFLoader(file_path)

            docs = loader.load()
            all_docs += docs
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(all_docs)
        vectorstore = InMemoryVectorStore.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )

        retriever = vectorstore.as_retriever()
        retriever_tool = create_retriever_tool(retriever, name="retrieve_document", description="Retrieves the pdf documents from the relevant lecture")

        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",self.system_message ),
                ("placeholder", "{chat_history}"),  # History of interactions
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),  # Internal for steps created through function calling
            ]
        )
        
        # Define the tools
        self.tools = [get_scores, insert_score, plot_something,retriever_tool,format_page_links,Joke]

        # Create the agent and executor
        self.agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools)

        # Wrap with chat history management
        self.agent_with_chat_history = RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        
        # Default configuration for the agent
        self.config = {"configurable": {"session_id": session_id}}

    def call_agent(self, prompt) -> str:
        """Calls the agent with a prompt and returns the response output."""
        response = self.agent_with_chat_history.invoke(
            {"input": prompt}, self.config
        )
        # print(response)
        return response["output"]


class NewAgent():
    def __init__(self, session_id="test-session"):
        print("initializing")
        # Initialize model, memory, and tools
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.memory = InMemoryChatMessageHistory(session_id=session_id)
        all_docs = []
        file_paths = ["pdfs/reuse_ase.pdf", "pdfs/safety.pdf"]

        for file_path in file_paths:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            all_docs += docs

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(all_docs)
        vectorstore = InMemoryVectorStore.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )

        retriever = vectorstore.as_retriever()
        retriever_tool = create_retriever_tool(retriever, name="retrieve_document", description="Retrieves the pdf documents from the relevant lecture")

        # Define the prompt template with a system message placeholder
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                ("placeholder", "{chat_history}"),  # History of interactions
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),  # Internal for steps created through function calling
            ]
        )

        # Define the tools
        self.tools = [get_scores, insert_score, plot_something, retriever_tool, format_page_links, Joke]

        # Create the agent and executor
        self.agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools)

        # Wrap with chat history management
        self.agent_with_chat_history = RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        # Default configuration for the agent
        self.config = {"configurable": {"session_id": session_id}}

    def call_agent(self, prompt, system_message) -> str:
        """Calls the agent with a prompt and returns the response output.
        Optionally takes a system_message to update the agent's behavior dynamically."""
        # Use the provided system message or the default if none is provided
        # current_system_message = system_message if system_message else self.default_system_message

        # Invoke the agent with the system message as part of the input
        response = self.agent_with_chat_history.invoke(
            {"input": prompt, "system_message": system_message}, self.config
        )
        return response["output"]


# question_answer_chain = create_stuff_documents_chain(model, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)
