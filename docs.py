from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from setup import _set_env

def docs_retriever():
    _set_env("OPENAI_API_KEY")
    names = ["A", "B"]
    # names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    docs = [CSVLoader(file_path="data/dataset/" + name + ".csv").load() for name in names]
    docs_list = [item for sublist in docs for item in sublist]
    # print("docs_list")
    # print(docs_list)
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add to vectorDB
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(),
    )
    retriever = vectorstore.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "Retrieve_from_CDC",
        "Search and return information about diseases",
    )
    return [retriever_tool]

tools = docs_retriever()