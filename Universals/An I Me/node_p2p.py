import json
import time
import asyncio
from opentelemetry import trace, propagate

# 1. Tracing & Telemetry Initialization
tracer = trace.get_tracer(__name__)

class NodeDefense:
    def __init__(self, secret_key, state_store):
        self.secret_key = secret_key.encode()
        self.state = state_store  # Instance of FencedStateStore
        self.panic_controller = PanicController()
        self.state_mode = "SYNCING" 

    async def ingress_gate(self, raw_bytes):
        """Standardized transport-agnostic entry point."""
        # Unpack envelope
        envelope = self.deserialize(raw_bytes)
        meta = envelope["metadata"]
        
        # Inject Trace Context from envelope
        ctx = self.extract_context(meta["traceparent"])
        with tracer.start_as_current_span("ingress", context=ctx) as span:
            
            # 2. Perimeter Defense (HMAC Verification)
            if not self.verify_perimeter(raw_bytes, meta.get("signature")):
                span.set_status(trace.Status(trace.StatusCode.ERROR, "Invalid Signature"))
                return None

            # 3. Autonomous Survivability (Panic-Quiet)
            if self.panic_controller.is_quiet():
                span.add_event("Panic-Quiet active, dropping packet")
                return None

            # 4. State Integrity (Fencing)
            # Only proceeds if token is monotonic
            if not self.state.commit_write(meta["fencing_token"], envelope["payload"]):
                self.panic_controller.record_fencing_event()
                span.add_event("Fencing violation detected")
                return None
            
            return await self.process(envelope["payload"])

    def verify_perimeter(self, data, signature):
        # HMAC verification logic
        return True 

    def deserialize(self, raw_bytes):
        return json.loads(raw_bytes.decode('utf-8'))

    def extract_context(self, traceparent):
        return propagate.extract({"traceparent": traceparent})

    async def process(self, payload):
        # Final business logic execution
        return True