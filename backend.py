import logging
from dotenv import load_dotenv
import traceback

from src.agents.chat_agent.agent import  *

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

if __name__ == "__main__":
    # out = chat_agent(chat_id="2", human_message="What was dau yesterday?")
    # out = data_agent(chat_id="2",query="What was dau yesterday?")
    out = ask_idea_agent(chat_id="2", query="We should just shut this down")
    print(out)