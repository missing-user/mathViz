import matplotlib.pyplot as plt
import numpy as np
from numba import jit

res = 2048
maxIter = 50

@jit
def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return (n, z.real, z.imag)
        else:
            z = z * z + c
    return (n, z.real, z.imag)

def mandelbrot_set(xres, yres, re_start, re_end, im_start, im_end):
    values = np.empty([xres, yres, 3])
    for x in range(xres):
        re_range = re_end - re_start
        mx = (x/xres)*re_range + re_start
        for y in range(yres):
            im_range = im_end - im_start
            my = (y/yres)*im_range + im_start
            values[x][y] = mandelbrot(complex(mx, my), maxIter)
    return values

def get_iterations(input):
    output = []
    for collumn in results:
        output.append([i[0] for i in collumn])
    return output

def get_numbers(input):
    output = []
    for collumn in results:
        output.append([complex(i[1], i[2]) for i in collumn])
    return output

results = mandelbrot_set(res, res, -2, 1,-1,1)

fig, ax = plt.subplots(nrows=2, ncols=2)
ax[0][0].imshow(get_iterations(results), cmap='inferno')
ax[0][0].set_title('iteration count')
complex = np.asarray(get_numbers(results))
ax[1][1].imshow(complex.imag, cmap='inferno')
ax[1][1].set_title('imaginary component')
ax[0][1].imshow(complex.real, cmap='inferno')
ax[0][1].set_title('real component')
ax[1][0].imshow(results)
ax[1][0].set_title('combined')
plt.gray()
plt.show()
