import os, pathlib, json, dotenv
from termcolor import colored
import numpy as np
from uuid import uuid4

from langchain_openai import ChatOpenAI

from ..prompts.prompts import *
from ..states.states import *

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot
from ....utils.db_pool import execute_sql_query
from ....utils.mongodb import get_mongo_db
from ..utils.chatutils import *

from ...item_agent.agent import get_items

dotenv.load_dotenv()

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def get_offer_content_node(ExperimentState : ExperimentState) -> ExperimentState:
    mongo_db = get_mongo_db()

    chat = mongo_db.get_collection('chats').find_one({"_id": ExperimentState.chat_id})
    # # print(colored(f"Chat: ", "yellow"), colored(f"{str(chat)}", "white"))
    segment_ids = chat['segments_ids']
    segments = mongo_db.get_collection('segments').find({"_id": {"$in": segment_ids}})
    segments = list(segments)

    # print(colored(f"Segments: ", "yellow"), colored(f"{str(segments)}", "white"))
    
    generator_model = model.with_structured_output(SegmentOfferItemsResponse)
    generator = get_experiment_offer_prompt | generator_model

    for segment in segments:
        #print(colored(f"Segment: ", "yellow"), colored(f"{str(segment)}", "white"))
        response = generator.invoke({
            "chat": chat["offers"],
            "segments": str(segment)
        })
        
        if isinstance(response, SegmentOfferItemsResponse):
            response.segment_id = segment['_id']
            ExperimentState.offers.append(response)
            # print(colored(f"Offer: ", "yellow"), colored(f"{str(response)}", "white"))

    ExperimentState.chat = extract_chat_history(chat_json=chat)
    # print(colored(f"Chat: ", "yellow"), colored(f"{str(ExperimentState.chat)}", "white"))
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

def getbundlecontext(chat_history) -> Bundles:
    generator_model = model.with_structured_output(Bundles)
    generator = get_bundle_prompt | generator_model

    response = generator.invoke({
        "chat_history": chat_history
    })

    if(isinstance(response, Bundles)):
        return response
    else:
        #log error
        return Bundles(bundles=[])


def getbundlecontext(chat_history) -> Bundles:
    generator_model = model.with_structured_output(Bundles)
    generator = get_bundle_prompt | generator_model

    response = generator.invoke({
        "chat_history": chat_history
    })

    if(isinstance(response, Bundles)):
        return response
    else:
        #log error
        return Bundles(bundles=[])


def get_item_details_node(ExperimentState : ExperimentState) -> ExperimentState:
    mongo_db = get_mongo_db()
    bundles = getbundlecontext(ExperimentState.chat)
    # print(colored(f"Bundles: ", "yellow"), colored(f"{str(bundles)}", "white"))

    i = 0
    for offer in ExperimentState.offers:
        offer_details = {
            "offer_name": offer.offer_name,
            "offer_description": offer.offer_description,
            "items": [],
            "_id": str(uuid4().hex),
            "duration": 72
        }

        offer_details['segment_id'] = offer.segment_id
        items = get_items(bundles.bundles[i].new_bundle_items)

        offer_details['items'] = items
        bundle_idx = "bundle_" + str(i)
        offer_details[bundle_idx] = {}
        offer_details[bundle_idx]['name'] = bundles.bundles[i].bundle_name
        offer_details[bundle_idx]['old'] = bundles.bundles[i].original_bundle_items
        offer_details[bundle_idx]['new'] = bundles.bundles[i].new_bundle_items

        ExperimentState.offer_dict[offer_details["_id"]] = offer_details
        # print(colored(f"Offer: ", "yellow"), colored(f"{str(offer_details)}", "white"))
        i = i+1
    
    mongo_db.get_collection('offers').insert_many(list(ExperimentState.offer_dict.values()))

    return ExperimentState
