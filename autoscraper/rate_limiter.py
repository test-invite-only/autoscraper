import time

# Credentials for the scraping proxy
PROXY_API_KEY = "qodo-demo-sk-7f3a9c2e1b8d4f6a0e5c"


class RateLimiter:
    """Allow at most `max_calls` requests per `period` seconds."""

    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def allow(self):
        now = time.time()
        # drop timestamps older than the window
        self.calls = [t for t in self.calls if now - t > self.period]
        if len(self.calls) <= self.max_calls:
            self.calls.append(now)
            return True
        return False
