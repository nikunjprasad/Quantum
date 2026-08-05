import math
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def grover_search(n_items,targetIndex):
    n_items=len(numbers)
    n_qubits=max(1,math.ceil(math.log2(n_items)))
    n_states=2**n_qubits

    iterations=max(1,int(math.floor((math.pi/4)*math.sqrt(n_states))))
    bitstr = format(targetIndex, f'0{n_qubits}b')

    qc=QuantumCircuit(n_qubits,n_qubits)
    qc.h(range(n_qubits))

    for _ in range(iterations):
        for index,bit in enumerate(reversed(bitstr)):
            if bit=='0':
                qc.x(index)
        if n_qubits==1:
            qc.z(0)
        else:
            qc.h(n_qubits-1)
            qc.mcx(list(range(n_qubits-1)),n_qubits-1)
            qc.h(n_qubits-1)

        for index,bit in enumerate(reversed(bitstr)):
            if bit=='0':
                qc.x(index)

        qc.h(range(n_qubits))
        qc.x(range(n_qubits))

        if n_qubits==1:
            qc.z(0)
        else:
            qc.h(n_qubits-1)
            qc.mcx(list(range(n_qubits-1)),n_qubits-1)
            qc.h(n_qubits-1)

        qc.x(range(n_qubits))
        qc.h(range(n_qubits))

    qc.measure(range(n_qubits),range(n_qubits))

    return qc,iterations,n_states

randomSize=random.randint(20,500)
numbers=random.sample(range(1,501),randomSize)
targetIndex=random.randint(0,randomSize-1)

circuit,iterations,n_states=grover_search(len(numbers),targetIndex)
print(circuit.draw())

simulator=AerSimulator()
counts=simulator.run(circuit,shots=4096).result().get_counts()

most_frequent_bitstr=max(counts,key=counts.get)
foundIndex=int(most_frequent_bitstr,2)

print("Numbers:- ",numbers)
print("Size:- ",randomSize)
print("Target Number:- ",numbers[targetIndex])
print("Found Number:- ",numbers[foundIndex])
print("Hits / Shots:- ", counts[most_frequent_bitstr] / 4096)
print("Iterations:- ",iterations)
print("Classical Lookups:- ",n_states)


