import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from ..prompts.prompts import *
from ..states.states import *
from ..utils.databases import *

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def generate_offers_node(OfferState : OfferState) -> OfferState:
    metrics_dicts = get_metrics_dicts(OfferState.metric_ids)
    metric_plot = generate_metric_plot(OfferState.metric_ids)

    mongo_db = get_mongo_db()['segments']
    segments = mongo_db.find({"_id": {"$in": OfferState.segments_ids}})
    segments = list(segments)
    segments_names = [segment["name"] for segment in segments]

    with open('kb/gdd.txt', 'r') as file:
        GDD = file.read()

    prompt = offer_prompt.invoke({
        "segment_names": segments_names,
        "idea": OfferState.idea,
        "segments": segments,
        "GDD": GDD,
        "human_remark": OfferState.human_remark
    })

    content = [
        {
            "type": "text",
            "text": prompt.to_string()
        }
    ]

    for plot in metric_plot:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{plot}"},
        })

    message = HumanMessage(content=content)

    response = model.invoke([message])

    OfferState.offers = response.content

    return OfferState