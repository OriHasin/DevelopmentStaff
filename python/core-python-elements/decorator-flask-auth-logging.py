from functools import wraps
from flask import Flask, request

""" In web frameworks like Flask or Django, you often use decorators to implement middleware functionalities. 
Middleware can be used for logging, authentication, input validation, and response formatting.

Explanation:
The order of execution for decorators is from bottom to top.
1. @authenticate will run first (because it's closest to the function).
2. @log_request will run next.
3. @app.route runs last to register the route.

So the flow is:
1. @authenticate: Checks user authentication.
2. @log_request: Logs the request details.
3. The function `get_data` is called if all decorators pass.
"""

app = Flask(__name__)

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Request: {request.method} {request.path}")
        return func(*args, **kwargs)
    return wrapper

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        print('Authrization' in request.headers)
        if not token or token != "valid_token":
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

@app.route('/data', methods=['GET'])
@log_request
@authenticate
def get_data():
    return {"data": "This is the secured data."}

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
