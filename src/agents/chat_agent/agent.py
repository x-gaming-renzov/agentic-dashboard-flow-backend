from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from .utils.databases import *

def get_graph():
    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)

    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile()

