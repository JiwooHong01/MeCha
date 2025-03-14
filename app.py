import pprint
from langchain_core.messages import BaseMessage, HumanMessage
from translator import *

def user(graph):
    print("질문을 입력하면 RAG 챗봇이 답변합니다. (종료하려면 exit)")
    while True:
        user_input = input("질문: ")
        if user_input.lower() in ["exit", "quit"]:
            print("종료합니다.")
            break

        # korean_input = "안녕하세요? 저는 한국어를 영어로 번역하는 모델입니다."
        user_input = translate_korean_to_english(user_input)
        # print("번역 결과:", english_output)

        inputs = {
            "messages": [
                ("user", user_input),
            ]
        }

        # answer = ask_question(rag_chain, user_input)
        # print(f"답변: {answer}\n")
        for output in graph.stream(inputs):
            for key, value in output.items():
                pprint.pprint(f"Output from node '{key}':")
                pprint.pprint("---")
                value = translate_english_to_korean(value)
                pprint.pprint(value, indent=2, width=80, depth=None)
            pprint.pprint("\n---\n")
    # inputs = {
    #     "messages": [
    #         ("user", "What does Lilian Weng say about the types of agent memory?"),
    #     ]
    # }
    # for output in graph.stream(inputs):
    #     for key, value in output.items():
    #         pprint.pprint(f"Output from node '{key}':")
    #         pprint.pprint("---")
    #         pprint.pprint(value, indent=2, width=80, depth=None)
    #     pprint.pprint("\n---\n")