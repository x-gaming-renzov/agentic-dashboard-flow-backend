def extract_chat_history(chat_json):
    # Extract the chat history from the provided JSON
    chat_history = chat_json.get("chat_history", [])
    
    # Ignore the very first entry and extract messages from remaining chat history
    result = []
    for entry in chat_history[1:]:  # Start from index 1 to skip the first entry
        # Check if the type is "human" or "ai" and get the message
        if entry['type'] in ['human', 'ai']:
            message = entry['content']
            if isinstance(message, list):
                # If content is a list, extract the message from it
                message = ''.join([msg['text'] for msg in message if isinstance(msg, dict) and 'text' in msg])
            result.append({entry['type']: message})
    
    return result