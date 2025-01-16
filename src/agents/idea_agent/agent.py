from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from .utils.databases import *

def get_graph():
    graph = StateGraph(IdeaState)

    graph.add_node("generate_factors", generate_factors)
    graph.add_node("generate_ideas", generate_ideas)

    graph.add_edge(START, "generate_factors")
    graph.add_edge("generate_factors", "generate_ideas")
    graph.add_edge("generate_ideas", END)

    compiled_graph = graph.compile()
    return compiled_graph
