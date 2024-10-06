import time
from functools import wraps

""" Here, we can see an example of rate limiter in the decorator aspect. the usage of that decorator is like routing
 decorators with Flask. Actually we firstly create a function that get the parameter as the input, than we use the 
 other template for creating decorators.
 
 """


# Simulated storage for rate limiting and caching
user_requests = {}
cache = {}

def rate_limiter(limit=5):
    def decorator(func):
        @wraps(func)
        def wrapper(user_id, *args, **kwargs):
            current_time = time.time()
            if user_id not in user_requests:
                user_requests[user_id] = []
            user_requests[user_id] = [t for t in user_requests[user_id] if t > current_time - 60]
            if len(user_requests[user_id]) >= limit:
                return "Too many requests, please try again later.", 429
            user_requests[user_id].append(current_time)
            return func(user_id, *args, **kwargs)
        return wrapper
    return decorator

def cache_result(func):
    @wraps(func)
    def wrapper(user_id, *args, **kwargs):
        if user_id in cache:
            return cache[user_id]
        result = func(user_id, *args, **kwargs)
        cache[user_id] = result
        return result
    return wrapper

@rate_limiter(limit=5)
@cache_result
def get_user_data(user_id):
    # Simulated user data fetching
    return {"user_id": user_id, "data": "This is user data."}

# Simulating API requests
for i in range(7):  # Simulating 7 requests from user with ID 1
    response = get_user_data(1)
    print(response)
