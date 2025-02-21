import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from ..prompts.prompts import *
from ..states.states import *
from ....utils.db_pool import execute_sql_query
from ....utils.mongodb import get_mongo_db
from ..utils.kbutils import format_armor_enchantments

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model = ChatOpenAI(model="o1")
# model = ChatOpenAI(model="deepseek/deepseek-chat", api_key="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", base_url="https://openrouter.ai/api/v1")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

# NODE : 1 -> generate bundle theme/idea
# NODE : 2 -> fetch relevant items | kb/knowledge agent
# NODE : 3 -> generate offers

def generate_offers_node(OfferState : OfferState) -> OfferState:
    metric_plot = generate_metric_plot(OfferState.metric_ids)

    mongo_db = get_mongo_db()
    segments = mongo_db['segments'].find({"_id": {"$in": OfferState.segments_ids}})
    segments = list(segments)
    segments_names = [segment["name"] for segment in segments]
    ideas = mongo_db['ideas'].find({"_id": {"$in": OfferState.idea}})
    ideas = list(ideas)
    
    with open('kb/gdd.txt', 'r') as file:
        GDD = file.read()

    json_data = {}
    with open('kb/categorized_data.json', 'r') as f:
        json_data = json.load(f)

    items = format_armor_enchantments(json_data)

    prompt = offer_prompt.invoke({
        "segment_names": segments_names,
        "idea": ideas,
        "segments": segments,
        "GDD": GDD,
        "human_remark": OfferState.human_remark,
        "items":items
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
    ai_message = AIMessage(content=response.content)
    OfferState.chat_history = [message, ai_message]
    OfferState.offers = response.content

    return OfferState