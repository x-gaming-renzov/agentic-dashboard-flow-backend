import logging
from dotenv import load_dotenv
import traceback
import pandas
import asyncio
import uuid

from src.agents.chat_agent.agent import  *
from src.agents.offer_agent.agent import register_new_chat,get_offers
from src.agents.data_agent.agent import get_metrics_dicts
from experiment import get_offer_cohorts
from db import get_metric_ids_for_idea, insert_ideas_into_insight, insert_experiment, add_experiment_to_user, get_offer
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
    CACHED = {"1":"141","2":"142","3":"143"}

    if idea_id in CACHED:
        chat_id = CACHED[idea_id]
        return {"chat_id": chat_id}
    
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

def generate_direct_chat(message:str):
    segments = []
    metrics = ["1","2","3","4"]
    IDEA_PREFIX = os.getenv("IDEA_PREFIX")
    CHAT_PREFIX = os.getenv("CHAT_PREFIX")

    idea_remark = IDEA_PREFIX + " " + message
    logging.info(f"idea_remark : {idea_remark}")
    ideas = generate_ideas(metrics=metrics,
                              segments=segments,
                              num_ideas=1,
                              human_remark=idea_remark)
    
    logging.info(f"ideas : {ideas}")
    idea_ids = register_ideas(ideas_details=ideas['ideas_details'],
               segments=ideas['segments'],
               factors=ideas['factors'])
    
    chat_remark = CHAT_PREFIX + " " +  ideas["ideas_details"][0].detailed_description +  "\nThis idea is based on below human remark:\n" + idea_remark
    logging.info(f"chat_remark : {chat_remark}")
    
    offers = get_offers(metric_ids=metrics, segment_ids=segments, human_remark=chat_remark, idea_ids=idea_ids)
    logging.info(f"offers : {offers}")

    chat_id = register_new_chat(offers)
    logging.info(f"chat_id : {chat_id}")

    return {"chat_id" : chat_id}

def create_experiment_handler(chat_id, segment_ids, user_id):
    try:
        # Run the asynchronous tasks to get the offers and cohorts concurrently.
        # get_offer_cohorts returns a tuple: (offer_ids, cohort_A, cohort_B)
        offer_ids, cohort_A, cohort_B = asyncio.run(get_offer_cohorts(chat_id, segment_ids))
        logging.info(f"Offers received: {offer_ids}")
        logging.info(f"Cohort A: {cohort_A}")
        logging.info(f"Cohort B: {cohort_B}")

        # Retrieve offer details from the database for the given offer IDs.
        # get_offer returns a mapping of offer id to a dictionary of details.
        offer_details = get_offer(offer_ids)
        logging.info(f"Offer details: {offer_details}")

        experiment_ids = []  # to collect experiment IDs

        # Loop over each offer. Each experiment is generated for one offer.
        for idx, offer in enumerate(offer_ids):
            # For two offers, assign cohort_A for the first and cohort_B for the second.
            # If there are more offers than cohorts, default to an empty list.
            if idx == 0:
                variant_players = cohort_A
            elif idx == 1:
                variant_players = cohort_B
            else:
                variant_players = []

            # Get offer details; fall back to defaults if not found.
            details = offer_details.get(offer, {})
            label = details.get("offer_name", "unnamed")
            exp_description = details.get("offer_description", "sample_description")

            # Build the experiment JSON document for this offer
            experiment = {
                "_id": str(uuid.uuid4()),   # Unique experiment ID
                "label": label,               # Use the offer_name from offer details
                "exp_description": exp_description,  # Use the offer_description
                "status": "pending",          # Always pending at creation
                "segments": segment_ids,
                "groups": {
                    "control": {
                        "players": [],            # Control group players: empty array
                        "offer_id": "default",    # Fixed default offer id
                    },
                    "variant": {
                        # Map each player in the corresponding cohort to an initial value of 0
                        "players": [{player: 0} for player in variant_players],
                        "offer_id": offer,        # Offer for this experiment (offer id)
                    }
                },
                "result": {
                    # Default result values for each group
                    "control": [{
                        "name": "bought",
                        "value": 0,
                        "unit": "players"
                    }],
                    "variant": [{
                        "name": "bought",
                        "value": 0,
                        "unit": "players"
                    }]
                },
                "user":user_id
            }

            # Insert the experiment document using the DB function
            inserted_ids = insert_experiment(experiment)
            if inserted_ids:
                experiment_id = inserted_ids[0]
                # Update the user's document with the new experiment id
                add_experiment_to_user(user_id, experiment_id)
                experiment_ids.append(experiment_id)
            else:
                logging.error("Failed to insert one of the experiments.")

        return {"experiment_ids": experiment_ids}

    except Exception as e:
        logging.error(f"Error in create_experiment_handler: {e}")
        return {"error": "An error occurred while creating the experiment."}


if __name__ == "__main__":
    # out = chat_agent(chat_id="2", human_message="What was dau yesterday?")
    # out = data_agent(chat_id="2",query="What was dau yesterday?")
    # out = ask_idea_agent(chat_id="2", query="We should just shut this down")
    # out = ask_metric_agent(instructions="total player joins yesterday", displayed_metrics=[], chat_id="1")
    # out = ask_metric_agent(instructions="pie chart of events for last day", displayed_metrics=[], chat_id="1")
    # out = generate_new_chat(idea_id="2")
    # out = generate_direct_chat("We should target increasing playtime of players who have less events")
    out = create_experiment_handler(chat_id="3", segment_ids=['1', '2'], user_id="dhiru")
    print(out)