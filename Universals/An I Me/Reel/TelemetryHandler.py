import time

class TelemetryHandler(PipelineHandler):
    async def handle(self, ctx: IngressContext) -> bool:
        ctx.start_time = time.perf_counter()
        # Continue to next handler
        return True
    
    def log_metrics(self, ctx: IngressContext):
        latency = time.perf_counter() - ctx.start_time
        if not ctx.is_valid:
            # Export to Prometheus/Datadog
            print(f"Halt event: {ctx.short_circuit_reason} | Latency: {latency}")