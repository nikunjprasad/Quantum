from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def deutsch_jozsca(n,oracle_type):
    qc=QuantumCircuit(n+1,n)
    for qubit in range(n):
        qc.h(qubit)

    qc.x(n)
    qc.h(n)
    qc.barrier()

    if oracle_type=="balanced":
        for qubit in range(n):
            qc.cx(qubit,n)
    else:
        pass

    qc.barrier()

    for qubit in range(n):
        qc.h(qubit)

    qc.measure(range(n),range(n))from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def deutsch_jozsca(n,oracle_type):
    qc=QuantumCircuit(n+1,n)
    for qubit in range(n):
        qc.h(qubit)

    qc.x(n)
    qc.h(n)
    qc.barrier()

    if oracle_type=="balanced":
        for qubit in range(n):
            qc.cx(qubit,n)
    else:
        pass

    qc.barrier()

    for qubit in range(n):
        qc.h(qubit)

    qc.measure(range(n),range(n))
    return qc

n=int(input())
balancedCircuit=deutsch_jozsca(n,"balanced")
constantCircuit=deutsch_jozsca(n,"constant")

print(balancedCircuit.draw())
print(constantCircuit.draw())

simulator= AerSimulator()

balancedResult=simulator.run(balancedCircuit,shots=1).result()

constantResult=simulator.run(constantCircuit,shots=1).result()

print("Balanced function output:- ",list(balancedResult.get_counts().keys())[0])
print("Constant function output:- ",list(constantResult.get_counts().keys())[0])
        