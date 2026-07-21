"""Quantum state teleportation example.

Demonstrates entanglement-based teleportation across a multi-hop network
using both the engine method and the module-level convenience function.

Prerequisites: build the Python bindings first —
    pip install maturin
    cd python && maturin develop --release
"""

from qnet_core import (
    QNetEngine,
    NodeDefinition,
    LinkDefinition,
    TeleportationParameters,
    teleportation as tp_fn,
)


def build_chain_network() -> QNetEngine:
    """Build a 4-node linear repeater chain A-B-C-D."""
    engine = QNetEngine()

    nodes = [
        NodeDefinition(id="A", memory_lifetime_t2=1.0),
        NodeDefinition(id="B", memory_lifetime_t2=1.0),
        NodeDefinition(id="C", memory_lifetime_t2=1.0),
        NodeDefinition(id="D", memory_lifetime_t2=1.0),
    ]

    links = [
        LinkDefinition(from_node="A", to="B", distance_km=10.0, base_fidelity=0.95, generation_rate_hz=1000.0),
        LinkDefinition(from_node="B", to="C", distance_km=20.0, base_fidelity=0.90, generation_rate_hz=700.0),
        LinkDefinition(from_node="C", to="D", distance_km=15.0, base_fidelity=0.92, generation_rate_hz=850.0),
    ]

    engine.define_network(nodes=nodes, links=links)
    return engine


# ------------------------------------------------------------------
# Method 1 — Engine.execute_teleportation() with a parameters object
# ------------------------------------------------------------------

engine = build_chain_network()

params = TeleportationParameters(
    source_node="A",
    target_node="D",
    state_fidelity=0.95,
    classical_bandwidth_ms=100.0,
)
params.relay_nodes = ["B", "C"]  # intermediaries via automatic entanglement swapping

outcome = engine.execute_teleportation(params=params)

print(f"--- Teleportation via engine.execute_teleportation() ---")
print(f"Success:                       {outcome.success}")
print(f"Teleportation fidelity:        {outcome.teleportation_fidelity:.4f}")
print(f"Resource entanglement fidelity:{outcome.resource_entanglement_fidelity:.4f}")
print(f"Latency:                       {outcome.latency_ms:.1f} ms")
print(f"Path:                          {' -> '.join(outcome.path)}")
print(f"Classical bits transferred:    {outcome.classical_bits_transferred}")


# ------------------------------------------------------------------
# Method 2 — Module-level convenience function (no relay setup needed)
# ------------------------------------------------------------------

tp_result = tp_fn(
    engine,
    source_node="A",
    target_node="D",
    state_fidelity=0.95,
    classical_bandwidth_ms=100.0,
)

print(f"\n--- Teleportation via teleportation() convenience function ---")
print(f"Teleportation fidelity:        {tp_result.teleportation_fidelity:.4f}")
print(f"Latency:                       {tp_result.latency_ms:.1f} ms")
