from openai import OpenAI
# import os
from setup import _set_env
import sys
from dotenv import load_dotenv

# 발급받은 OpenAI API 키를 설정하세요.

def translate_korean_to_english(korean_text: str) -> str:
    load_dotenv()
    _set_env("OPENAI_API_KEY")

    # sys.setdefaultencoding('utf8')


    """
    ChatGPT API를 사용해 한국어 텍스트를 영어로 번역하는 함수.
    
    :param korean_text: 한국어 문자열
    :return: 영어로 번역된 문자열
    """
    # korean_text = (korean_text).encode('utf-8')


    client = OpenAI()
    # ChatGPT에게 한국어 -> 영어 번역을 명시적으로 요청하기 위해 system/message를 구성합니다.
    # temperature=0.0으로 설정하면 결과가 더 일관적입니다.
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful translator who accurately translates Korean text into English. First: Detect the language of the input text Second: Translate the input text from the detected language in first step to the English language Third: Return output only the translated text not add up the description."
            },
            {
                "role": "user",
                "content": f"Please translate the following Korean text into English:\n'{korean_text}'"
            }
        ],
        temperature=0.0
    )
    
    # API의 응답에서 번역된 텍스트를 추출
    translated_text = response.choices[0].message.content
    return translated_text

# 예시 사용
if __name__ == "__main__":
    korean_input = "hello"
    english_output = translate_korean_to_english(korean_input)
    print("번역 결과:", english_output)
