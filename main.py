from flask import Flask, request, jsonify
import logging
import dotenv

dotenv.load_dotenv()

from backend import chat, data_agent, ask_idea_agent
from cors import cors_enabled

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/chat', methods=['POST'])
@cors_enabled()
def chat_endpoint():
    """
    Endpoint to handle chat messages.
    Expects JSON input with 'chat_id' and 'message'.
    """
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        message = data.get('message')

        if not chat_id or not message:
            return jsonify({'error': 'Invalid input. chat_id and message are required.'}), 400

        response = chat(chat_id, message)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/data-agent', methods=['POST'])
@cors_enabled()
def data_agent_endpoint():
    """
    Endpoint to handle database-related queries.
    Expects JSON input with 'chat_id' and 'query'.
    """
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        query = data.get('query')

        if not chat_id or not query:
            return jsonify({'error': 'Invalid input. chat_id and query are required.'}), 400

        response = data_agent(chat_id, query)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in /data-agent endpoint: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/idea-agent', methods=['POST'])
@cors_enabled()
def idea_agent_endpoint():
    """
    Endpoint to handle idea generation requests.
    Expects JSON input with 'chat_id' and 'query'.
    """
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        query = data.get('query')

        if not chat_id or not query:
            return jsonify({'error': 'Invalid input. chat_id and query are required.'}), 400

        response = ask_idea_agent(chat_id, query)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in /idea-agent endpoint: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)
