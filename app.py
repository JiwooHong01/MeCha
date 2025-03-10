import pprint
from langchain_core.messages import BaseMessage, HumanMessage


def user(graph):
    inputs = {
        "messages": [
            ("user", "What does Lilian Weng say about the types of agent memory?"),
        ]
    }
    for output in graph.stream(inputs):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")