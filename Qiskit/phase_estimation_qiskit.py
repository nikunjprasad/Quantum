import numpy as np
from qiskit import QuantumCircuit,transpile
from qiskit.circuit.library import QFT,UnitaryGate
from qiskit_aer import AerSimulator
import random

def qpe(U_matrix,stateVector,num_counting_qubits):

    m=int(np.log2(len(stateVector)))
    t=num_counting_qubits

    qc=QuantumCircuit(t+m,t)
    counting_qubits=list(range(t))
    target_qubits=list(range(t,t+m))

    qc.prepare_state(stateVector,target_qubits)

    qc.h(counting_qubits)

    for k in range(t):
        U_power=np.linalg.matrix_power(U_matrix,2**k)
        cU_gate=UnitaryGate(U_power,label="U^2(2^"+str(k)+")").control(1)
        qc.append(cU_gate,[counting_qubits[k]]+target_qubits)

    iqft_gate=QFT(num_qubits=t,inverse=True).to_gate()
    qc.append(iqft_gate,counting_qubits)

    qc.measure(counting_qubits,range(t))
    return qc

theta=random.random()
t_qubits=4

U=np.array([[1,0],[0,np.exp(2j*np.pi*theta)]],dtype=complex)

psi=np.array([0,1],dtype=complex)

circuit=qpe(U,psi,t_qubits)

simulator=AerSimulator()
circuit=transpile(circuit,simulator)
print(circuit.draw())
counts=simulator.run(circuit,shots=1000).result().get_counts()

most_frequent_bitstr=max(counts,key=counts.get)
measured_integer=int(most_frequent_bitstr,2)
estimated_phase=measured_integer/(2**t_qubits)

print("Target Phase:- ",theta)
print("Measured Bitstring:- ",most_frequent_bitstr)
print("Estimated Phase:- ",estimated_phase)
