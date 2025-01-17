import functools
from flask import make_response, request

def cors_enabled(allowed_origins=None):
    """
    Decorator to add CORS support to Flask routes.
    
    :param allowed_origins: List of allowed origin domains. 
                            If None, defaults to allowing all origins ('*').
    """
    if allowed_origins is None:
        allowed_origins = ['*']  # Allow all origins by default
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Handle OPTIONS preflight request
            if request.method == 'OPTIONS':
                response = make_response('', 204)
                response.headers['Access-Control-Allow-Origin'] = allowed_origins[0]
                response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Max-Age'] = '3600'
                return response

            # Call the original function for other HTTP methods
            response = func(*args, **kwargs)

            # Ensure the response has CORS headers
            if isinstance(response, tuple):
                data, status = response[0], response[1]
                headers = response[2] if len(response) > 2 else {}
                headers['Access-Control-Allow-Origin'] = allowed_origins[0]
                return data, status, headers
            elif isinstance(response, dict) or isinstance(response, str):
                response = make_response(response)
            
            response.headers['Access-Control-Allow-Origin'] = allowed_origins[0]
            return response

        return wrapper
    return decorator
