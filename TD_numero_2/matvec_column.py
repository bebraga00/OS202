import numpy as np
from time import time

from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank

# problem dimension
dim = 12
# new column dimension
new_column = dim // nbp
# offset for each matrix
offset = rank * dim//nbp
# matrix initialisation
A = np.array([[(i + j + offset) % dim+1. for i in range(new_column)] for j in range(dim)])
print(rank, ": A =", A)

# vector initialisation
u = np.array([offset+i+1. for i in range(new_column)])
print(rank, ": u =", u)

# matrix-vector product
beg = time()
v_interm = A.dot(u)
print(rank, ": v_interm =", v_interm)
v = np.empty(dim)

globCom.Allreduce(v_interm, v, op=MPI.SUM)
end = time()
diff = end - beg
print(rank, ": v =", v)
print(rank, ": time : ", diff, sep="")