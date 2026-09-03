import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import Packet, SolitonLattice, collision, soliton_validation

a = Packet(0, 2, 1, 1.0)
b = Packet(0, 2, -1, 1.0)
assert collision(a, b, mode="xor") is None
lattice = SolitonLattice(7)
lattice.inject((Packet(0, 1, 1, 1.0), Packet(0, 5, -1, 1.0)))
lattice.run(2)
assert lattice.tick == 2
assert len(lattice.log) == 3
metrics = soliton_validation(size=512, span=40.0, distance=0.5, steps=100)
assert metrics["relative_energy_drift"] < 1e-10
assert metrics["relative_power_error"] < 1e-3
print("routing validation passed")
print(metrics)
