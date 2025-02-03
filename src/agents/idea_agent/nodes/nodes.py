import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from ..prompts.prompts import *
from ..states.states import *
from ..utils.databases import *

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model_large = ChatOpenAI(model="gpt-4o")
model = ChatOpenAI(model="gpt-4o-mini")
#model_large = ChatOllama(model="llama3.2:3b")
#model = ChatOllama(model="llama3.2:3b")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def generate_factors(IdeaState: IdeaState) -> IdeaState:
    metrics_dicts = get_metrics_dicts(IdeaState.metrics)
    focus_metric = get_metrics_dicts(['0'])
    plots = generate_metric_plot(IdeaState.metrics)
    IdeaState.plots = plots

    with open('kb/gdd.txt', 'r') as file:
        gdd = file.read()

    mongo_db = get_mongo_db()['segments']
    segment_ids = IdeaState.segments
    segments = mongo_db.find({"_id": {"$in": segment_ids}})
    segment_names = [segment['name'] for segment in segments]

    prompt = factor_prompt.invoke({
        "focus_metrics": str(focus_metric),
        "segment_name": str(segment_names),
        "segment_details": str(segments),
        "metrics": str(metrics_dicts),
        "gdd": gdd,
        "human_remark": IdeaState.human_remark,
    })

    content = [
        {"type": "text", "text": prompt.to_string()},
    ]

    for plot in plots:
        print(plot[:min(100, len(plot))])
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{plot}"},
        })

    message = HumanMessage(content=content)

    response = model.invoke([message])

    IdeaState.factors = response.content

    return IdeaState

def generate_ideas_node(IdeaState: IdeaState) -> IdeaState:
    metrics_dicts = get_metrics_dicts(IdeaState.metrics)
    focus_metric = get_metrics_dicts(['0'])

    with open('kb/gdd.txt', 'r') as file:
        gdd = file.read()

    mongo_db = get_mongo_db()['segments']
    segment_ids = IdeaState.segments
    segments = mongo_db.find({"_id": {"$in": segment_ids}})
    segment_names = [segment['name'] for segment in segments]

    prompt = ideas_prompt.invoke({
        "focus_metrics": str(focus_metric),
        "segment_name": str(segment_names),
        "segment_details": str(segments),
        "metrics": str(metrics_dicts),
        "gdd": gdd,
        "human_remark": IdeaState.human_remark,
        "num_ideas": IdeaState.num_ideas,
        "factors": IdeaState.factors,
    })

    content = [
        {"type": "text", "text": prompt.to_string()},
    ]

    for plot in IdeaState.plots:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{plot}"},
        })

    message = HumanMessage(content=content)
    generator_model = model_large.with_structured_output(IdeaDetailResponse)
    response = generator_model.invoke([message])

    if isinstance(response, IdeaDetailResponse):
        IdeaState.ideas_details = response.ideas_details

    return IdeaState