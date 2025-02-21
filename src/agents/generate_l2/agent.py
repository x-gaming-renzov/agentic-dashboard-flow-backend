from langgraph.graph import StateGraph, START, END
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor, as_completed

from .nodes.nodes import *
from ...utils.mongodb import get_mongo_db
from ..data_agent.agent import get_data_from_db

def get_graph():
    graph = StateGraph(L2MetricsState)

    graph.add_node("get_l2_metrics", get_l2_metrics)
    graph.add_node("get_l2_metrics_from_isntructions", get_l2_metrics_from_isntructions)

    graph.add_edge(START, "get_l2_metrics")
    graph.add_edge("get_l2_metrics", "get_l2_metrics_from_isntructions")
    graph.add_edge("get_l2_metrics_from_isntructions", END)

    compiled_graph = graph.compile()
    return compiled_graph

def generate_l2_metrics(focus_metric: str, l1_metrics: List[str], remarks: Optional[str]):
    graph = get_graph()

    state = L2MetricsState(
        focus_metric=focus_metric,
        l1_metrics=l1_metrics,
        remarks=remarks
    )

    final_state = graph.invoke(state)

    return final_state['l2_metrics']

def register_metrics(metrics : List[MetricState]):
    mongo_db = get_mongo_db()['metrics']
    last_id = int(list(mongo_db.find())[-1]['_id'])
    metrics_json = [metric.model_dump() for metric in metrics]
    for metric in metrics_json:
        last_id += 1
        metric['_id'] = str(last_id)
        mongo_db.insert_one(metric)
    with ThreadPoolExecutor() as executor:
        futures = {}
        for metric in metrics_json:
            future = executor.submit(get_data_from_db, str(metric))
            futures[metric['_id']] = future
        for future in as_completed(futures.values()):
            print(colored(f"Status: ", "yellow"), colored(f"Done", "white"))
            pass
        for future in futures:
            print(colored(f"Status: ", "yellow"), colored(f"Updating metric with data", "white"))
            mongo_db.update_one({"_id": future}, {"$set": {"query": futures[future].result()[1]}})
    metrics_ids = [metric['_id'] for metric in metrics_json]
    return metrics_ids
