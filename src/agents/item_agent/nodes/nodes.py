import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from ..prompts.prompts import *
from ..states.states import *
from ..utils.flowutils import get_propmt_list, get_option_paths, read_json, list_subroot_instructions

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot

dotenv.load_dotenv()
JSON_PATH = pathlib.Path(__file__).parent.parent / "flow.json"
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model_large = ChatOpenAI(model="o1-preview")
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))
    
def get_multi_item_details_node(offer_description : str = None) -> Items:
    generator_model = model.with_structured_output(Items)
    generator = get_multi_item_details_prompt | generator_model
    flow_json = read_json(JSON_PATH)
    item_instructions = list_subroot_instructions(flow_json)

    response = generator.invoke({
        "offer_description": offer_description,
        "item_types": item_instructions
        # "offer_context": offer_description
    })

    if isinstance(response, Items):
        return response
    else:
        return None

if __name__ == "__main__":
    description = "designed for the competitive player, this bundle provides crucial boosts for PvP battles, enhancing both offense and defense strategies. With upgrades tailored to skills and gear, players are positioned for success in their PvP endeavors."
