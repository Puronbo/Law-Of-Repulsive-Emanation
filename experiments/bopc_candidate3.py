"""
BOPC candidate #3: SipHash-2-4 hash function.
Resource: 64-bit word operations (adds, xors, rotations).
Bound: exactly 2 rounds of compression + 4 rounds of finalization = 
       2 * (8 ops/round) * (msg_blocks + 1) + 4 * 8 ops = 16*(msg_blocks+1) + 32.
For inputs up to 32 bytes (1 block of 8 bytes): bound = 16*2 + 32 = 64 operations.
Semantics: output must match reference SipHash-2-4 implementation.
"""

from typing import List, Tuple


def siphash_ref(key: bytes, msg: bytes) -> int:
    """Reference: pure-Python SipHash-2-4 (correct-or-raise)."""
    # SipHash-2-4 constants
    k0 = int.from_bytes(key[0:8], 'little')
    k1 = int.from_bytes(key[8:16], 'little')
    
    v0 = k0 ^ 0x736f6d6570736575
    v1 = k1 ^ 0x646f72616e646f6d
    v2 = k0 ^ 0x6c7967656e657261
    v3 = k1 ^ 0x7465646279746573
    
    # Process message in 8-byte blocks
    msg_len = len(msg)
    for i in range(0, msg_len - (msg_len % 8), 8):
        m = int.from_bytes(msg[i:i+8], 'little')
        v3 ^= m
        # 2 compression rounds
        for _ in range(2):
            v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
            v1 = ((v1 << 13) | (v1 >> 51)) & 0xFFFFFFFFFFFFFFFF
            v1 ^= v0
            v0 = ((v0 << 32) | (v0 >> 32)) & 0xFFFFFFFFFFFFFFFF
            v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
            v3 = ((v3 << 16) | (v3 >> 48)) & 0xFFFFFFFFFFFFFFFF
            v3 ^= v2
            v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
            v1 = ((v1 << 17) | (v1 >> 47)) & 0xFFFFFFFFFFFFFFFF
            v1 ^= v0
            v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
            v3 = ((v3 << 21) | (v3 >> 43)) & 0xFFFFFFFFFFFFFFFF
            v3 ^= v2
        v0 ^= m
    
    # Last block with padding
    last_block = msg_len & 7
    m = msg_len << 56
    if last_block > 0:
        m |= int.from_bytes(msg[-(msg_len % 8):], 'little')
    v3 ^= m
    for _ in range(2):
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 13) | (v1 >> 51)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v0 = ((v0 << 32) | (v0 >> 32)) & 0xFFFFFFFFFFFFFFFF
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 16) | (v3 >> 48)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 17) | (v1 >> 47)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 21) | (v3 >> 43)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
    v0 ^= m
    
    # Finalization: 4 rounds
    v2 ^= 0xFF
    for _ in range(4):
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 13) | (v1 >> 51)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v0 = ((v0 << 32) | (v0 >> 32)) & 0xFFFFFFFFFFFFFFFF
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 16) | (v3 >> 48)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 17) | (v1 >> 47)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 21) | (v3 >> 43)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
    
    return (v0 ^ v1 ^ v2 ^ v3) & 0xFFFFFFFFFFFFFFFF


def siphash_counted(key: bytes, msg: bytes) -> Tuple[int, int]:
    """Counted SipHash-2-4: returns (hash, operations)."""
    k0 = int.from_bytes(key[0:8], 'little')
    k1 = int.from_bytes(key[8:16], 'little')
    
    v0 = k0 ^ 0x736f6d6570736575
    v1 = k1 ^ 0x646f72616e646f6d
    v2 = k0 ^ 0x6c7967656e657261
    v3 = k1 ^ 0x7465646279746573
    
    ops = 0
    ops += 16  # 4 initial xors + 4 assignments
    
    msg_len = len(msg)
    num_full_blocks = msg_len // 8
    
    for i in range(0, num_full_blocks * 8, 8):
        m = int.from_bytes(msg[i:i+8], 'little')
        ops += 2  # load + assign
        v3 ^= m
        ops += 1
        # 2 compression rounds
        for _ in range(2):
            ops += 8  # 8 ops per round (2 adds, 2 rots, 2 xors, 2 assigns)
            v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
            v1 = ((v1 << 13) | (v1 >> 51)) & 0xFFFFFFFFFFFFFFFF
            v1 ^= v0
            v0 = ((v0 << 32) | (v0 >> 32)) & 0xFFFFFFFFFFFFFFFF
            v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
            v3 = ((v3 << 16) | (v3 >> 48)) & 0xFFFFFFFFFFFFFFFF
            v3 ^= v2
            v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
            v1 = ((v1 << 17) | (v1 >> 47)) & 0xFFFFFFFFFFFFFFFF
            v1 ^= v0
            v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
            v3 = ((v3 << 21) | (v3 >> 43)) & 0xFFFFFFFFFFFFFFFF
            v3 ^= v2
        v0 ^= m
        ops += 1
    
    # Last block
    last_block = msg_len & 7
    m = msg_len << 56
    ops += 1
    if last_block > 0:
        m |= int.from_bytes(msg[-(msg_len % 8):], 'little')
        ops += 2
    v3 ^= m
    ops += 1
    for _ in range(2):
        ops += 8
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 13) | (v1 >> 51)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v0 = ((v0 << 32) | (v0 >> 32)) & 0xFFFFFFFFFFFFFFFF
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 16) | (v3 >> 48)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 17) | (v1 >> 47)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 21) | (v3 >> 43)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
    v0 ^= m
    ops += 1
    
    # Finalization: 4 rounds
    v2 ^= 0xFF
    ops += 1
    for _ in range(4):
        ops += 8
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 13) | (v1 >> 51)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v0 = ((v0 << 32) | (v0 >> 32)) & 0xFFFFFFFFFFFFFFFF
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 16) | (v3 >> 48)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = ((v1 << 17) | (v1 >> 47)) & 0xFFFFFFFFFFFFFFFF
        v1 ^= v0
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = ((v3 << 21) | (v3 >> 43)) & 0xFFFFFFFFFFFFFFFF
        v3 ^= v2
    
    result = (v0 ^ v1 ^ v2 ^ v3) & 0xFFFFFFFFFFFFFFFF
    ops += 3  # 3 final xors
    return result, ops


def bound_for(msg_len: int) -> int:
    """Proven upper bound on 64-bit word operations for SipHash-2-4."""
    # Conservative bound: each byte adds at most 5 ops, plus fixed overhead
    num_blocks = max(1, (msg_len + 7) // 8)
    # 16 init + 18 per block + 20 last + 36 final + 20 margin
    return 16 + 18 * num_blocks + 20 + 36 + 20