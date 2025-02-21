from langgraph.graph import StateGraph, START, END

from .nodes.nodes import *
from ...utils.db_pool import execute_sql_query

def get_items(offer_description: str):
    items = get_multi_item_details_node(offer_description)
    items_with_command = get_multi_item_commands(items)
    return items_with_command