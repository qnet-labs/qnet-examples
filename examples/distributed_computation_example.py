"""Distributed quantum computing example.

Demonstrates multi-party computation with coordinated measurements using
both the engine's simplified API and full parameters object.

Prerequisites: build the Python bindings first —
    pip install maturin
    cd python && maturin develop --release
"""

from qnet_core import (
    QNetEngine,
    NodeDefinition,
    LinkDefinition,
    DistributedComputingParameters,
    CoordinationTopology,
    MeasurementBasis,
    BasisType,
    distributed_computation as dc_fn,
)


def build_mesh_network() -> QNetEngine:
    """Build a 3-node fully-connected mesh network."""
    engine = QNetEngine()

    nodes = [
        NodeDefinition(id="A", memory_lifetime_t2=1.0),
        NodeDefinition(id="B", memory_lifetime_t2=1.0),
        NodeDefinition(id="C", memory_lifetime_t2=1.0),
    ]

    links = [
        LinkDefinition(from_node="A", to="B", distance_km=10.0, base_fidelity=0.95, generation_rate_hz=1000.0),
        LinkDefinition(from_node="B", to="C", distance_km=10.0, base_fidelity=0.93, generation_rate_hz=900.0),
        LinkDefinition(from_node="A", to="C", distance_km=20.0, base_fidelity=0.90, generation_rate_hz=750.0),
    ]

    engine.define_network(nodes=nodes, links=links)
    return engine


engine = build_mesh_network()

# ------------------------------------------------------------------
# Method 1 — Engine.run_distributed_computation() simplified API
# ------------------------------------------------------------------

result = engine.run_distributed_computation(
    participants=["A", "B", "C"],
    coordination_topology="star",       # string shortcut
    basis_type="ghz",                    # "ghz" | "cluster" | "graph"
    correlation_strength=0.85,
    classical_relay_latency_ms=5.0,
)

print(f"--- Distributed computation via engine.run_distributed_computation() (simplified) ---")
print(f"Success:             {result.success}")
print(f"Fidelity:            {result.computation_fidelity:.4f}")
print(f"Total latency:       {result.total_latency_ms:.1f} ms")
print(f"Coordination overhead:{result.coordination_overhead_ms:.1f} ms")
print(f"Resource links:      {result.resource_links_used}")
for party in result.party_results:  # List[PartyOutcome]
    print(f"  {party.node_id}: success={party.successful_measurement}, fidelity={party.local_fidelity:.4f}")


# ------------------------------------------------------------------
# Method 2 — Full DistributedComputingParameters object
# ------------------------------------------------------------------

topology = CoordinationTopology.star("A")       # or .ring(), .mesh(), .arbitrary(edges)
basis = MeasurementBasis(
    basis_type=BasisType.GHZ,                   # GHZ | Cluster | GraphGraph
    correlation_strength=0.85,
)

params = DistributedComputingParameters(
    participants=["A", "B", "C"],
    coordination_topology=topology,
    measurement_basis=basis,
    classical_relay_latency_ms=5.0,
)

result2 = engine.run_distributed_computation(params=params)

print(f"\n--- Distributed computation via full parameters object ---")
print(f"Fidelity:            {result2.computation_fidelity:.4f}")
for party in result2.party_results:
    print(f"  {party.node_id}: success={party.successful_measurement}, fidelity={party.local_fidelity:.4f}")


# ------------------------------------------------------------------
# Method 3 — Module-level convenience function
# ------------------------------------------------------------------

dc_result = dc_fn(
    engine,
    participants=["A", "B", "C"],
    coordination_topology=CoordinationTopology.mesh(),
    measurement_basis=MeasurementBasis(basis_type=BasisType.Cluster, correlation_strength=0.80),
    classical_relay_latency_ms=10.0,
)

print(f"\n--- Distributed computation via distributed_computation() convenience function ---")
print(f"Fidelity:            {dc_result.computation_fidelity:.4f}")
for party in dc_result.party_results:
    print(f"  {party.node_id}: success={party.successful_measurement}, fidelity={party.local_fidelity:.4f}")
