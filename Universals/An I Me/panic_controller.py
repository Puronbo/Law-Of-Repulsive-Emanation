import time
import logging

logger = logging.getLogger("PanicController")

class PanicController:
    def __init__(self, threshold=3, window=60):
        self.threshold = threshold
        self.window = window
        self.fencing_history = []
        self.is_throttled = False
        self.quiet_until = 0

    def record_fencing_event(self):
        now = time.monotonic()
        self.fencing_history.append(now)
        # Keep events only within the current window
        self.fencing_history = [t for t in self.fencing_history if now - t < self.window]
        
        if len(self.fencing_history) >= self.threshold:
            self.is_throttled = True
            self.quiet_until = now + 300 # 5-minute quiet period
            logger.critical("Threshold breached. Panic-Quiet mode activated for 300s.")

    def is_quiet(self):
        if self.is_throttled:
            if time.monotonic() > self.quiet_until:
                self.is_throttled = False
                logger.info("Panic-Quiet expired. Resuming operations.")
                return False
            return True
        return False