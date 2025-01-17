import functools
from firebase_functions import https_fn

def cors_enabled(allowed_origins=None):
    """
    Decorator to add CORS support to Firebase Cloud Functions
    
    :param allowed_origins: List of allowed origin domains 
                             If None, defaults to allowing all origins
    """
    if allowed_origins is None:
        allowed_origins = ['*']  # Allow all origins by default
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(req: https_fn.Request) -> https_fn.Response:
            # Preflight request handling
            if req.method == 'OPTIONS':
                headers = {
                    'Access-Control-Allow-Origin': allowed_origins[0],
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Max-Age': '3600'
                }
                return ('', 204, headers)
            
            # CORS headers for actual request
            headers = {
                'Access-Control-Allow-Origin': allowed_origins[0]
            }
            
            try:
                # Call the original function
                result = func(req)
                
                # If result is a tuple, append headers
                if isinstance(result, tuple):
                    if len(result) == 2:
                        return (*result, headers)
                    elif len(result) == 3:
                        # If headers already exist, update them
                        result_headers = result[2].copy()
                        result_headers.update(headers)
                        return (result[0], result[1], result_headers)
                
                return result
            
            except Exception as e:
                # Ensure CORS headers are sent with error responses
                return ({'error': str(e)}, 500, headers)
        
        return wrapper
    
    return decorator