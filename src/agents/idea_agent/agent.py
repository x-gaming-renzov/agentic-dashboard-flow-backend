from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from ...utils.db_pool import execute_sql_query

def get_graph():
    graph = StateGraph(IdeaState)

    graph.add_node("generate_factors", generate_factors)
    graph.add_node("generate_ideas", generate_ideas_node)

    graph.add_edge(START, "generate_factors")
    graph.add_edge("generate_factors", "generate_ideas")
    graph.add_edge("generate_ideas", END)

    compiled_graph = graph.compile()
    return compiled_graph

def generate_ideas(metrics : list[str], 
                   segments : list[int], 
                   human_remark : str = "What are in-app purchase ideas opportunities for this segments?", 
                   num_ideas : int = 3) -> list[Any]:
    state = IdeaState(metrics=metrics, human_remark=human_remark, num_ideas=num_ideas, segments=segments)
    graph = get_graph()

    output = graph.invoke(state)

    return output

def register_ideas(ideas_details : list[IdeasDetails], segments : list[str], factors : str) -> None:
    mongo_db = get_mongo_db()['ideas']
    idea_ids = []
    try:
        last_id = int(list(mongo_db.find())[-1]['_id'])
    except TypeError:
        last_id = 0
    ideas_json = [idea.model_dump() for idea in ideas_details]
    for idea in ideas_json:
        last_id += 1
        idea['_id'] = str(last_id)
        idea['segments'] = segments
        idea['factors'] = factors
        mongo_db.insert_one(idea)
        idea_ids.append(idea['_id'])
    return idea_ids