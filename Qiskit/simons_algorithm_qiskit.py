from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def simons_algorithm(secret_string):
    n=len(secret_string)
    qc=QuantumCircuit(2*n,n)

    for qubit in range(n):
        qc.h(qubit)

    qc.barrier()

    secret_string = secret_string[::-1]

    for qubit in range(n):
        qc.cx(qubit,qubit+n)

    first_one=secret_string.find('1')
    if first_one!=-1:
        for i in range(n):
            if secret_string[i]=='1':
                qc.cx(first_one,i+n)
    
    qc.barrier()
    for qubit in range(n):
        qc.h(qubit)

    qc.measure(range(n),range(n))

    return qc

def solve_equation(measured_strings,n):
    matrix=[[int(bit) for bit in measured_string] for measured_string in measured_strings if measured_string!='0'*n]
    if not matrix:
        return '0'*n
    num_rows=len(matrix)
    pivot_cols=[]
    r=0
    for col in range(n):
        pivot_row=-1
        for row in range(r,num_rows):
            if matrix[row][col]==1:
                pivot_row=row
                break
        if pivot_row==-1:
            continue
        matrix[r],matrix[pivot_row]=matrix[pivot_row],matrix[r]
        pivot_cols.append(col)

        for row in range(num_rows):
            if row!=r and matrix[row][col]==1:
                matrix[row]=[a^b for a,b in zip(matrix[row],matrix[r])]
        r+=1
        if r==num_rows:
            break
    free_cols=[c for c in range(n) if c not in pivot_cols]
    if not free_cols:
        return '0'*n

    s=[0]*n
    chosen_free=free_cols[0]
    s[chosen_free]=1

    for r_idx, p_col in enumerate(pivot_cols):
        val=sum(matrix[r_idx][f]*s[f] for f in free_cols)%2
        s[p_col]=val

    return "".join(map(str,s))
    
    
secret_number=int(input())
secret_string=format(secret_number,'b')
n=len(secret_string)

circuit=simons_algorithm(secret_string)
print(circuit.draw())

simulator=AerSimulator()
counts=simulator.run(circuit,shots=1024).result().get_counts()
measured_strings=list(counts.keys())

recovered_string=solve_equation(measured_strings,n)

print("Secret Number:- ",secret_number)
print("Recovered Number:- ",int(recovered_string,2))

        