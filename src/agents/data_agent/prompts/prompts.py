from langchain.prompts import PromptTemplate

lead_prompt = PromptTemplate(
    template="""
You are the data analyst lead for a Minecraft server. The server records its player data in a database. You have the following information:

Database schema:
{db_schema}

Database type: {db_type}

Events in the table:
{event_data}

Table name: {table_name}

You have received the following query about the game:
{query}

Provide instructions to a junior developer who will write sql statement for you to answer the query. The instructions should only include the necessary operations to perform, relevant columnns, table, and any specific values to focus on.

#INSTRUCTIONS
1. Your instructions should be clear and concise. 
2. The exact name of the relevent columns and values should be included
3. The table name should be mentioned
4. The operations should be mentioned
5. The instructions should be written in a way that a junior developer can understand and implement them
6. The instructions should be written in a way that it is met with the goal of the query""",
input_variables=["db_data", "db_type", "event_data", "table_name", "query"])

dev_prompt = PromptTemplate(
    template="""
    You are an expert sql devloper.
You write queries as per the instruction given from your team lead.

Write a query for the following instruction for postgreSQL database:
{instruction}

# QUERY
{query}

Database schema:
{db_schema}

Events in the table:
{event_data}

Rules:
1. The query should be written in SQL
2. The query should be written as per the instruction given by the team lead
3. The query should be written in a way that it is met with the goal of the query
4. The query should be written in a way that it is optimized and efficient
5. Ensure that the query is written correctly and is free of errors
6. DOT NOT HALLUCINATE. YOUR QUERY WILL BE DIRECTLY EXECUTED ON THE DATABASE.
7. RETURN SINGLE STRING QUERRY SCRIPT CODE
""",
input_variables=["instruction", "query", "db_schema", "event_data"])