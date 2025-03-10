from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
from langgraph.prebuilt import tools_condition
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display
from graph import Graph
from docs import *
from state import *
import pprint
from display import display
import pprint
from app import user
from langchain_core.messages import BaseMessage, HumanMessage



def main():
    
    graph = Graph()
    display(graph)
    print("*" * 20 + "Prompt[rlm/rag-prompt]" + "*" * 20)
    # prompt = hub.pull("rlm/rag-prompt").pretty_print()  # Show what the prompt looks like
    user(graph)


if __name__ == "__main__":
    main()