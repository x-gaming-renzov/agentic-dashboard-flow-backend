from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from .states.states import *
from .utils.databases import *

def get_graph():
    graph = StateGraph(ExperimentState)

    graph.add_node("get_offer_content_node", get_offer_content_node)
    graph.add_node("get_item_details_node", get_item_details_node)

    graph.add_edge(START, "get_offer_content_node")
    graph.add_edge("get_offer_content_node", "get_item_details_node")
    graph.add_edge("get_item_details_node", END)

    return graph.compile()