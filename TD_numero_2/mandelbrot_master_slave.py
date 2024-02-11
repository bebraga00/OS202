# compute the Mandelbrot set 
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm

from mpi4py import MPI

# global communication
globCom = MPI.COMM_WORLD.Dup()
# number of processes
nbp     = globCom.size
# identifier for each process
rank    = globCom.rank

if nbp == 1:
    print("At least two processes for the master-slave architecture!")
    exit(1)

# Mandelbrot set definition and methods
@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z:    complex
        iter: int

        # we verify initially that the complex
        # does not belong to a known convergence zone
        #   1. belonging to the discs C0{(0,0),1/4} and C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2. belonging to the cardioid {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # else, we iterate
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations

# Mandelbrot calculation parameters
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

# the new height is divided between the processes except for the master
new_height = height // (nbp - 1)
scaleX = 3./width
scaleY = 2.25/height
if rank != 0:
    convergence = np.empty((width, new_height), dtype=np.double)
else:
    convergence = np.empty((width, 0), dtype=np.double)

# send and receive the data necessary to the calculations
if(rank == 0):
    for i in range(nbp - 1):
        data_to_send = [new_height, i * new_height]
        globCom.send(data_to_send, dest=(i + 1))
elif(rank != 0):
    data_received = []
    data_received = globCom.recv(source=0)

# Mandelbrot set computation
if(rank != 0):
    deb = time()
    for y in range(data_received[0]):
        for x in range(width):
            c = complex(-2. + scaleX*x, -1.125 + scaleY * (y + data_received[1]))
            convergence[x, y] = mandelbrot_set.convergence(c, smooth=True)
    fin = time()
    diff = fin - deb
    print(f"Mandelbrot set computation time in rank ", rank, ": ", diff, sep="")
    globCom.send(convergence, dest=0)
else:
    for i in range(nbp - 1):
        convergence = np.concatenate((convergence, globCom.recv(source=(i + 1))), axis=1)
    deb = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence.T)*255))
    fin = time()
    print(f"Time to image constitution: {fin-deb}")
    img_name = "image_master_slave.png"
    image.save(img_name)