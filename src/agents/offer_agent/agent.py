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

def get_offers(metric_ids : list[str], segment_ids : list[str], human_remark : str, idea_ids : list[str]):
    graph = get_graph()

    state = graph.invoke({
        "segments_ids" : segment_ids,
        "metric_ids" : metric_ids,
        "human_remark" : human_remark,
        "idea" : idea_ids
    })

    return state

def register_new_chat(offers : Dict) -> None:
    mongo_db = get_mongo_db()['chats']
    try:
        last_id = int(list(mongo_db.find())[-1]['_id'])
    except TypeError:
        last_id = 0
    offers_json = {
        "segments_ids": offers['segments_ids'],
        "metric_ids": offers['metric_ids'],
        "human_remark": offers['human_remark'],
        "idea": offers['idea'],
        "offers": offers['offers'],
        "chat_history": [message.model_dump() for message in offers['chat_history']]
    }
    last_id += 1
    offers_json['_id'] = str(last_id)
    mongo_db.insert_one(offers_json)
    return None