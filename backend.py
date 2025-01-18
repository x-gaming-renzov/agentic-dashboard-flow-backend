import logging
from dotenv import load_dotenv
import traceback

from src.agents.chat_agent.agent import  *
from src.agents.offer_agent.agent import register_new_chat,get_offers
from db import get_metric_ids_for_idea

def chat(chat_id,message):
    try:
        response = chat_agent(chat_id=chat_id, human_message=message)
        return response
    except Exception as e:
        logging.error(e)
        return {
            "reply" : "Sorry, something went wrong. Please try again later."
        }

def data_agent(chat_id,query):
    try:
        response = ask_db_agent(instructions=query,chat_id=chat_id)
        return response
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        return {
            "reply" : "Sorry, something went wrong. Please try again later."
        }
    
def ask_idea_agent(chat_id, query):
    try:
        response = ask_idea_agent_to_generate_idea(instructions=query, chat_id=chat_id)
        return response
    except Exception as e:
        logging.error(e)
        return {
            "reply" : "Sorry, something went wrong. Please try again later."
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
    return chat_id

if __name__ == "__main__":
    # out = chat_agent(chat_id="2", human_message="What was dau yesterday?")
    # out = data_agent(chat_id="2",query="What was dau yesterday?")
    # out = ask_idea_agent(chat_id="2", query="We should just shut this down")
    out = ask_metric_agent(instructions="What was dau since 12 Jan 2025?", displayed_metrics=[], chat_id="2")
    # out = generate_new_chat(idea_id="2")
    print(out)