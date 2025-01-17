from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage

from .nodes.nodes import *
from .utils.databases import *

def get_graph():
    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)

    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile()

def chat_agent(chat_id : str, human_message: str):
    mongo_db = get_mongo_db()
    chat = mongo_db['chats'].find_one({"_id" : chat_id})
    graph = get_graph()

    out = graph.invoke({
    "human_message": "fetch dau",
    "segment_ids" : chat['segments_ids'],
    "metric_ids" : chat['metric_ids'],
    "idea_ids" : chat['idea'],
    "chat_history" : chat['chat_history']})

    ai_message = AIMessage(
        content = str(out['reply']))
    chat['chat_history'].append(ai_message.model_dump())

    mongo_db['chats'].update_one({"_id" : chat_id}, {"$set" : {"chat_history" : chat['chat_history']}})

    response =  {
        "reply" : out['reply'],
    }

    if 'is_asking_sub_agent' in out:
        response['is_asking_sub_agent'] = out['is_asking_sub_agent']
        response['agent_instructions'] = {
            "instructions" : str(out['agent_instructions']['agent_instructions']),
            "agent_name" : out['agent_instructions']['agent_name']
        }

    return response