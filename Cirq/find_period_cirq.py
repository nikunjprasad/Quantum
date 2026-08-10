import math
import random
import numpy as np
from fractions import Fraction
import cirq

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

    counting_qubits=[cirq.LineQubit(qubit) for qubit in range(t_counting)]
    target_qubits=[cirq.LineQubit(t_counting+qubit) for qubit in range(m)]

    circuit=cirq.Circuit()
    
    psi_1=np.zeros(2**m,dtype=complex)
    psi_1[1]=1.0
    A=np.eye(2**m,dtype=complex)
    A[:,0]=psi_1
    Q,_=np.linalg.qr(A)
    circuit.append(cirq.MatrixGate(Q).on(*target_qubits))

    circuit.append(cirq.H.on_each(counting_qubits))

    for j in range(t_counting):
        power=2**(t_counting-1-j)
        U_power=np.linalg.matrix_power(U_mat,power)
        cU=cirq.MatrixGate(U_power).controlled()
        circuit.append(cU(counting_qubits[j],*target_qubits))

    circuit.append(cirq.qft(*counting_qubits,inverse=True))

    circuit.append(cirq.measure(counting_qubits,key='result'))

    return circuit,t_counting


N=random.randint(3,15)
while True:
    a=random.randint(2,N-2)
    if math.gcd(a,N)==1:
        break
        
circuit,t_counting=find_period(a,N)
print(circuit)

simulator=cirq.Simulator()
result=simulator.run(circuit,repetitions=1000)
histogram=result.histogram(key='result')

candidate_r_list=[]
for measured_int in histogram.keys():
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