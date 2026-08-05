import math
import random
import cirq

def grover_search(n_items,targetIndex):
    n_items=len(numbers)
    n_qubits=max(1,math.ceil(math.log2(n_items)))
    n_states=2**n_qubits

    iterations=max(1,int(math.floor((math.pi/4)*math.sqrt(n_states))))
    bitstr = format(targetIndex, f'0{n_qubits}b')

    circuit=cirq.Circuit()
    qubits=[cirq.LineQubit(qubit) for qubit in range(n_qubits)]

    circuit.append(cirq.H.on_each(qubits))


    for _ in range(iterations):
        for index,bit in enumerate(bitstr):
            if bit=='0':
                circuit.append(cirq.X(qubits[index]))
        if n_qubits==1:
            circuit.append(cirq.Z(qubits[0]))
        else:
            circuit.append(cirq.Z(qubits[-1]).controlled_by(*qubits[:-1]))

        for index,bit in enumerate(bitstr):
            if bit=='0':
                circuit.append(cirq.X(qubits[index]))

        circuit.append(cirq.H.on_each(qubits))
        circuit.append(cirq.X.on_each(qubits))

        if n_qubits==1:
            circuit.append(cirq.Z(qubits[0]))
        else:
            circuit.append(cirq.Z(qubits[-1]).controlled_by(*qubits[:-1]))

        circuit.append(cirq.X.on_each(qubits))
        circuit.append(cirq.H.on_each(qubits))

    circuit.append(cirq.measure(qubits,key='result'))

    return circuit,iterations,n_states

randomSize=random.randint(20,500)
numbers=random.sample(range(1,501),randomSize)
targetIndex=random.randint(0,randomSize-1)

circuit,iterations,n_states=grover_search(len(numbers),targetIndex)
print(circuit)

simulator=cirq.Simulator()
result=simulator.run(circuit,repetitions=4096)

histogram=result.histogram(key='result')
foundIndex=max(histogram,key=histogram.get)

print("Numbers:- ",numbers)
print("Size:- ",randomSize)
print("Target Number:- ",numbers[targetIndex])
print("Found Number:- ",numbers[foundIndex])
print("Hits / Shots:- ", histogram[foundIndex] / 4096)
print("Iterations:- ",iterations)
print("Classical Lookups:- ",n_states)


