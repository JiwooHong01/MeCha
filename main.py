from graph import Graph
from docs import *
from state import *

from display import display
from app import user
from dotenv import load_dotenv

def main():
    load_dotenv()
    graph = Graph()
    display(graph)
    print("*" * 20 + "Prompt[rlm/rag-prompt]" + "*" * 20)
    # prompt = hub.pull("rlm/rag-prompt").pretty_print()  # Show what the prompt looks like
    user(graph)


if __name__ == "__main__":
    main()