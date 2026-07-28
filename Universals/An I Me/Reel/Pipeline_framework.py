class IngressPipeline:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler: PipelineHandler):
        self.handlers.append(handler)

    async def execute(self, ctx: IngressContext) -> bool:
        for handler in self.handlers:
            if not await handler.handle(ctx):
                return False
        return True