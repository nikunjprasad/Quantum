import cirq

def bernstein_varizani(secret_string):
    n=len(secret_string)
    input_qubits=[cirq.LineQubit(i) for i in range(n)]
    target_qubit=cirq.LineQubit(n)

    circuit=cirq.Circuit()

    circuit.append(cirq.H.on_each(input_qubits))
    circuit.append(cirq.X(target_qubit))
    circuit.append(cirq.H(target_qubit))

    for i, bit in enumerate(secret_string):
        if bit=='1':
            circuit.append(cirq.CNOT(input_qubits[i],target_qubit))

    circuit.append(cirq.H.on_each(input_qubits))

    circuit.append(cirq.measure(input_qubits,key='result'))

    return circuit

secret_number=int(input())
circuit=bernstein_varizani(format(secret_number,'b'))
print(circuit)

simulator=cirq.Simulator()
result=simulator.run(circuit,repetitions=1)
measurement=result.measurements['result'][0]

measured_string="".join(str(bit) for bit in measurement)
print("Secret Number:- ", secret_number)
print("Measured Number:- ",int(measured_string,2))