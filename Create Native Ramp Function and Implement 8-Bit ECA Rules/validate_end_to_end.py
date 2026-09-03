import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import CalibratedSolitonNetwork, Perturbation

# Positive-domain task avoids conflating this stage with signed output coding.
network = CalibratedSolitonNetwork(
    weights=(((0.5, 0.25), (0.25, 0.5)), ((0.5, 0.5),)),
    biases=((0.1, 0.1), (0.0,)),
)
assert network.forward((1.0, 0.0)) == network.forward((1.0, 0.0))
assert len(network.forward((1.0, 0.0))) == 1
samples = [((1.0, 0.0), (0.75,)), ((0.0, 1.0), (0.75,)),
           ((1.0, 1.0), (1.0,)), ((0.0, 0.0), (0.0,))]
losses = network.train_robust(samples, epochs=8, learning_rate=0.03,
                              impairment=Perturbation(gain_error=0.05))
assert losses[-1] < losses[0]
print('end-to-end validation passed')
print('losses:', losses)
