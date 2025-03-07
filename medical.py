# main.py
import os
import getpass

from rag_chatbot import build_rag_chain, ask_question

def main():
    # 1) OpenAI API Key 설정
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY: ")

    # 2) 크롤링 시작 URL 및 깊이 설정
    file_name = "crawled_data.json"
    if not os.path.exists(file_name):
        print(f"파일 {file_name}이(가) 없습니다. 먼저 crawler.py를 실행해 주세요.")
        return
    

    # 3) RAG 체인 빌드
    print("RAG 체인을 구성합니다...")
    rag_chain = build_rag_chain(file_name)

    # 4) 질의응답 루프
    print("질문을 입력하면 RAG 챗봇이 답변합니다. (종료하려면 exit)")
    while True:
        user_input = input("질문: ")
        if user_input.lower() in ["exit", "quit"]:
            print("종료합니다.")
            break

        answer = ask_question(rag_chain, user_input)
        print(f"답변: {answer}\n")

if __name__ == "__main__":
    main()
