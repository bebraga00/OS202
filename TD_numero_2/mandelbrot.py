import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm

from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank

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

        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations

mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

new_height = height // nbp
scaleX = 3./width
scaleY = 2.25/height
convergence = np.empty((width, new_height), dtype=np.double)

deb = time()
offset = rank * new_height
for y in range(new_height):
    for x in range(width):
        c = complex(-2. + scaleX*x, -1.125 + scaleY * (y + offset))
        convergence[x, y] = mandelbrot_set.convergence(c, smooth=True)
fin = time()
diff = fin - deb
print(f"Mandelbrot set computation time in rank ", rank, ": ", diff, sep="")

if(rank != 0):
    globCom.Send(convergence, dest=0)
    print("Sent from rank", rank)
else:
    for i in range(nbp - 1):
        received = np.empty((width, new_height), dtype=np.double)
        globCom.Recv(received, source=(i + 1))
        print("Received from rank", i + 1)
        convergence = np.concatenate((convergence, received), axis=1)
    deb = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence.T)*255))
    fin = time()
    print(f"Time to image constitution: {fin-deb}")
    img_name = "image.png"
    image.save(img_name)
