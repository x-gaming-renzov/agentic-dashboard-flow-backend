import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI

from ..prompts.prompts import *
from ..states.states import *
from ..utils.databases import execute_sql_query
import traceback

from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

dotenv.load_dotenv()
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 

print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))

def generate_instructions(DataQuerryState : DataQuerryState) -> DataQuerryState:
    generator = lead_prompt | model
    DataQuerryState.instruction = generator.invoke({
        "db_schema": DataQuerryState.db_schema,
        "db_type": "postgresql",
        "event_data": DataQuerryState.event_data,
        "table_name": DataQuerryState.table_name,
        "query": DataQuerryState.human_query
    }).content

    print(colored(f"Status: ", "green"), colored(f"Instructions generated", "white"))
    #print(colored(f"Instructions: ", "white"), colored(f"{DataQuerryState.instruction}", "yellow"))
    return DataQuerryState

def generate_query(DataQuerryState : DataQuerryState) -> DataQuerryState:
    generator_model = model.with_structured_output(QuerryResponse)
    generator = dev_prompt | generator_model
    response = generator.invoke({
        "instruction": DataQuerryState.instruction,
        "query": DataQuerryState.human_query,
        "db_schema": DataQuerryState.db_schema,
        "event_data": DataQuerryState.event_data,
    })
    if isinstance(response, QuerryResponse):
        DataQuerryState.query = response.querry
    print(colored(f"Status: ", "green"), colored(f"Query generated", "white"))
    #print(colored(f"Query: ", "white"), colored(f"{DataQuerryState.query}", "yellow"))
    return DataQuerryState

def execute_query(DataQuerryState: DataQuerryState):
    """Execute SQL query."""
    try : 
        DataQuerryState.data = execute_sql_query(DataQuerryState.query)
        DataQuerryState.should_retry = False
        print(colored(f"Status: ", "green"), colored(f"Query executed", "white"))
        # print(colored(f"Data: ", "white"), colored(f"{DataQuerryState.data}", "yellow"))
    except Exception as e:
        traceback.print_exc()
        error_note = f"""
Developer ran into an error while executing your instructions. Here is the error message:
{e}

Developer's querry was query was:
{DataQuerryState.query}

Your instructions were:
{DataQuerryState.instruction}

Retry again with a different query.
        """
        DataQuerryState.human_query += error_note
        DataQuerryState.should_retry = True
        print(colored(f"Status: ", "red"), colored(f"Error while executing query", "white"))
        print(colored(f"Error: ", "white"), colored(f"{e}", "red"))

    return DataQuerryState

def should_retry(DataQuerryState: DataQuerryState) -> str:
    if DataQuerryState.should_retry:
        print(colored(f"Status: ", "red"), colored(f"Retrying", "white"))
        return "generate_query"
    return "END"

def qa_test(DataQuerryState: DataQuerryState) -> DataQuerryState:
    generator_model = model.with_structured_output(QaResponse)
    generator = qa_prompt | generator_model
    response = generator.invoke({
        "query": DataQuerryState.human_query,
        "instruction": DataQuerryState.instruction,
        "dev_query": DataQuerryState.query,
        "data": str(DataQuerryState.data)[:min(100, len(str(DataQuerryState.data)))]
    })
    if isinstance(response, QaResponse):
        DataQuerryState.qa_status = response.ok
    print(colored(f"Status: ", "green"), colored(f"QA test completed", "white"))
    # print(colored(f"QA Status: ", "white"), colored(f"{DataQuerryState.qa_status}", "yellow"))

    # print(colored(f"Remarks: ", "white"), colored(f"{response.remarks}", "yellow"))
    remark_note = str(response.remarks)
    DataQuerryState.human_query += remark_note
    return DataQuerryState

def qa_filter(DataQuerryState: DataQuerryState) -> str:
    if DataQuerryState.qa_status :
        print(colored(f"Status: ", "green"), colored(f"QA passed", "white"))
        return "END"
    return "generate_instructions"