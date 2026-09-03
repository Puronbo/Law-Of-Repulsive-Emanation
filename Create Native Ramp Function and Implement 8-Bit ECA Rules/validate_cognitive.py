import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import Action, CognitiveAgent, Fact, Goal, Observation

at_a = Fact('location', 'A')
at_b = Fact('location', 'B')
ready = Fact('state', 'ready')
move = Action('move-A-B', frozenset({at_a}), frozenset({at_b}), frozenset({at_a}))
prepare = Action('prepare', frozenset({at_b}), frozenset({ready}))
agent = CognitiveAgent((move, prepare), plan_horizon=3, salience_threshold=0.5)
agent.remember((at_a,))
agent.set_goal(Goal('ready-at-B', frozenset({at_b, ready})))
selected, plan = agent.observe(Observation(0, frozenset({at_a}), salience=1.0))
assert selected == move
assert [action.name for action in plan] == ['move-A-B', 'prepare']
assert at_b in agent.facts and at_a not in agent.facts
selected, plan = agent.observe(Observation(1, frozenset({at_b}), salience=0.0))
assert selected == prepare
assert ready in agent.facts
assert agent.episodes[0].salience_spikes == 1
assert agent.episodes[1].salience_spikes == 0

# Cost, not merely step count, determines the selected plan.
mid = Fact('location', 'M')
cheap_first = Action('cheap-A-M', frozenset({at_a}), frozenset({mid}), frozenset({at_a}), cost=1.0)
cheap_finish = Action('cheap-M-B', frozenset({mid}), frozenset({at_b}), frozenset({mid}), cost=1.0)
expensive_direct = Action('expensive-A-B', frozenset({at_a}), frozenset({at_b}), frozenset({at_a}), cost=5.0)
cost_agent = CognitiveAgent((expensive_direct, cheap_first, cheap_finish), plan_horizon=3)
cost_agent.remember((at_a,))
cost_agent.set_goal(Goal('cheap-B', frozenset({at_b})))
cost_plan = cost_agent.plan()
assert cost_plan is not None
assert [action.name for action in cost_plan] == ['cheap-A-M', 'cheap-M-B']

# Equal-cost alternatives resolve in declared action order.
alt1 = Action('route-1', frozenset({at_a}), frozenset({at_b}), frozenset({at_a}), cost=1.0)
alt2 = Action('route-2', frozenset({at_a}), frozenset({at_b}), frozenset({at_a}), cost=1.0)
tie_agent = CognitiveAgent((alt1, alt2), plan_horizon=1)
tie_agent.remember((at_a,))
tie_agent.set_goal(Goal('tie', frozenset({at_b})))
assert tie_agent.plan()[0].name == 'route-1'

# No applicable action returns an auditable no-op, not an invented action.
blocked = CognitiveAgent((prepare,), plan_horizon=2)
blocked.set_goal(Goal('unreachable', frozenset({at_b})))
selected, plan = blocked.observe(Observation(0, frozenset()))
assert selected is None and plan is None
assert blocked.episodes[-1].plan_length == -1

# Traces are deterministic for identical state and observations.
def make_agent():
    a = CognitiveAgent((move, prepare), plan_horizon=3)
    a.remember((at_a,))
    a.set_goal(Goal('ready-at-B', frozenset({at_b, ready})))
    a.observe(Observation(0, frozenset({at_a}), 1.0))
    a.observe(Observation(1, frozenset({at_b}), 0.0))
    return a
assert make_agent().trace_digest() == make_agent().trace_digest()
print('cognitive validation passed')
print(agent.trace())
