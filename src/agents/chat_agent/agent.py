from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage

from .nodes.nodes import *
from .utils.databases import get_mongo_db as get_mongo_db_from_chat_agent
from ..generate_l2.agent import ask_metric_agent_to_display_chart_node, register_metrics
from ..generate_l2.states.states import ShouldGenerateNewMetric

from ..data_agent.agent import *
from ..idea_agent.agent import *

from concurrent.futures import ThreadPoolExecutor, as_completed

def get_graph():
    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)

    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile()

def chat_agent(chat_id : str, human_message: str):
    mongo_db = get_mongo_db_from_chat_agent()
    chat = mongo_db['chats'].find_one({"_id" : chat_id})
    graph = get_graph()

    out = graph.invoke({
    "human_message": human_message,
    "segment_ids" : chat['segments_ids'],
    "metric_ids" : chat['metric_ids'],
    "idea_ids" : chat['idea'],
    "chat_history" : chat['chat_history']})

    human_message = HumanMessage(
        content = human_message)
    ai_message = AIMessage(
        content = str(out['reply']))
    chat['chat_history'].append(human_message.model_dump())
    chat['chat_history'].append(ai_message.model_dump())

    mongo_db['chats'].update_one({"_id" : chat_id}, {"$set" : {"chat_history" : chat['chat_history']}})

    response =  {
        "reply" : out['reply'],
    }

    if 'is_asking_sub_agent' in out:
        response['is_asking_sub_agent'] = out['is_asking_sub_agent']
        response['agent_instructions'] = {
            "instructions" : str(out['agent_instructions'].agent_instructions),
            "agent_name" : out['agent_instructions'].agent_name
        }

    return response

def ask_db_agent(instructions : str, chat_id : str):
    data, query_code = get_data_from_db(query = instructions)

    mongo_db = get_mongo_db_from_chat_agent()
    chat = mongo_db['chats'].find_one({"_id" : chat_id})
    graph = get_graph()

    tool_output = str(data)

    if len(tool_output) > 5000:
        tool_output = tool_output[:5000]

    tool_output = f"""
DB AGENT's response for your query : 
here's result of data you requested : 
{tool_output}

your instructions was : {instructions}
"""
    out = graph.invoke({
    "human_message": tool_output,
    "segment_ids" : chat['segments_ids'],
    "metric_ids" : chat['metric_ids'],
    "idea_ids" : chat['idea'],
    "chat_history" : chat['chat_history']})

    ai_message = AIMessage(content=str(out['reply']))
    chat['chat_history'].append(ai_message.model_dump())

    mongo_db['chats'].update_one({"_id" : chat_id}, {"$set" : {"chat_history" : chat['chat_history']}})

    response =  {
        "reply" : out['reply'],
    }

    return response

def ask_idea_agent_to_generate_idea(instructions : str, chat_id : str):
    mongo_db = get_mongo_db_from_chat_agent()
    chat = mongo_db['chats'].find_one({"_id" : chat_id})

    metric_ids = chat['metric_ids']
    segment_ids = chat['segments_ids']

    ideas = generate_ideas(metrics=metric_ids, segments=segment_ids, human_remark=instructions)
    idea_ids = register_ideas(ideas_details=ideas['ideas_details'], segments=segment_ids, factors=ideas['factors'])

    return {
        'idea_ids' : idea_ids
    }

def ask_metric_agent_to_display_chart(instructions : str, displayed_metrics : list[str], chat_id: str):
    mongo_db = get_mongo_db_from_chat_agent()
    chat = mongo_db['chats'].find_one({"_id" : chat_id})
    response = ask_metric_agent_to_display_chart_node(instructions=instructions)

    def genrate_response(metric_id : str):
        plot = generate_metric_plot([metric_id])

        content = [
            {
                "type" : "text",
                "text" : f"Here's the plot for metric :"
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{plot}"},
            }
        ]

        ai_message = AIMessage(
            content = content
        )

        chat['chat_history'].append(ai_message.model_dump())

        graph = get_graph()

        out = graph.invoke({
        "human_message": instructions,
        "segment_ids" : chat['segments_ids'],
        "metric_ids" : chat['metric_ids'],
        "idea_ids" : chat['idea'],
        "chat_history" : chat['chat_history']})

        ai_message = AIMessage(content=str(out['reply']))
        chat['chat_history'].append(ai_message.model_dump())

        mongo_db['chats'].update_one({"_id" : chat_id}, {"$set" : {"chat_history" : chat['chat_history']}})

        response =  {
            "reply" : out['reply']
        }

        return response

    if isinstance(response, ShouldGenerateNewMetric):
        if not response.should_generate_new_metric:
            reply = genrate_response(response.exsiting_metric_id)
            if response.exsiting_metric_id in displayed_metrics:
                reply['metric_ids'] = displayed_metrics
            else:
                displayed_metrics.append(response.exsiting_metric_id)
                chat['metric_ids'] = displayed_metrics
                reply['metric_ids'] = displayed_metrics
            
        elif response.should_generate_new_metric:
            metric = register_metrics([response.new_metric])
            reply = genrate_response(metric[0])
            displayed_metrics.append(metric[0])
            reply['metric_ids'] = displayed_metrics
            chat['metric_ids'] = displayed_metrics
    
    mongo_db['chats'].update_one({"_id" : chat_id}, {"$set" : {"metric_ids" : chat['metric_ids']}})

    metric_ids = chat['metric_ids']
    metric_dfs = []
    
    for metric_id in metric_ids:
        metric_dfs.append({
            "metric_id" : metric_id,
            "metric_df" : fetch_metric_data(metric_id)
        })
        #print(metric_dfs)

    reply['metric_dfs'] = metric_dfs

    return reply



            
        


