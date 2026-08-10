import math
import random
import numpy as np
from fractions import Fraction
from qiskit import QuantumCircuit,transpile
from qiskit.circuit.library import QFT,UnitaryGate
from qiskit_aer import AerSimulator

def build_mod_exp_matrix(a,N):
    m=math.ceil(math.log2(N))
    dim=2**m
    U=np.zeros((dim,dim),dtype=complex)
    for y in range(dim):
        if y<N:
            U[(a*y)%N,y]=1.0
        else:
            U[y,y]=1.0
    return U,m
    
def find_period(a,N):
    t_counting=2*math.ceil(math.log2(N))
    U_mat,m=build_mod_exp_matrix(a,N)

    qc=QuantumCircuit(t_counting+m,t_counting)
    counting_qubits=list(range(t_counting))
    target_qubits=list(range(t_counting,t_counting+m))

    psi_1=np.zeros(2**m,dtype=complex)
    psi_1[1]=1.0
    qc.prepare_state(psi_1,target_qubits)

    qc.h(counting_qubits)

    for k in range(t_counting):
        U_power=np.linalg.matrix_power(U_mat,2**k)
        cU_gate=UnitaryGate(U_power,label="U^(2^"+str(k)+")").control(1)
        qc.append(cU_gate,[counting_qubits[k]]+target_qubits)

    iqft_gate=QFT(num_qubits=t_counting,inverse=True).to_gate()
    qc.append(iqft_gate,counting_qubits)

    qc.measure(counting_qubits,range(t_counting))

    return qc,t_counting


N=random.randint(3,15)
while True:
    a=random.randint(2,N-2)
    if math.gcd(a,N)==1:
        break
        
circuit,t_counting=find_period(a,N)
print(circuit.draw())

simulator=AerSimulator()
circuit=transpile(circuit,simulator)
counts=simulator.run(circuit,shots=1000).result().get_counts()

candidate_r_list=[]
for bitstring in counts.keys():
    measured_int=int(bitstring,2)
    if measured_int==0:
        continue
    phase=measured_int/(2**t_counting)
    frac=Fraction(phase).limit_denominator(N)
    if frac.denominator>1:
        candidate_r_list.append(frac.denominator)
r_lcm=math.lcm(*candidate_r_list)

for k in range(1,N+1):
    r_test=r_lcm*k
    if pow(a,r_test,N)==1:
        r=r_test
        break

print("a:- ",a," N:- ",N)
print("Measured Phase:- ",phase)
print("Calculated Period:- ",r)
print("a^r mod N:- ",(a**r)%N)