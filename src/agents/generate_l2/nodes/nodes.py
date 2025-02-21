import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI

from ..prompts.prompts import *
from ..states.states import *
from ....utils.db_pool import execute_sql_query
from ....utils.mongodb import get_mongo_db

from ...data_agent.agent import get_metrics_dicts

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model_large = ChatOpenAI(model="o1-preview")
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def get_l2_metrics(L2MetricsState : L2MetricsState) -> L2MetricsState:
    generator_model = model_large
    generator = l2_prompt | generator_model

    l1_metrics = get_metrics_dicts(L2MetricsState.l1_metrics)

    with open('kb/events.txt', 'r') as file:
        event_data = file.read()
    
    with open('kb/schema.txt', 'r') as file:
        schema = file.read()

    with open('kb/gdd.txt', 'r') as file:
        gdd = file.read()
    
    with open('kb/metric_guide.txt', 'r') as file:
        metric_guide = file.read()

    response = generator.invoke({
        "sql_schema": schema,
        "event_types": event_data,
        "GDD": gdd,
        "metric_guide": metric_guide,
        "focus_metric": L2MetricsState.focus_metric,
        "l1_metrics": str(l1_metrics),
        "remarks": L2MetricsState.remarks
    })

    L2MetricsState.l2_instructions = response.content
    # print(colored(f"Status: ", "yellow"), colored(f"Instructions: {response.content}", "white"))

    return L2MetricsState

def get_l2_metrics_from_isntructions(L2MetricsState : L2MetricsState) -> L2MetricsState:
    generator_model = model.with_structured_output(L2MetricStructuredResponse)
    generator = l2_out_prompt | generator_model

    l1_metrics = get_metrics_dicts(L2MetricsState.l1_metrics)

    with open('kb/events.txt', 'r') as file:
        event_data = file.read()
    
    with open('kb/schema.txt', 'r') as file:
        schema = file.read()

    with open('kb/gdd.txt', 'r') as file:
        gdd = file.read()
    
    with open('kb/metric_guide.txt', 'r') as file:
        metric_guide = file.read()

    response = generator.invoke({
        "sql_schema": schema,
        "event_types": event_data,
        "GDD": gdd,
        "focus_metric": L2MetricsState.focus_metric,
        "l1_metrics": str(l1_metrics),
        "remarks": L2MetricsState.remarks,
        "l2_metrics": L2MetricsState.l2_metrics
    })

    if isinstance(response, L2MetricStructuredResponse):
        L2MetricsState.l2_metrics = response.metrics
        # print(colored(f"Status: ", "yellow"), colored(f"Metrics: {response.metrics}", "white"))
    else:
        print(colored(f"Error: ", "red"), colored(f"Response is not of type L2MetricStructuredResponse", "white"))

    return L2MetricsState

def ask_metric_agent_to_display_chart_node(instructions: str) -> ShouldGenerateNewMetric | None:
    generator_model = model.with_structured_output(NewMetricResponse)
    
    mongo_db = get_mongo_db()['metrics']
    metrics = list(mongo_db.find())

    generator = display_metric_prompt | generator_model

    response = generator.invoke({
        "instructions": instructions
    })

    if isinstance(response, NewMetricResponse):
        generator_model = model.with_structured_output(ShouldGenerateNewMetric)
        generator = should_generate_new_metric_prompt | generator_model

        response = generator.invoke({
            "metric_details": response.new_metrics_to_display,
            "existing_metrics": metrics
        })

        if isinstance(response, ShouldGenerateNewMetric):
            return response
        else:
            print(colored(f"Error: ", "red"), colored(f"Response is not of type ShouldGenerateNewMetric", "white"))
            return None
    else:
        print(colored(f"Error: ", "red"), colored(f"Response is not of type NewMetricResponse", "white"))
        return None
