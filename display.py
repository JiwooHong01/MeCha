from IPython.display import Image, display
from graph import Graph

def display(graph):
    try:
        display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        pass