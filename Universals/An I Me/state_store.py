import logging

logger = logging.getLogger("FencedStateStore")

class FencedStateStore:
    def __init__(self):
        self.last_token = 0
        self.data = {}

    def commit_write(self, token, payload):
        if token < self.last_token:
            logger.warning(f"Rejected stale fencing token: {token} (Last: {self.last_token})")
            return False
        
        self.last_token = token
        self.data.update(payload)
        return True