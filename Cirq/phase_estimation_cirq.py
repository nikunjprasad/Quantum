import numpy as np
import cirq
import random

def qpe(U_matrix,stateVector,num_counting_qubits):

    m=int(np.log2(len(stateVector)))
    t=num_counting_qubits

    
    counting_qubits=[cirq.LineQubit(qubit) for qubit in range(t)]
    target_qubits=[cirq.LineQubit(t+qubit) for qubit in range(m)]

    circuit=cirq.Circuit()

    dim=len(stateVector)
    A=np.eye(dim,dtype=complex)
    A[:,0]=stateVector
    Q,R=np.linalg.qr(A)
    phase=R[0,0]/abs(R[0,0]) if R[0,0]!=0 else 1

    V_prep=Q/phase
    circuit.append(cirq.MatrixGate(V_prep).on(*target_qubits))

    circuit.append(cirq.H.on_each(counting_qubits))

    for j in range(t):
        power=2**(t-1-j)
        U_power=np.linalg.matrix_power(U_matrix,power)
        cU=cirq.MatrixGate(U_power).controlled()
        circuit.append(cU(counting_qubits[j],*target_qubits))

    circuit.append(cirq.qft(*counting_qubits,inverse=True))

    circuit.append(cirq.measure(counting_qubits,key='result'))
    return circuit

theta=random.random()
t_qubits=4

U=np.array([[1,0],[0,np.exp(2j*np.pi*theta)]],dtype=complex)

psi=np.array([0,1],dtype=complex)

circuit=qpe(U,psi,t_qubits)
print(circuit)

simulator=cirq.Simulator()
result=simulator.run(circuit,repetitions=1000)

histogram=result.histogram(key='result')
most_frequent_integer=max(histogram,key=histogram.get)
estimated_phase=most_frequent_integer/(2**t_qubits)

print("Target Phase:- ",theta)
print("Measured Integer:- ",most_frequent_integer)
print("Estimated Phase:- ",estimated_phase)