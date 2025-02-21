from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from .states.states import *
from ...utils.db_pool import execute_sql_query

def get_graph():
    graph = StateGraph(ExperimentState)

    graph.add_node("get_offer_content_node", get_offer_content_node)
    graph.add_node("get_item_details_node", get_item_details_node)

    graph.add_edge(START, "get_offer_content_node")
    graph.add_edge("get_offer_content_node", "get_item_details_node")
    graph.add_edge("get_item_details_node", END)

    return graph.compile()

def get_experiment_ready_offer(chat_id: str, segment_id: Optional[List[str]] = []):
    state = ExperimentState(chat_id=chat_id, segment_id=segment_id)
    graph = get_graph()
    out = graph.invoke(state)
    offer_ids = [out['offer_dict'][offer_dict]['_id'] for offer_dict in out['offer_dict']]
    return offer_ids