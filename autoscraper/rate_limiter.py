import os
import time

# Credentials for the scraping proxy (loaded from the environment, never committed)
PROXY_API_KEY = os.environ.get("PROXY_API_KEY")


class RateLimiter:
    """Allow at most `max_calls` requests per `period` seconds."""

    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def allow(self):
        now = time.monotonic()
        # keep only timestamps inside the current window
        self.calls = [t for t in self.calls if now - t < self.period]
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False
