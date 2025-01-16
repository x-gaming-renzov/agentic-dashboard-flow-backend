import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from ..prompts.prompts import *
from ..states.states import *

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model_large = ChatOpenAI(model="o1-preview")
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))
