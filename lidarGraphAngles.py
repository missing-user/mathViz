import matplotlib.pyplot as plt
import numpy as np

angles = [ 1.97676566e+01,  1.80633474e+01,  1.63590382e+01,  1.49208299e+01,
  1.34826217e+01 , 1.22813269e+01,  1.10800321e+01,  1.00837831e+01,
  9.08753421e+00,  8.26539853e+00 , 7.44326285e+00,  6.76708949e+00,
  6.09091613e+00,  5.53605616e+00 , 4.98119619e+00,  4.52658281e+00,
  4.07196944e+00 , 3.69987481e+00  ,3.32778019e+00,  3.02343627e+00,
  2.71909236e+00 , 2.47027817e+00  ,2.22146399e+00,  2.01811057e+00,
  1.81475714e+00 , 1.64859266e+00  ,1.48242817e+00,  1.34667028e+00,
  1.21091238e+00 , 1.10000716e+00  ,9.89101929e-01,  8.98505249e-01,
  8.07908569e-01,  7.17311889e-01 , 6.26715209e-01,  5.36118529e-01,
  4.45521849e-01,  3.54925169e-01 , 2.64328488e-01,  1.73731808e-01,
  8.31351283e-02, -7.46155180e-03 ,-9.80582319e-02, -1.88654912e-01,
 -2.79251592e-01, -3.69848272e-01 ,-4.60444952e-01, -5.51041632e-01,
 -6.41638312e-01, -7.32234992e-01 ,-8.22831673e-01, -9.13428353e-01,
 -1.00402503e+00, -1.09462171e+00 ,-1.18521839e+00, -1.27581507e+00,
 -1.36641175e+00, -1.45700843e+00 ,-1.54760511e+00, -1.63820179e+00,
 -1.72879847e+00,  -1.81939515e+00, -1.90999183e+00,  (-1.90999183e+00 -0.09059667999999999)   ]



def ousterAngle(layer):
    #print('layer:', layer, '   ', formatDeg(np.deg2rad(layer * (45 / 64) + 90 - 22.5)))
    return 22.5 - layer * (45 / 64)


ouster = np.zeros(len(angles))
# angles = np.rad2deg(angles)

for i in range(len(angles)):
    ouster[i] = ousterAngle(i)
print('ouster')
print(ouster)
print()
print('target angles')
print(angles)
print()
print('difference')
print(angles-ouster)

plt.plot(ouster, label="ouster angle")
plt.plot(angles, label="target lens angle")
plt.plot(angles-ouster, label="difference")
plt.legend(bbox_to_anchor=(0.25, 1), loc='upper left', borderaxespad=0.)
plt.ylabel('angle in degrees')
plt.show()
