import numpy as np
import qiskit

import bluequbit


def test_job_estimation():
    dq_client = bluequbit.BQClient()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    results = dq_client.estimate(qc_qiskit)
    assert results.estimated_runtime == 100


def test_job_estimation_large():
    dq_client = bluequbit.BQClient()
    qc = qiskit.QuantumCircuit(24)
    qc.x(np.arange(24))
    results = dq_client.estimate(qc)
    assert results.estimated_runtime == 187
    # assert results.device == "qsim_simulator"
    assert results.num_qubits == 24
    assert (
        results.warning_message
        == "This is just an estimate; the actual runtime may be less or more."
    )


def test_job_estimate_validation_too_many_qubits():
    # Too many qubits
    dq_client = bluequbit.BQClient()
    qc = qiskit.QuantumCircuit(38)
    qc.x(np.arange(38))
    result = dq_client.estimate(qc)
    expected_message = "Circuit contains more than 34 qubits, which is not supported for CPU backend. See deqart.com/docs#supported-circuits for more details."
    assert expected_message in result.error_message

    result = dq_client.run(qc)
    print(result)
    assert expected_message in result.error_message
