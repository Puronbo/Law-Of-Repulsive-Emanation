class SemanticHandler(PipelineHandler):
    def __init__(self, pca_engine, novelty_threshold: float):
        self.pca = pca_engine
        self.threshold = novelty_threshold

    async def handle(self, ctx: IngressContext) -> bool:
        # ctx.semantic_vector must exist here
        if ctx.semantic_vector is None:
            ctx.halt("Missing semantic data")
            return False
            
        score = self.pca.calculate_novelty(ctx.semantic_vector)
        if score > self.threshold:
            ctx.halt(f"Novelty Panic: {score}")
            return False
        return True