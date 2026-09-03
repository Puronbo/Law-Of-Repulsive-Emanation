from .soliton_eca import (
    RULES,
    EcaCell,
    Soliton,
    SolitonBus,
    SolitonECA,
    evolve,
    negative_ramp,
    ramp,
)
from .soliton_nn import NeuralSoliton, SolitonNeuralNetwork, SolitonNeuron, WeightedSolitonBus
from .soliton_protocol import Packet, SolitonLattice, collision, reversible_pair
from .soliton_wire import (
    SolitonWireClient, SolitonWireServer, WireError, WireRequest, WireResponse,
    decode_response, encode_envelope, request_from_spikes, wire_frame,
)
from .soliton_physics import Fiber, energy, fundamental_soliton, propagate, soliton_validation
from .soliton_mixing import (
    ActivationCalibration, CalibratedMixer, DifferentialEncoder,
    DifferentialSoliton, ramp_activation, sigmoid_activation, transfer_curve,
)
from .soliton_hardware import (
    CalibratedSolitonLayer, Perturbation, perturb, perturbation_report, relative_error,
)
from .soliton_calibration import (
    CalibrationReport, fit_affine_calibration, robustness_summary, robust_train,
)
from .soliton_end_to_end import CalibratedSolitonNetwork
from .soliton_benchmark import (
    CurveDiagnostics, benchmark_summary, calibrate_csv, diagnose_curve,
    impairment_sweep, load_transfer_csv,
)
from .soliton_quality import QualityGate, QualityResult, evaluate_quality, quality_report, require_quality
from .soliton_replicates import (
    ReplicatePoint, ReplicateReport, aggregate_replicates, calibrate_replicates,
    replicate_report,
)
from .soliton_drift import DriftDiagnostics, drift_passes, estimate_drift
from .soliton_uncertainty import (
    UncertaintyReport, estimate_uncertainty, require_uncertainty, uncertainty_passes,
)
from .soliton_holdout import (
    HoldoutPoint, HoldoutReport, holdout_passes, holdout_report,
    leave_one_input_out, require_holdout,
)
from .soliton_coverage import CoverageReport, evaluate_coverage, require_coverage
from .soliton_snn import (
    AERSpike, Connection, LIFNeuron, SolitonSNN, decode_spike,
    decode_spike_stream, encode_spike, encode_spike_stream, temporal_xor_spikes,
    trace_digest,
)
from .soliton_framing import AERFrame, decode_frames, encode_frames
from .soliton_admission import AdmissionPolicy, admit_spikes
from .cognitive_agent import Action, CognitiveAgent, CognitiveEvent, Episode, Fact, Goal, Observation
from .language_grounding import apply_command, parse_command
from .episodic_store import EpisodicStore, MemoryRecord
from .soliton_metrics import SNNMetrics, metrics, validate_spike_trace
from .runtime import SolitonCognitiveRuntime
from .simulated_body import ActuatorEvent, BodyState, SimulatedBody

__all__ = [
    "RULES", "EcaCell", "Soliton", "SolitonBus", "SolitonECA",
    "evolve", "negative_ramp", "ramp",
    "NeuralSoliton", "SolitonNeuralNetwork", "SolitonNeuron", "WeightedSolitonBus",
    "Packet", "SolitonLattice", "collision", "reversible_pair",
    "Fiber", "energy", "fundamental_soliton", "propagate", "soliton_validation",
    "ActivationCalibration", "CalibratedMixer", "DifferentialEncoder",
    "DifferentialSoliton", "ramp_activation", "sigmoid_activation", "transfer_curve",
    "CalibratedSolitonLayer", "Perturbation", "perturb", "perturbation_report", "relative_error",
    "CalibrationReport", "fit_affine_calibration", "robustness_summary", "robust_train",
    "CalibratedSolitonNetwork",
    "CurveDiagnostics", "benchmark_summary", "calibrate_csv", "diagnose_curve",
    "impairment_sweep", "load_transfer_csv",
    "QualityGate", "QualityResult", "evaluate_quality", "quality_report", "require_quality",
    "ReplicatePoint", "ReplicateReport", "aggregate_replicates", "calibrate_replicates", "replicate_report",
    "DriftDiagnostics", "drift_passes", "estimate_drift",
    "UncertaintyReport", "estimate_uncertainty", "require_uncertainty", "uncertainty_passes",
    "HoldoutPoint", "HoldoutReport", "holdout_passes", "holdout_report",
    "leave_one_input_out", "require_holdout",
    "CoverageReport", "evaluate_coverage", "require_coverage",
    "AERSpike", "Connection", "LIFNeuron", "SolitonSNN", "decode_spike",
    "decode_spike_stream", "encode_spike", "encode_spike_stream", "temporal_xor_spikes",
    "trace_digest",
    "AERFrame", "decode_frames", "encode_frames",
    "AdmissionPolicy", "admit_spikes",
    "Action", "CognitiveAgent", "CognitiveEvent", "Episode", "Fact", "Goal", "Observation",
    "apply_command", "parse_command", "EpisodicStore", "MemoryRecord",
    "SNNMetrics", "metrics", "validate_spike_trace",
    "SolitonCognitiveRuntime",
    "ActuatorEvent", "BodyState", "SimulatedBody",
]
