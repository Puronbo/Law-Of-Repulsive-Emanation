@dataclass
class IngressContext:
    raw_bytes: bytes
    epoch: int
    version_state: Dict[str, Any]
    semantic_vector: Optional[list] = None
    is_valid: bool = True
    short_circuit_reason: Optional[str] = None

    def halt(self, reason: str):
        self.is_valid = False
        self.short_circuit_reason = reason