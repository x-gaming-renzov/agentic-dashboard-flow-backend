import logging
import dotenv
from firebase_functions import https_fn
from firebase_admin import initialize_app
from firebase_functions import options
import traceback

dotenv.load_dotenv()

from util import logger
from backend import chat, data_agent, ask_idea_agent, generate_new_chat,ask_metric_agent,generate_direct_chat
from cors import cors_enabled

# Initialize Flask app
initialize_app()

# Configure logging
logging.basicConfig(level=logging.INFO)

@https_fn.on_request(memory=options.MemoryOption.GB_1,timeout_sec=300)
@cors_enabled()
def chat_endpoint(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to handle chat messages.
    Expects JSON input with 'chat_id' and 'message'.
    """
    logger.info("Received dashboard request")
    if req.method != 'POST':
        logger.warning("Invalid method for dashboard: %s", req.method)
        return ("Method not allowed", 405)
    try:
        data = req.get_json()
        chat_id = data.get('chat_id')
        message = data.get('message')

        if not chat_id or not message:
            return {'error': 'Invalid input. chat_id and message are required.'}, 400

        response = chat(chat_id, message)
        return response,200
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        traceback.print_exc()
        return {'error': 'An error occurred while processing your request.'}, 500

@https_fn.on_request(memory=options.MemoryOption.GB_1,timeout_sec=300)
@cors_enabled()
def data_agent_endpoint(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to handle database-related queries.
    Expects JSON input with 'chat_id' and 'query'.
    """
    try:
        data = req.get_json()
        chat_id = data.get('chat_id')
        query = data.get('query')

        if not chat_id or not query:
            return {'error': 'Invalid input. chat_id and query are required.'}, 400

        response = data_agent(chat_id, query)
        return response,200
    except Exception as e:
        logging.error(f"Error in /data-agent endpoint: {e}")
        traceback.print_exc()
        return {'error': 'An error occurred while processing your request.'}, 500

@https_fn.on_request(memory=options.MemoryOption.GB_1,timeout_sec=300)
@cors_enabled()
def idea_agent_endpoint(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to handle idea generation requests.
    Expects JSON input with 'chat_id' and 'query'.
    """
    try:
        data = req.get_json()
        chat_id = data.get('chat_id')
        insight_id = data.get('insight_id')
        query = data.get('query')

        if not chat_id or not query or not insight_id:
            return {'error': 'Invalid input. chat_id, insight_id and query are required.'}

        response = ask_idea_agent(chat_id, query,insight_id)
        return response,200
    except Exception as e:
        logging.error(f"Error in /idea-agent endpoint: {e}")
        traceback.print_exc()
        return {'error': 'An error occurred while processing your request.'}, 500

@https_fn.on_request(memory=options.MemoryOption.GB_1,timeout_sec=300)
@cors_enabled()
def metric_agent_endpoint(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to handle metric display requests.
    Expects JSON input with 'instructions', 'displayed_metrics', and 'chat_id'.
    """
    try:
        data = req.get_json()
        # print(data)
        instructions = data.get('instructions')
        displayed_metrics = data.get('displayed_metrics')
        chat_id = data.get('chat_id')

        if displayed_metrics is None:
            displayed_metrics = []

        if not instructions or not chat_id:
            return {'error': 'Invalid input. instructions, displayed_metrics, and chat_id are required.'}, 400

        response = ask_metric_agent(instructions, displayed_metrics, chat_id)
        print(f"response fire : {response}")
        return response,200
    except Exception as e:
        logging.error(f"Error in /metric-agent endpoint: {e}")
        traceback.print_exc()
        return {'error': 'An error occurred while processing your request.'}, 500

@https_fn.on_request(memory=options.MemoryOption.GB_1,timeout_sec=300)
@cors_enabled()
def generate_chat_endpoint(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to generate a new chat based on an idea ID.
    Expects JSON input with 'idea_id'.
    """
    try:
        # Parse the incoming request data
        data = req.get_json()
        idea_id = data.get('idea_id')

        if not idea_id:
            return {'error': 'Invalid input. idea_id is required.'}, 400

        logging.info(f"Received request to generate chat for idea_id: {idea_id}")

        # Call the generate_new_chat function
        response = generate_new_chat(idea_id)

        # Return the chat ID in the response
        return response,200
    except Exception as e:
        logging.error(f"Error in /generate-chat endpoint: {e}")
        traceback.print_exc()
        return {'error': 'An error occurred while processing your request.'}, 500

@https_fn.on_request(memory=options.MemoryOption.GB_1,timeout_sec=300)
@cors_enabled()
def generate_direct(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to generate new chat, based on a single message
    """
    try:
        # Parse the incoming request data
        data = req.get_json()
        message = data.get('message')

        if not message:
            return {'error': 'Invalid input. message is required.'}, 400

        logging.info(f"Received request to generate chat for idea_id: {message}")

        # Call the generate_new_chat function
        response = generate_direct_chat(message)

        # Return the chat ID in the response
        return response,200
    except Exception as e:
        logging.error(f"Error in /generate-chat endpoint: {e}")
        traceback.print_exc()
        return {'error': 'An error occurred while processing your request.'}, 500