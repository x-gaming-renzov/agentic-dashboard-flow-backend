import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from ..prompts.prompts import *
from ..states.states import *
from ..utils.databases import *

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model_large = ChatOpenAI(model="o1-preview")
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def chat_node(ChatState: ChatState) -> ChatState:
    #metric_plot = generate_metric_plot(ChatState.metric_ids)

    mongo_db = get_mongo_db()

    segments = mongo_db['segments'].find({"_id": {"$in": ChatState.segment_ids}})
    segments = list(segments)
    segments_names = [segment["name"] for segment in segments]

    ideas = mongo_db['ideas'].find({"_id": {"$in": ChatState.idea_ids}})
    ideas = list(ideas)

    with open('kb/gdd.txt', 'r') as file:
        GDD = file.read()

    metrics_dicts = get_metrics_dicts(ChatState.metric_ids)
    #"focus_metric", "segments", "metrics", "idea", "gdd", "chat_history"
    prompt = system_message_prompt.invoke({
        "focus_metric": metrics_dicts[0],
        "segment_names": segments_names,
        "metrics": metrics_dicts,
        "idea": ideas,
        "gdd": GDD,
        "segments": segments
    })

    generator_model = model.with_structured_output(AIRepsonse)

    system_message = SystemMessage(
        content=prompt.to_string())
    ai_message = AIMessage(
        content=str(ChatState.offer))
    human_message = HumanMessage(
        content=ChatState.human_message)
    response = generator_model.invoke([system_message, ai_message, human_message])

    if isinstance(response, AIRepsonse):
        ChatState.reply = response.reply
        if response.is_asking_sub_agent:
            ChatState.is_asking_sub_agent = response.is_asking_sub_agent
            ChatState.agent_instructions = response.agent_instructions

    return ChatState
    


