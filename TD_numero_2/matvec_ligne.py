# Produit matrice-vecteur v = A.u
import numpy as np
from time import time

from mpi4py import MPI

# Communication global, default
globCom = MPI.COMM_WORLD.Dup()
# Nombre de processus
nbp     = globCom.size
# Identifieur de chaque processus
rank    = globCom.rank

# Dimension du problème (peut-être changé)
dim = 12
# nouvelle dimension de lignes
new_line = dim // nbp
# offset pour chaque matrice
offset = rank * dim//nbp
# Initialisation de la matrice
A = np.array([[(i + j + offset) % dim+1. for i in range(dim)] for j in range(new_line)])
print(rank, ": A =", A)

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
print(rank, ": u =", u)

# Produit matrice-vecteur
beg = time()
v_interm = A.dot(u)
print(rank, ": v_interm =", v_interm)
v = np.empty(dim)
# fonction qui accumule les variables v_interm et concatene le resultat dans v
globCom.Allgather(v_interm, v)
end = time()
diff = end - beg
print(rank, ": v =", v)
print(rank, ": temps pour la multiplication :", diff)