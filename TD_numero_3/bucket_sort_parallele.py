import numpy as np
# import math
from time import time
# from random import random
from mpi4py import MPI
import math

globCom = MPI.COMM_WORLD.Dup()
nbp = globCom.size
rank = globCom.rank

if(nbp == 1):
    print("Au moins deux processus pour l'architecture maitre-esclave !")
    exit(1)

if(rank == 0):
    # Creer le tableau aleatoire qui sera trie
    s = 0
    dim = 10
    max = 100
    np.random.seed(s)
    A = np.random.randint(0, max, dim)
    print(A)

    # Creer le tableau pour separer les buckets
    B = [[] for _ in range(nbp - 1)]

    # Decider quelles donnees seront envoyees a quel processus
    for i in range(dim):
        where = ((nbp - 1) * A[i]) // max
        B[where].append(A[i])

    # Envoyer les tableaux aux processus
    for i in range(nbp - 1):
        globCom.send(B[i], dest=(i+1))
        print("Sent", B[i], "to rank", i+1)

    # Recevoir et concatener les vecteurs
    A = []
    for i in range(nbp - 1):
        A += globCom.recv(source=i+1)
    print(A)

else:
    received = []
    received = globCom.recv(source=0)
    received.sort()
    globCom.send(received, dest=0)
