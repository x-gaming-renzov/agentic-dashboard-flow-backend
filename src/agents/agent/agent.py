from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from .utils.databases import *

def get_graph():
    graph = StateGraph(SegmentState)

    graph.add_node("generate_segments", generate_segments_nodes)

    graph.add_edge(START, "generate_segments")
    graph.add_edge("generate_segments", END)

    compiled_graph = graph.compile()
    return compiled_graph

def generate_segments(metrics : list[str], human_remark : str, num_segments : int) -> list[Any]:
    state = SegmentState(metrics=metrics, human_remark=human_remark, num_segments=num_segments)
    graph = get_graph()

    output = graph.invoke(state)

    return output['segments']

def register_segments(segments : list[SegmentState], metrics : list[str]) -> None:
    mongo_db = get_mongo_db()['segments']
    try:
        last_id = int(mongo_db.find_one(sort=[("_id", -1)])['_id'])
    except TypeError:
        last_id = 0
    segments_json = [segment.model_dump() for segment in segments]
    for segment in segments_json:
        last_id += 1
        segment['_id'] = str(last_id)
        segment['metrics'] = metrics
        mongo_db.insert_one(segment)
    return None
