from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from .states.states import *
from .utils.databases import *

def get_graph():
    graph = StateGraph(OfferState)

    graph.add_node("generate_offers_node", generate_offers_node)

    graph.add_edge(START, "generate_offers_node")
    graph.add_edge("generate_offers_node", END)

    return graph.compile()

def get_offers(metric_ids : list[str], segment_ids : list[str], human_remark : str):
    graph = get_graph()

    state = graph.invoke({
        "segments_ids" : segment_ids,
        "metric_ids" : metric_ids,
        "human_remark" : human_remark
    })

    return state['offers']