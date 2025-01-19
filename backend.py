import logging
from dotenv import load_dotenv
import traceback
import pandas

from src.agents.chat_agent.agent import  *
from src.agents.offer_agent.agent import register_new_chat,get_offers
from src.agents.data_agent.agent import get_metrics_dicts
from db import get_metric_ids_for_idea, insert_ideas_into_insight
from util import extract_columns_and_values
from pandas import DataFrame

def chat(chat_id,message):
    try:
        response = chat_agent(chat_id=chat_id, human_message=message)
        return response
    except Exception as e:
        logging.error(e)
        return {
            "reply" : "Sorry, something went wrong. Please try to reframe."
        }

def data_agent(chat_id,query):
    try:
        response = ask_db_agent(instructions=query,chat_id=chat_id)
        return response
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        return {
            "reply" : "Sorry, something went wrong. Please try to reframe."
        }
    
def ask_idea_agent(chat_id, query,insight_id):
    try:
        response = ask_idea_agent_to_generate_idea(instructions=query, chat_id=chat_id)
        if(response):
            idea_ids = response["idea_ids"]
            if(idea_ids):
                insert_ideas_into_insight(idea_ids, insight_id)
        return response
    except Exception as e:
        logging.error(e)
        return {
            "reply" : "Sorry, something went wrong. Please try to reframe."
        }

def ask_metric_agent(instructions : str, displayed_metrics : list[str], chat_id: str):
    try:
        response = ask_metric_agent_to_display_chart(instructions=instructions, displayed_metrics=displayed_metrics, chat_id=chat_id)
        # logging.info(f"response : {response}")
        metrics = get_metrics_dicts(response['metric_ids'])
        # logging.info(f"metrics : {metrics}")
        metric_details = None
        i = 0
        metric_count = len(metrics)
        
        result = {}
        result["metrics"] = []
        for i in range(metric_count):
            metric = metrics[i]
            metric_id = response["metric_ids"][i]
            metric_data = response["metric_dfs"][i]['metric_df']
            metric_data = DataFrame(metric_data)
            title = metric['chartOptions']['title']
            description = metric['description']
            metric_type = metric['chartType']
            # print(metric_data.columns)

            logging.info(f"metric_data : {metric_data}")
            columns,values = extract_columns_and_values(metric_data)

            for i in range(len(columns)):
                if columns[i] == "":
                    print("found empty column")
                    columns[i] = "category"


            metric_details = {
                "metric_id" : metric_id,
                "metric_type" : metric_type,
                "title" : title,
                "description" : description,
                "columns": columns,
                "values" : values
            } 

            result["metrics"].append(metric_details)

            logging.info(f"metric_details : {metric_details}")

        result["reply"] = response["reply"]
        result["metric_ids"] = response["metric_ids"]

        return result
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        return {
            "reply" : "Sorry, something went wrong. Please try to reframe"
        }

def generate_new_chat(idea_id:str):
    segments = ['1', '2']
    metrics = get_metric_ids_for_idea(idea_id)
    logging.info(f"metrics : {metrics}")
    ideas = [idea_id]
    human_remark = 'Explore personalised in-app offers for my segemnts'
    offers = get_offers(metric_ids=metrics, segment_ids=segments, human_remark=human_remark, idea_ids=ideas)
    logging.info(f"offers : {offers}")
    chat_id = register_new_chat(offers= offers)
    logging.info(f"chat_id : {chat_id}")        

    return {"chat_id" : chat_id}

if __name__ == "__main__":
    # out = chat_agent(chat_id="2", human_message="What was dau yesterday?")
    # out = data_agent(chat_id="2",query="What was dau yesterday?")
    # out = ask_idea_agent(chat_id="2", query="We should just shut this down")
    # out = ask_metric_agent(instructions="total player joins yesterday", displayed_metrics=[], chat_id="1")
    # out = ask_metric_agent(instructions="pie chart of events for last day", displayed_metrics=[], chat_id="1")
    out = generate_new_chat(idea_id="2")
    print(out)