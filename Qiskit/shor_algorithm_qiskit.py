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

def extract_minimal_period(a,N,candidate_denominators):
    if not candidate_denominators:
        return None
    r_lcm=math.lcm(*candidate_denominators)

    valid_multiple=None
    for k in range(1,N+1):
        if pow(a,r_lcm*k,N)==1:
            valid_multiple=r_lcm*k
            break

    if valid_multiple is None:
        return None

    for d in range(1,valid_multiple+1):
        if valid_multiple%d==0 and pow(a,d,N)==1:
            return d
    
    return valid_multiple

def qpe(a,N):
    m=math.ceil(math.log2(N))
    t=2*m
    U_mat,_=build_mod_exp_matrix(a,N)

    qc=QuantumCircuit(t+m,t)
    counting_qubits=list(range(t))
    target_qubits=list(range(t,t+m))

    qc.x(target_qubits[-1])

    qc.h(counting_qubits)

    for k in range(t):
        U_power=np.linalg.matrix_power(U_mat,2**k)
        cU=UnitaryGate(U_power,label=f"U^2^{k})").control(1)
        qc.append(cU,[counting_qubits[k]]+target_qubits)

    qc.append(QFT(num_qubits=t,inverse=True).to_gate(),counting_qubits)
    qc.measure(counting_qubits,range(t))

    sim=AerSimulator()
    t_qc=transpile(qc,sim,basis_gates=['h','p','cp','swap','measure','unitary'])
    counts=sim.run(t_qc,shots=1000).result().get_counts()

    candidate_denominators=[]
    for bitstr in counts.keys():
        val=int(bitstr,2)
        if val==0:
            continue
        phase=val/(2**t)
        frac=Fraction(phase).limit_denominator(N)
        if frac.denominator>1:
            candidate_denominators.append(frac.denominator)

    return extract_minimal_period(a,N,candidate_denominators)

def shors_factoring(N):
    if N%2==0:
        return 2,N//2

    attempts=0

    while True:
        attempts+=1
        a=random.randint(2,N-1)
        gcd_val=math.gcd(a,N)

        if gcd_val>1:
            return gcd_val,N//gcd_val

        r=qpe(a,N)

        if r is None or r%2!=0:
            continue

        val=pow(a,r//2,N)
        if val==N-1:
            continue

        p=math.gcd(val-1,N)
        q=math.gcd(val+1,N)

        if p>1 and p<N:
            return p,N//p
        elif q>1 and q<N:
            return q,N//q

n=random.randint(2,15)

p,q=shors_factoring(2*n-1)
print("N:- ",2*n-1)
print("Factors:- ",p,q)