import os, pathlib, json, dotenv
from termcolor import colored
import numpy as np
from uuid import uuid4

from langchain_openai import ChatOpenAI

from ..prompts.prompts import *
from ..states.states import *

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot
from ..utils.databases import *

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
#model_large = OllamaLLM(model="deepseek-r1:8b")
model = ChatOpenAI(model="gpt-4o-mini")
#model = ChatOpenAI(model="deepseek/deepseek-chat", api_key="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", base_url="https://openrouter.ai/api/v1")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def get_offer_content_node(ExperimentState : ExperimentState) -> ExperimentState:
    mongo_db = get_mongo_db()

    chat = mongo_db.get_collection('chats').find_one({"_id": ExperimentState.chat_id})
    print(colored(f"Chat: ", "yellow"), colored(f"{str(chat)}", "white"))
    segment_ids = chat['segments_ids']
    segments = mongo_db.get_collection('segments').find({"_id": {"$in": segment_ids}})
    segments = list(segments)

    print(colored(f"Segments: ", "yellow"), colored(f"{str(segments)}", "white"))
    
    generator_model = model.with_structured_output(SegmentOfferItemsResponse)
    generator = get_experiment_offer_prompt | generator_model

    for segment in segments:
        print(colored(f"Segment: ", "yellow"), colored(f"{str(segment)}", "white"))
        response = generator.invoke({
            "chat": chat["offers"],
            "segments": str(segment)
        })
        
        if isinstance(response, SegmentOfferItemsResponse):
            response.segment_id = segment['_id']
            ExperimentState.offers.append(response)
            print(colored(f"Offer: ", "yellow"), colored(f"{str(response)}", "white"))

    return ExperimentState

def get_item_context(item ,k=5):
    from openai import OpenAI
    client = OpenAI()

    with open('kb/item_data.json') as f:
        data = json.load(f)

    embd = client.embeddings.create(
            input=item,
            model="text-embedding-3-small"
        ).data[0].embedding

    result = []
    for i in range(len(data)):
        result.append([np.dot(embd, data[i]['embd']), data[i]['_id']])

    result.sort(key=lambda x: x[0], reverse=True)

    context = []
    for i in range(k):
        for item in data:
            if item['_id'] == result[i][1]:
                context.append(item['detailed_description'])
    return context

def get_item_details_node(ExperimentState : ExperimentState) -> ExperimentState:
    mongo_db = get_mongo_db()

    generator_model = model.with_structured_output(ItemDetailsResponse)
    generator = get_item_details_prompt | generator_model
    for offer in ExperimentState.offers:
        offer_details = {
            "offer_name": offer.offer_name,
            "offer_description": offer.offer_description,
            "items": [],
            "_id": str(uuid4().hex),
            "duration": 72
        }
        for item in offer.items:
            context = get_item_context(item)
            
            response = generator.invoke({
                "item": item,
                "context": context,
                "offer_context": offer.offer_description
            })

            if isinstance(response, ItemDetailsResponse):
                print(colored(f"Item: ", "yellow"), colored(f"{str(response)}", "white"))
                #response.set_command.replace("player_name", "player")
                offer_details["items"].append(response.model_dump())
        offer_details['segment_id'] = offer.segment_id
        ExperimentState.offer_dict[offer_details["_id"]] = offer_details
    
    mongo_db.get_collection('offers').insert_many(list(ExperimentState.offer_dict.values()))

    return ExperimentState
