# MeCha
Medical Chatbot

## Progress 0326
### How to run
python main.py

### Database Preparation
1. crawled_resultA~Z : python cdc_scraper.py (output saved in data/raw/crawled_resultA~Z.csv)
2. remove unnecessary sentences : removedup_sent.py -> output saved in data/dataset_raw/A~Z.csv
3. remove unnecessary sentences : removedup_sent2.py -> output saved in data/dataset2/A~Z.csv
4. remove unnecessary words : removedup_word.py -> output saved in data/dataset/A~Z.csv

### graph.py
1. get Graph from graph.py
- LangGraph 기반으로 에이전트(Agent) + 도구(Retriever) + 노드 간 조건 분기 로직을 연결한 상태 그래프(StateGraph) 를 정의
-> “질문이 들어오면 → 필요 시 도구를 호출하여 RAG 검색 → 검색 결과를 바탕으로 최종 답을 생성” 하는 흐름을 그래프 형태로 모델링

- Graph() 함수: StateGraph를 만든 뒤, 노드와 에지(Edges)를 설정하고 compile하여 최종 그래프 객체를 반환.
- add_node("agent", agent): 노드 이름이 “agent”이고, 실제 실행 로직(함수)은 agent (임포트된 Python 함수).

- ToolNode(tools): “retrieve” 노드는 툴을 실행하는 노드. 예를 들어 RAG의 검색 도구(리트리버)를 호출.

- rewrite와 generate 등은 질문 재작성, 최종 답변 생성 등을 담당.

2. 그래프 시작 시, “agent” 노드부터 실행.
- tools_condition 함수가 실행 결과를 반환하면, 그 값에 따라 다른 노드로 이동.=
- 예: agent가 “어떤 툴을 호출해야겠다”고 하면 → “retrieve” 노드로, 그렇지 않으면 → END (바로 종료).
- “retrieve” 노드 실행 후, grade_documents 함수로 분기.
- 예: 검색 결과(문서)가 질문과 관련 있는지 “grade_documents”가 확인 → “generate” 또는 “rewrite” 노드로 이동.


### state.py
AgentState: 그래프를 돌 때 관리할 상태를 정의하는 TypedDict.
- messages 필드: 여러 메시지들을 append하는 방식을 사용(add_messages). 즉, 노드가 실행될 때마다 새 메시지를 상태에 추가.
- 이렇게 하면 에이전트가 주고받은 대화가 한곳에 모입니다.
이 함수는 “검색된 문서(docs)가 사용자 질문(question)과 관련 있는지”를 판단 → 결과로 "generate" 또는 "rewrite" 문자열을 반환.
그래프에서 “retrieve” 노드 실행 후, 다음 노드를 결정하는 조건 함수 역할.
- | 파이프 연산: LangChain에서 프롬프트를 LLM에 연결해 “체인”을 만든다는 의미.




### Todo
지금 줄글로 나오는 걸
1. 진단명 + 확률
2. 치료법
3. 추가 질문

