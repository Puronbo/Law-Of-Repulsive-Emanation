class EpochHandler(PipelineHandler):
    def __init__(self, current_epoch: int):
        self.current_epoch = current_epoch

    async def handle(self, ctx: IngressContext) -> bool:
        if ctx.epoch < self.current_epoch:
            ctx.halt("Stale Epoch")
            return False
        return True

class VersionHandler(PipelineHandler):
    def __init__(self, current_version: int, registry: dict):
        self.current_version = current_version
        self.registry = registry

    async def handle(self, ctx: IngressContext) -> bool:
        p_ver = ctx.version_state.get("currentVersion", 1)
        if p_ver != self.current_version:
            if p_ver in self.registry:
                ctx.semantic_vector = self.registry[p_ver].transform(ctx.semantic_vector)
            else:
                ctx.halt("Incompatible version")
                return False
        return True