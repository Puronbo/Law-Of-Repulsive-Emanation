async def init_pipeline():
    pipeline = IngressPipeline()
    
    # 1. Observability (Non-blocking)
    pipeline.add_handler(TelemetryHandler())
    
    # 2. Safety Gates (Short-circuit immediately)
    pipeline.add_handler(EpochHandler(current_epoch=2026))
    pipeline.add_handler(VersionHandler(current_version=2, registry={1: legacy_mapper}))
    
    # 3. Logic & Analysis (Expensive)
    pipeline.add_handler(SemanticHandler(pca_engine=engine, novelty_threshold=0.85))
    
    # 4. Canary Control (Operational gate)
    pipeline.add_handler(CanaryMonitorHandler(error_budget=0.05))
    
    return pipeline