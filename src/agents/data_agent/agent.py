from langgraph.graph import StateGraph, START, END
import pandas as pd
import os, dotenv
import json
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


from .nodes.nodes import *
from .utils.databases import get_mongo_db, execute_sql_query
dotenv.load_dotenv()

def get_graph():
    graph = StateGraph(DataQuerryState)

    graph.add_node("generate_instructions", generate_instructions)
    graph.add_node("generate_query", generate_query)
    graph.add_node("execute_query", execute_query)
    graph.add_node("qa_test", qa_test)

    graph.add_edge(START, "generate_instructions")
    graph.add_edge("generate_instructions", "generate_query")
    graph.add_edge("generate_query", "execute_query")
    graph.add_conditional_edges("execute_query", should_retry,{
        "generate_query" : "generate_instructions",
        "END" : "qa_test"
    })
    graph.add_conditional_edges("qa_test", qa_filter, {
        "generate_instructions" : "generate_instructions",
        "END" : END
    })

    compiled_graph = graph.compile()
    return compiled_graph

def get_data_from_db(query : str):
    graph = get_graph()
    with open('src/agents/data_agent/kb/events.txt', 'r') as file:
        event_data = file.read()
    with open('src/agents/data_agent/kb/schema.txt', 'r') as file:
        schema = file.read()

    state = DataQuerryState(
        db_type="postgresql",
        event_data=event_data,
        table_name="data",
        human_query=query,
        db_schema=schema
    )

    final_state = graph.invoke(state)

    return final_state['data'], final_state['query']

def fetch_metric_data(id : str) -> pd.DataFrame:
    mongo_db = get_mongo_db()
    metric_dict = mongo_db['charliedemo']['metrics'].find_one({"_id": id})

    if metric_dict is None:
        return None
    
    try:
        data = execute_sql_query(metric_dict['query'])
    except Exception as e:
        print(f"Error: {e}")
        data, query = get_data_from_db(f"Make sure the query is correct. Error: {e}. If not, correct it and return the data. Metric detail : {metric_dict}")
        mongo_db['charliedemo']['metrics'].update_one({"_id": id}, {"$set": {"query": query}})
    
    if metric_dict['chartType'] == 'line':
        xAxis_name = metric_dict['chartOptions']['xAxis']
        yAxis_name = metric_dict['chartOptions']['yAxis']
        data = pd.DataFrame(data, columns=[xAxis_name, yAxis_name])
        try: 
            data[xAxis_name] = pd.to_datetime(data[xAxis_name])
        except:
            pass
        data = data.sort_values(by=xAxis_name)
        data = data.reset_index(drop=True)
    elif metric_dict['chartType'] == 'bar':
        xAxis_name = metric_dict['chartOptions']['xAxis']
        yAxis_name = metric_dict['chartOptions']['yAxis']
        data = pd.DataFrame(data, columns=[xAxis_name, yAxis_name])
        data = data.sort_values(by=yAxis_name, ascending=False)
        data = data.reset_index(drop=True)
    elif metric_dict['chartType'] == 'pie':
        categories_name = metric_dict['chartOptions']['categories']
        values_name = metric_dict['chartOptions']['values']
        percentages = []

        data = pd.DataFrame(data, columns=[categories_name, values_name])

        sum_values = data[values_name].sum()

        for i in range(len(data)):
            percentages.append(data[values_name][i]/sum_values)

        data['percentages'] = percentages
        data = data.sort_values(by=values_name, ascending=False)
        data = data.reset_index(drop=True)
    elif metric_dict['chartType'] == 'metric':
        data = pd.DataFrame(data, columns=['value'])

    else:
        data = pd.DataFrame(data)

    return data

def generate_metric_plot(ids : list) -> List[str]:
    plots = []
    for id in ids:
        metric_data = fetch_metric_data(id)
        metric_dict = get_mongo_db()['charliedemo']['metrics'].find_one({"_id": id})
        if metric_data is None:
            return "Metric not found"
        
        if metric_data.shape[0] == 0:
            return "No data found for the metric"

        metric_dict = get_mongo_db()['charliedemo']['metrics'].find_one({"_id": id})
        title = metric_dict['name']
        if metric_dict['chartType'] == 'line':
            x = metric_data[metric_data.columns[0]]
            y = metric_data[metric_data.columns[1]]
            labels = [metric_dict['chartOptions']['xAxis'], metric_dict['chartOptions']['yAxis']]
            
            base64_plot = get_base64_plot('line', x, y, labels, title=title)
            plots.append(base64_plot)
        elif metric_dict['chartType'] == 'bar':
            x = metric_data[metric_data.columns[0]]
            y = metric_data[metric_data.columns[1]]
            labels = [metric_dict['chartOptions']['xAxis'], metric_dict['chartOptions']['yAxis']]
            base64_plot = get_base64_plot('bar', x, y, labels, title=title)
            plots.append(base64_plot)
        elif metric_dict['chartType'] == 'pie':
            x = metric_data[metric_data.columns[0]]
            y = metric_data[metric_data.columns[1]]
            base64_plot = get_base64_plot('pie', y, categories=x, title=title)
            plots.append(base64_plot)
        
    return plots
    
def get_base64_plot(plot_type, x, y=None, labels=None, categories=None, title=None):
    # Create the plot based on the specified type
    plt.figure()
    if plot_type == 'line':
        plt.plot(x, y)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
        plt.title(title)
    elif plot_type == 'bar':
        plt.bar(x, y)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
        plt.title(title)
    elif plot_type == 'pie':
        if labels:
            plt.pie(x, labels=categories, autopct='%1.1f%%')
        else:
            plt.pie(x, autopct='%1.1f%%')
        plt.title(title)
    else:
        raise ValueError("Unsupported plot type. Use 'line', 'bar', or 'pie'.")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Encode the buffer content to Base64
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    #plt.show()

    # Close the plot to free memory
    plt.close()
    print(colored(f"Status: ", "green"), colored(f"Plot generated", "white"))
    return base64_string

def get_metrics_dicts(ids : list) -> List[Dict[str, Any]]:
    metrics = []
    for id in ids:
        metric_dict = get_mongo_db()['charliedemo']['metrics'].find_one({"_id": id})
        if metric_dict is None:
            return "Metric not found"
        metrics.append(metric_dict)
    return metrics