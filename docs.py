from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from setup import _set_env

def docs_retriever():
    _set_env("OPENAI_API_KEY")

    # urls = [
    #     "https://lilianweng.github.io/posts/2023-06-23-agent/",
    #     "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    #     "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    # ]

    # docs = [WebBaseLoader(url).load() for url in urls]
    # docs_list = [item for sublist in docs for item in sublist]

    # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    #     chunk_size=100, chunk_overlap=50
    # )
    # doc_splits = text_splitter.split_documents(docs_list)
    names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    # names = ["A", "B"]
    docs = [CSVLoader(file_path="data/raw/crawled_results" + name + ".csv").load() for name in names]
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
        "retrieve_blog_posts",
        "Search and return information about Lilian Weng blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
    )
    return [retriever_tool]

tools = docs_retriever()