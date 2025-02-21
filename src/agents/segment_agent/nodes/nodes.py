import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from ..prompts.prompts import *
from ..states.states import *

from ...data_agent.agent import get_metrics_dicts, generate_metric_plot

dotenv.load_dotenv()

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model_large = ChatOpenAI(model="o1-preview")
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))



def generate_segments_nodes(SegmentState : SegmentState) -> SegmentState:
    generator_model = model.with_structured_output(SegmentsResponse)

    metrics = get_metrics_dicts(SegmentState.metrics)

    with open('kb/events.txt', 'r') as file:
        event_data = file.read()
    
    with open('kb/schema.txt', 'r') as file:
        data_schema = file.read()

    with open('kb/gdd.txt', 'r') as file:
        gdd = file.read()

    plots = generate_metric_plot(SegmentState.metrics)

    prompt = segmentation_prompt.invoke({
        "num_segments": SegmentState.num_segments,
        "human_remark": SegmentState.human_remark,
        "metrics": metrics,
        "data_schema": data_schema,
        "events": event_data,
        "gdd": gdd
    })

    content = [
        {"type": "text", "text": prompt.to_string()},
    ]

    for plot in plots:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{plot}"},
        })
    
    message = HumanMessage(content=content)
    response = generator_model.invoke([message])

    if isinstance(response, SegmentsResponse):
        SegmentState.segments = response.segments

    return SegmentState

