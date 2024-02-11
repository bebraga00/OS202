# Produit matrice-vecteur v = A.u
import numpy as np
from time import time

from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank

# problem dimension
dim = 12
# new line dimension
new_line = dim // nbp
# offset for each matrix
offset = rank * dim//nbp
# matrix initialisation
A = np.array([[(i + j + offset) % dim+1. for i in range(dim)] for j in range(new_line)])
print(rank, ": A =", A)

# vector initialisation
u = np.array([i+1. for i in range(dim)])
print(rank, ": u =", u)

# matrix-vector product
beg = time()
v_interm = A.dot(u)
print(rank, ": v_interm =", v_interm)
v = np.empty(dim)

globCom.Allgather(v_interm, v)
end = time()
diff = end - beg
print(rank, ": v =", v)
print(rank, ": temps pour la multiplication :", diff)