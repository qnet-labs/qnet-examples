"""BB84-style quantum key distribution example.

Demonstrates running QKD between two nodes using both the engine method
and the module-level convenience function.

Prerequisites: build the Python bindings first —
    pip install maturin
    cd python && maturin develop --release
"""

from qnet_core import (
    QNetEngine,
    NodeDefinition,
    LinkDefinition,
    QKDParameters,
    qkd as qkd_fn,
)


def build_sample_network() -> QNetEngine:
    """Build a 4-node ring network for the example."""
    engine = QNetEngine()

    nodes = [
        NodeDefinition(id="A", memory_lifetime_t2=1.0),
        NodeDefinition(id="B", memory_lifetime_t2=1.0),
        NodeDefinition(id="C", memory_lifetime_t2=1.0),
        NodeDefinition(id="D", memory_lifetime_t2=1.0),
    ]

    links = [
        LinkDefinition(from_node="A", to="B", distance_km=10.0, base_fidelity=0.95, generation_rate_hz=1000.0),
        LinkDefinition(from_node="B", to="C", distance_km=15.0, base_fidelity=0.92, generation_rate_hz=800.0),
        LinkDefinition(from_node="C", to="D", distance_km=10.0, base_fidelity=0.93, generation_rate_hz=900.0),
    ]

    engine.define_network(nodes=nodes, links=links)
    return engine


# ------------------------------------------------------------------
# Method 1 — Engine.run_qkd() with a full parameters object
# ------------------------------------------------------------------

engine = build_sample_network()

params = QKDParameters(
    from_node="A",
    to_node="D",
    fidelity_target=0.9,
    max_latency_ms=5000.0,
    rounds=100,
    error_rate_tolerance=0.11,
    sifting_overhead_ratio=0.5,
    privacy_amplification_factor=0.8,
)

result = engine.run_qkd(params=params)

print(f"--- QKD via engine.run_qkd() ---")
print(f"Success:            {result.success}")
print(f"Key length:         {result.secret_key_length_bits} bits")
print(f"Efficiency:         {result.efficiency_rate:.2%}")
print(f"QBER:               {result.qber:.4f}")
print(f"Latency:            {result.latency_ms:.1f} ms")
print(f"Execution path:     {' -> '.join(result.execution_path)}")
print(f"Rounds completed:   {result.rounds_completed}")
print(f"Rounds failed:      {result.rounds_failed}")


# ------------------------------------------------------------------
# Method 2 — Module-level convenience function
# ------------------------------------------------------------------

qkd_result = qkd_fn(
    engine,
    from_node="A",
    to_node="D",
    fidelity_target=0.9,
    max_latency_ms=5000.0,
    rounds=100,
    error_rate_tolerance=0.11,
)

print(f"\n--- QKD via qkd() convenience function ---")
print(f"Success:            {qkd_result.success}")
print(f"Key length:         {qkd_result.secret_key_length_bits} bits")
print(f"Efficiency:         {qkd_result.efficiency_rate:.2%}")
