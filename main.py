import logging
import dotenv
from firebase_functions import https_fn
from firebase_admin import initialize_app
from firebase_functions import options

dotenv.load_dotenv()

from util import logger
from backend import chat, data_agent, ask_idea_agent
from cors import cors_enabled

# Initialize Flask app
initialize_app()

# Configure logging
logging.basicConfig(level=logging.INFO)

@https_fn.on_request(memory=options.MemoryOption.GB_1)
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
        return {'error': 'An error occurred while processing your request.'}, 500

@https_fn.on_request(memory=options.MemoryOption.GB_1)
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
        return {'error': 'An error occurred while processing your request.'}, 500

@https_fn.on_request(memory=options.MemoryOption.GB_1)
@cors_enabled()
def idea_agent_endpoint(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to handle idea generation requests.
    Expects JSON input with 'chat_id' and 'query'.
    """
    try:
        data = req.get_json()
        chat_id = data.get('chat_id')
        query = data.get('query')

        if not chat_id or not query:
            return {'error': 'Invalid input. chat_id and query are required.'}

        response = ask_idea_agent(chat_id, query)
        return response,200
    except Exception as e:
        logging.error(f"Error in /idea-agent endpoint: {e}")
        return {'error': 'An error occurred while processing your request.'}, 500

