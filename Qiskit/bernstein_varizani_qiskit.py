from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def bernstein_varizani(secret_string):
    n=len(secret_string)
    qc=QuantumCircuit(n+1,n)

    for qubit in range(n):
        qc.h(qubit)

    qc.x(n)
    qc.h(n)
    qc.barrier()

    for i, bit in enumerate(reversed(secret_string)):
        if bit=='1':
            qc.cx(i,n)

    qc.barrier()

    for qubit in range(n):
        qc.h(qubit)

    qc.measure(range(n),range(n))
    return qc

secret_number=int(input())
circuit=bernstein_varizani(format(secret_number,'b'))
print(circuit.draw())

simulator=AerSimulator()
counts=simulator.run(circuit,shots=1).result().get_counts()
measured_string=list(counts.keys())[0]

print("Secret Number:- ",secret_number)
print("Measured Number:-", int(measured_string,2))

    