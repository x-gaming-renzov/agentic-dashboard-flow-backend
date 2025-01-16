import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI

from ..prompts.prompts import *
from ..states.states import *
from ..utils.databases import execute_sql_query

from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model = ChatOpenAI(model="gpt-4o-mini")
model_large = ChatOpenAI(model="gpt-4o")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def generate_instructions(DataQuerryState : DataQuerryState) -> DataQuerryState:
    generator = lead_prompt | model
    DataQuerryState.instruction = generator.invoke({
        "db_schema": DataQuerryState.db_schema,
        "db_type": "postgresql",
        "event_data": DataQuerryState.event_data,
        "table_name": DataQuerryState.table_name,
        "query": DataQuerryState.query
    }).content

    print(colored(f"Status: ", "green"), colored(f"Instructions generated", "white"))
    print(colored(f"Instructions: ", "white"), colored(f"{DataQuerryState.instruction}", "yellow"))
    return DataQuerryState

def generate_query(DataQuerryState : DataQuerryState) -> DataQuerryState:
    generator_model = model_large.with_structured_output(QuerryResponse)
    generator = dev_prompt | generator_model
    response = generator.invoke({
        "instruction": DataQuerryState.instruction,
        "query": DataQuerryState.query,
        "db_schema": DataQuerryState.db_schema,
        "event_data": DataQuerryState.event_data,
    })
    if isinstance(response, QuerryResponse):
        DataQuerryState.query = response.querry
    print(colored(f"Status: ", "green"), colored(f"Query generated", "white"))
    print(colored(f"Query: ", "white"), colored(f"{DataQuerryState.query}", "yellow"))
    return DataQuerryState

def execute_query(DataQuerryState: DataQuerryState):
    """Execute SQL query."""
    try : 
        DataQuerryState.data = execute_sql_query(DataQuerryState.query)
        DataQuerryState.should_retry = False
        print(colored(f"Status: ", "green"), colored(f"Query executed", "white"))
        print(colored(f"Data: ", "white"), colored(f"{DataQuerryState.data}", "yellow"))
    except Exception as e:
        error_note = f"""
YOu ran into an error while executing the query. Here is the error message:
{e}

Your query was:
{DataQuerryState.query}

Retry again with a different query.
        """
        DataQuerryState.instruction += error_note
        DataQuerryState.should_retry = True
        print(colored(f"Status: ", "red"), colored(f"Error while executing query", "white"))
        print(colored(f"Error: ", "white"), colored(f"{e}", "red"))

    return DataQuerryState

def should_retry(DataQuerryState: DataQuerryState) -> str:
    if DataQuerryState.should_retry:
        print(colored(f"Status: ", "red"), colored(f"Retrying", "white"))
        return "generate_query"
    return "END"