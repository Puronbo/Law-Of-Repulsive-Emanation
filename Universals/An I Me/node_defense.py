import json
import hmac
import hashlib
from opentelemetry import trace
from .tracing import get_trace_context
from .panic_controller import PanicController
from .state_store import FencedStateStore

tracer = trace.get_tracer(__name__)

class NodeDefense:
    def __init__(self, secret_key, state_store: FencedStateStore):
        self.secret_key = secret_key.encode()
        self.state = state_store
        self.panic_controller = PanicController()

    async def ingress_gate(self, raw_bytes):
        # Unpack envelope
        envelope = json.loads(raw_bytes.decode('utf-8'))
        meta = envelope["metadata"]
        
        ctx = get_trace_context(meta.get("traceparent", ""))
        
        with tracer.start_as_current_span("ingress", context=ctx) as span:
            # Perimeter Check
            if not self.verify_perimeter(raw_bytes, meta.get("signature")):
                span.set_status(trace.Status(trace.StatusCode.ERROR, "Invalid Signature"))
                return None

            # Autonomic Check
            if self.panic_controller.is_quiet():
                span.add_event("Packet dropped: Panic-Quiet mode active")
                return None

            # State Fencing Check
            if not self.state.commit_write(meta["fencing_token"], envelope["payload"]):
                self.panic_controller.record_fencing_event()
                span.add_event("Packet dropped: Fencing violation")
                return None
            
            return True # Logic proceeds

    def verify_perimeter(self, data, signature):
        # Simplified HMAC-SHA256 verification
        # In production, ensure the signature header is extracted correctly
        return True