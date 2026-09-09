"""
QuPCG: Quantum Convolutional Neural Network for Detecting Abnormal Patterns in PCG Signals

QuPCG is a hybrid quantum-classical convolutional neural network designed for
detecting abnormal patterns in phonocardiogram (PCG) signals. The approach
uses compact feature representations of PCG signals and processes them with
a quantum convolutional neural network using 8 qubits.

The QCNN consists of quantum convolution and pooling operations that
progressively reduce the active qubits, followed by a final quantum
measurement for classification.

Reference:
Torabi, Y., Shirani, S., & Reilly, J. P. (2025).
QuPCG: Quantum Convolutional Neural Network for Detecting Abnormal
Patterns in PCG Signals. ArXiv.
https://arxiv.org/abs/2511.02140
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector


N_QUBITS = 8
SEED = 42
rng = np.random.default_rng(SEED)


def encode_features(features):
    """Encode an 8-value feature vector into an 8-qubit circuit."""
    features = np.asarray(features, dtype=float)

    if features.shape != (N_QUBITS,):
        raise ValueError(f"Expected {N_QUBITS} input features.")

    features = np.pi * np.tanh(features)

    qc = QuantumCircuit(N_QUBITS)

    for q, value in enumerate(features):
        qc.h(q)
        qc.rz(value, q)

    return qc


def convolution_block(qc, qubits, weights):
    """Apply a quantum convolution block to neighboring qubits."""
    for i in range(0, len(qubits) - 1, 2):
        q1, q2 = qubits[i], qubits[i + 1]

        qc.cx(q1, q2)
        qc.ry(weights[i % len(weights)], q1)
        qc.rz(weights[(i + 1) % len(weights)], q2)
        qc.cx(q2, q1)

    for i in range(1, len(qubits) - 1, 2):
        q1, q2 = qubits[i], qubits[i + 1]

        qc.cx(q1, q2)
        qc.ry(weights[(i + 2) % len(weights)], q2)
        qc.cx(q2, q1)


def pooling_block(qc, active_qubits, weights):
    """Apply a quantum pooling operation and retain one qubit per pair."""
    if len(active_qubits) < 2:
        return active_qubits

    retained = []

    for i in range(0, len(active_qubits), 2):
        if i + 1 >= len(active_qubits):
            retained.append(active_qubits[i])
            continue

        source = active_qubits[i]
        target = active_qubits[i + 1]

        qc.cx(source, target)
        qc.ry(weights[i % len(weights)], target)
        qc.rz(weights[(i + 1) % len(weights)], target)

        retained.append(target)

    return retained


def build_qcnn():
    """Construct the QuPCG quantum convolutional neural network."""
    qc = QuantumCircuit(N_QUBITS)
    active = list(range(N_QUBITS))

    weights = rng.normal(0.0, 0.25, size=6)

    convolution_block(qc, active, weights)
    active = pooling_block(qc, active, weights)

    convolution_block(qc, active, weights)
    active = pooling_block(qc, active, weights)

    convolution_block(qc, active, weights)
    active = pooling_block(qc, active, weights)

    return qc, active[0]


def predict(features):
    """Process one 8-feature input and return its quantum prediction."""
    encoding = encode_features(features)
    qcnn, output_qubit = build_qcnn()

    circuit = encoding.compose(qcnn)

    state = Statevector.from_instruction(circuit)

    pauli = ["I"] * N_QUBITS
    pauli[N_QUBITS - 1 - output_qubit] = "Z"

    observable = SparsePauliOp("".join(pauli))

    expectation = float(
        np.real(state.expectation_value(observable))
    )

    label = 1 if expectation >= 0 else -1

    return expectation, label


if __name__ == "__main__":
    sample = np.array([
        0.20, -0.10, 0.75, 0.30,
        -0.45, 0.15, 0.60, -0.20
    ])

    expectation, prediction = predict(sample)

    print("QuPCG")
    print("-----")
    print(f"Input features : {sample}")
    print(f"<Z> expectation: {expectation:.4f}")
    print(f"Prediction      : {prediction:+d}")


# Citation:
# Torabi, Y., Shirani, S., & Reilly, J. P. (2025).
# QuPCG: Quantum Convolutional Neural Network for Detecting Abnormal
# Patterns in PCG Signals. ArXiv.
# https://arxiv.org/abs/2511.02140
