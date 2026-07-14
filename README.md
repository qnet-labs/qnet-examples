# qnet-examples

Python examples for **qnet_core** — a quantum network simulator.

Run these scripts to explore entanglement distribution across different topologies, routing strategies, and physical constraints. No build step required.

## Installation

```bash
pip install qnet-core
```

Then run any example with `python examples/<script>.py`.

## Examples

| # | Script | Description |
|---|--------|-------------|
| 1 | `examples/1_basic_simuation.py` | Routing trade-offs: latency vs. fidelity on a 2-hop repeater chain |
| 2 | `examples/2_basic_simulation.py` | Physical constraint boundaries (decoherence, latency limits) |
| 3 | `examples/3_test_latency_optimized_routing.py` | Lowest-latency routing across multi-hop paths |
| 4 | `examples/4_test_highest_fidelity_routing.py` | Highest-fidelity routing with purification cycles |
| 5 | `examples/5_test_physical_constraints_failure.py` | Requests that fail due to physical limits |
| 6 | `examples/6_test_sensitivity_analysis.py` | Parameter sensitivity analysis (which factors most impact success?) |
| 7 | `examples/7_custom_simulation_config.py` | Custom simulation configuration |
| 8 | `examples/8_topology_generation.py` | Pre-built topologies: satellite-fiber, telecom backbone, repeater chain |
| 9 | `examples/9_qnet_file_load.py` | Load `.qnet` JSON topology files directly |
| 10 | `examples/10_qnet_programmatic.py` | Build `.qnet` files programmatically, save, reload, simulate |
| 11 | `examples/11_strategy_battle.py` | Strategy comparison exercise |
| 12 | `examples/12_mesh_network.py` | Multi-path routing on a mesh topology; Monte Carlo across strategies |
| 13 | `examples/13_seed_determinism.py` | Seed-based reproducibility for fair config comparison |
| 14 | `examples/14_link_utilization.py` | Link utilization analysis |

Run any example:

```bash
python examples/8_topology_generation.py
```

## Running tests

```bash
python test_example.py
```

## Core API

### Quick start — single simulation request

```python
from qnet_core import QNetEngine, NodeDefinition, LinkDefinition, StrategyType

engine = QNetEngine()

nodes = [
    NodeDefinition(id="Alice", memory_lifetime_t2=150.0),
    NodeDefinition(id="Repeater_1", memory_lifetime_t2=150.0),
    NodeDefinition(id="Bob", memory_lifetime_t2=150.0),
]

links = [
    LinkDefinition(from_node="Alice", to="Repeater_1", distance_km=25.0, base_fidelity=0.88, generation_rate_hz=1000.0),
    LinkDefinition(from_node="Repeater_1", to="Bob", distance_km=25.0, base_fidelity=0.88, generation_rate_hz=1000.0),
]

engine.define_network(nodes=nodes, links=links)

result = engine.request_entanglement(
    from_node="Alice", to="Bob",
    fidelity_target=0.70,
    max_latency_ms=50.0,
    strategy=StrategyType.LowestLatency,
)

print(result.success, result.latency_ms, result.final_fidelity, result.execution_path)
```

### Monte Carlo ensemble

```python
stats = engine.simulate(
    from_node="Alice", to="Bob",
    fidelity_target=0.75, max_latency_ms=5000.0,
    runs=100, seed=42,
)

print(stats.empirical_success_rate)   # e.g. 0.87
print(stats.mean_latency_ms)           # mean latency across runs
print(stats.mean_fidelity)             # mean fidelity across runs
print(stats.link_utilization_heatmap)  # per-link usage data
```

### Load a `.qnet` topology file

```python
from qnet_core import from_qnet_file

engine = from_qnet_file("toronto_london.qnet")
stats = engine.simulate(from_node="Toronto", to="London", fidelity_target=0.75, runs=100)
```

### Build a `.qnet` file programmatically

```python
from qnet_core import PyQNetFile

f = PyQNetFile("my_network")
f.add_node("hub", memory_lifetime_ms=200.0, node_type="ground")
f.add_node("edge", memory_lifetime_ms=150.0, node_type="ground")
f.add_link("", "hub", "edge", distance_km=50.0, base_fidelity=0.92, generation_rate_hz=1000.0)
f.save("my_network.qnet")
```

## Strategy types

| Strategy | Use when... |
|----------|-------------|
| `LowestLatency` | You need the fastest result |
| `HighestFidelity` | Quality matters; purification is worth the extra time |
| `HighestSuccess` | Reliability is the priority |

## Pre-built topologies

```python
from qnet_core import generate_topology, compare_topologies

# Generate a topology
net = generate_topology("hybrid_satellite_fiber")  # or "telecom_backbone", "repeater_chain"

# Compare two topologies at given endpoints
report = compare_topologies(
    endpoints=[
        TopologyEndpoints("telecom_backbone", "A", "C"),
        TopologyEndpoints("hybrid_satellite_fiber", "Toronto", "London"),
    ],
    fidelity_target=0.75, max_latency_ms=5000.0, runs=100,
)

print(report.recommended_topology)
```

## Fixture files

These `.qnet` JSON files in the repo root are topology definitions you can load:

- `network_v1.qnet` — 2-node chain (A → B)
- `network_v2.qnet` — 3-node chain (A → B → C)
- `toronto_london.qnet` — 4-node hybrid satellite-fiber network
- `valid_network.qnet` / `invalid_network.qnet` — validation test fixtures

## Notebooks

Jupyter notebooks in `notebooks/`:

- `01_gothamq_validation.ipynb` — GothamQ validation workflows
- `02_sensitivity_analysis.ipynb` — Parameter sensitivity studies
- `03_topology_comparison.ipynb` — Fiber vs. satellite-fiber comparison
