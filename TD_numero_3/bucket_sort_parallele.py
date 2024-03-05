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
    print("At least two processes for the master-slave architecture!")
    exit(1)

if(rank == 0):
    # create the vector to be sorted
    deb = time()
    s = 0
    dim = 1000
    max = 100
    np.random.seed(s)
    A = np.random.randint(0, max, dim)

    # create a vector to be sent to the buckets
    B = [[] for _ in range(nbp - 1)]

    # separate the data into the buckets
    for i in range(dim):
        where = ((nbp - 1) * A[i]) // max
        B[where].append(A[i])

    # sent the data to the processes
    for i in range(nbp - 1):
        globCom.send(B[i], dest=(i+1))

    # receive and append the vectors
    A = []
    for i in range(nbp - 1):
        A += globCom.recv(source=i+1)
    fin = time()
    print("Total computation time:", (fin - deb))

else:
    received = []
    received = globCom.recv(source=0)
    received.sort()
    globCom.send(received, dest=0)
