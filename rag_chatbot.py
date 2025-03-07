# rag_chatbot.py
import os
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def load_crawled_data(json_file="crawled_data.json"):
    """
    JSON 파일에서 {url: text} 구조를 읽어옴
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def build_rag_chain(json_file, openai_api_key=None):
    """
    pages_dict: {url: text} 형식의 페이지 텍스트
    openai_api_key: OpenAI API Key
    return: langchain RetrievalQA 체인
    """
    data_dict = load_crawled_data(json_file)

    # 여러 URL에서 수집한 텍스트를 합쳐서 doc 리스트 생성
    # 실제로는 URL별로 Document를 생성하는 것이 더욱 바람직할 수 있음
    combined_text = []
    for url, text in data_dict.items():
        combined_text.append(text)
    all_text = "\n".join(combined_text)

    # 텍스트를 chunk로 쪼갬
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.create_documents([all_text])

    # Embedding + VectorStore
    if openai_api_key is None:
        openai_api_key = os.environ.get("OPENAI_API_KEY", "")

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = Chroma.from_documents(docs, embeddings)

    # Retriever 생성
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # RAG 용 프롬프트 템플릿
    prompt_template = PromptTemplate(
        template="""
You are a helpful assistant. Use the following context to answer the question. 
If the context does not provide enough information, say "I don't know".
Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"]
    )

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=openai_api_key
    )

    # RetrievalQA 체인 생성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template},
        verbose=True
    )

    return qa_chain

def ask_question(rag_chain, user_question: str):
    """
    rag_chain: build_rag_chain()로 만든 체인
    user_question: 사용자 질문
    return: 답변 문자열
    """
    response = rag_chain.run(user_question)
    return response
