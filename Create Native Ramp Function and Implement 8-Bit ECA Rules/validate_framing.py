import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import AERFrame, AERSpike, decode_frames, encode_frames

spikes = [AERSpike(0, 1, 2), AERSpike(2, 2, 3, -1, 0.5)]
wire = encode_frames(spikes, start_sequence=10)
assert decode_frames(wire, start_sequence=10) == spikes
frame = AERFrame.create(10, spikes[0])
assert AERFrame.decode(frame.encode()) == frame

# Corruption is detected by checksum verification.
corrupt = wire.replace('"payload":1.0', '"payload":1.1')
try:
    decode_frames(corrupt, start_sequence=10)
except ValueError as exc:
    assert 'checksum' in str(exc)
else:
    raise AssertionError('corrupted AER frame accepted')

# Reordering, duplication, and gaps are rejected by contiguous sequence checks.
lines = wire.splitlines()
for malformed in (lines[::-1], lines + [lines[0]], [lines[1]]):
    try:
        decode_frames('\n'.join(malformed), start_sequence=10)
    except ValueError as exc:
        assert 'sequence' in str(exc)
    else:
        raise AssertionError('invalid AER sequence accepted')
# Non-contiguous inspection can be explicitly requested.
assert len(decode_frames('\n'.join(lines[::-1]), start_sequence=10,
                        require_contiguous=False)) == 2
print('framing validation passed')
print(wire)
