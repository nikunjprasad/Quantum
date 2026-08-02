import cirq

def deutsch_jozsca(n,oracle_type):
    input_qubits=[cirq.LineQubit(i) for i in range(n)]
    target_qubit=cirq.LineQubit(n)

    circuit= cirq.Circuit()

    circuit.append(cirq.H.on_each(input_qubits))
    circuit.append(cirq.X(target_qubit))
    circuit.append(cirq.H(target_qubit))

    if oracle_type=="balanced":
        for q in input_qubits:
            circuit.append(cirq.CNOT(q,target_qubit))
    else:
        pass

    circuit.append(cirq.H.on_each(input_qubits))

    circuit.append(cirq.measure(input_qubits,key='result'))

    return circuit

n=int(input())
balancedCircuit=deutsch_jozsca(n,"balanced")
print("Balanced Circuit")
print(balancedCircuit)

constantCircuit=deutsch_jozsca(n,"constant")
print("Constant Circuit")
print(constantCircuit)

simulator=cirq.Simulator()
balancedResult=simulator.run(balancedCircuit,repetitions=1)
print("Balanced Function Output:- ",balancedResult.measurements['result'][0])

constantResult=simulator.run(constantCircuit,repetitions=1)
print("Constant Function Output:- ",constantResult.measurements['result'][0])