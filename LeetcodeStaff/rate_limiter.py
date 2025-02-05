from collections import deque
from time import time


class RateLimiter:

    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.limiter = {}

    def is_allowed(self, user_id: int) -> bool:
        curr_time = time()
        user_limiter = self.limiter.get(user_id, deque())

        if len(user_limiter) == 0:
            self.limiter[user_id] = user_limiter

        if len(user_limiter) < self.max_requests:
            user_limiter.appendleft(curr_time)
            return True

        else:
            last_timestamp = user_limiter[-1]
            if curr_time - last_timestamp > self.time_window:
                user_limiter.pop()
                user_limiter.appendleft(curr_time)
                return True
            return False

