class CanaryMonitorHandler(PipelineHandler):
    def __init__(self, error_budget: float):
        self.error_budget = error_budget
        self.fails = 0
        self.total = 0

    async def handle(self, ctx: IngressContext) -> bool:
        self.total += 1
        if not ctx.is_valid:
            self.fails += 1
            if (self.fails / self.total) > self.error_budget:
                ctx.halt("Error budget exceeded - Automated Rollback")
                return False
        return True