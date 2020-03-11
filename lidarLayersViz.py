import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys


# the actual math
height = 1.1
coneHeight = 0.3
desiredDistance = 120  # distance at which it switches to equidistant (ca 89deg)
maxDistance = 0
maxAngle = 0
tilt = 0
a = np.arctan(2.5 / height)
angles = [0] * 64
angles[0] = a
safePoints = 3

if(len(sys.argv)>1):
    print(sys.argv[1])
    safePoints = int(sys.argv[1])

def newA():
    return (np.arctan(np.tan(a) * height / (height - coneHeight)))


def distanceFloor(angle):
    return np.tan(angle) * height


def formatDist(angle):
    return "{:.1f}".format(distanceFloor(angle))


def formatDeg(angle):
    return "{:+.2f}".format(np.rad2deg(angle))


def ousterAngle(layer):
    return np.deg2rad(layer * (45 / 64) + 90 - 22.5)


def calcAngles(prt=False):
    global a
    global maxDistance
    global maxAngle
    delta = 0
    maxDistance = 0
    a = np.arctan(2.5 / height)
    for n in range(0, 64, safePoints):
        if(prt):
            print(n, 'a:', formatDeg(a), '  distance:', formatDist(a), '   delta a:', formatDeg(
            newA() - angles[max(0, n - safePoints)]), 'diff to ouster: ', formatDeg(a - ousterAngle(n)))
        maxDistance = max(maxDistance, distanceFloor(a))
        if(a > np.arctan(desiredDistance / height)):
            a += delta
        else:
            a = newA()
            delta = a - angles[max(0, n - safePoints)]
        angles[n] = a
        for i in range(safePoints):
            angles[n - i] = a - (i * delta / safePoints)
    maxAngle = a
    # print('all angles', angles)
    if(prt):
        print('maxDistance', "{:.1f}".format(maxDistance))
        print('max angle: ', formatDeg(maxAngle))


calcAngles(True)

# configure the plots
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

lines = []
cones = []
ind = -1
for alpha in angles:
    ind += 1
    line, = plt.plot([0, distanceFloor(alpha)], [height, 0])
    if((ind % safePoints) == 0):
        line.set_color('blue')
        cone, = plt.plot([distanceFloor(alpha), distanceFloor(alpha)], [
                         0, coneHeight], color='orange')
        cone.set_linewidth(3)
        cones.append(cone)
    else:
        line.set_color('lightblue')
    lines.append(line)


ax.set_xlim(0, 120)
ax.set_ylim(0, height + 1)

ax.margins(x=0)

axtilt = plt.axes([0.25, 0.1, 0.65, 0.03])
axcone = plt.axes([0.25, 0.15, 0.65, 0.03])

tilt_slid = Slider(axtilt, 'tilt', -5, 5, valinit=0)
cone_slid = Slider(axcone, 'cone height', 0.05, 0.3, valinit=0.3)

textstr = ''.join([
    'maxAngle: ', formatDeg(maxAngle),
    '\nmaxDistance: ', "{:.2f}".format(maxDistance),
    '\nsafePoints: ', str(safePoints)])

# place a text box in upper left in axes coords
textb = plt.text(0.05, 0.95, textstr, transform=ax.transAxes, verticalalignment='top')


def lHitsC(l, c):
    if(l.get_ydata()[1] > 0.3):
        return False

    slope = (l.get_ydata()[1] - height)/l.get_xdata()[1]
    heightAtCone = slope*c.get_xdata()[0]+height
    #print('slope', slope, '   xPos', c.get_xdata()[0])

    if heightAtCone <= 0.3 and heightAtCone >= 0:
        #print(cones.index(c),(c.get_xdata()[1], heightAtCone))
        return True
    return False


def update(val):
    global tilt
    global coneHeight
    tilt = np.deg2rad(tilt_slid.val)
    coneHeight = cone_slid.val
    calcAngles()
    for n in range(0, 64):
        if(angles[n] + tilt <= np.pi / 2):
            lines[n].set_xdata([0, distanceFloor(angles[n] + tilt)])
            lines[n].set_ydata([height, 0])
        else:
            lines[n].set_xdata([0, -distanceFloor(angles[n] + tilt)])
            lines[n].set_ydata([height, 2 * height])

    tstr = ''.join([
            'maxAngle: ', formatDeg(maxAngle+tilt),
            '\nmaxDistance: ', "{:.2f}".format(maxDistance),
            '\nsafePoints: ', str(safePoints)])
    textb.set_text(tstr)

    for c in cones:
        hits = 0
        for laser in lines:
            if(lHitsC(laser, c)):
                hits += 1
        if(hits == 0):
            c.set_color('red')
        elif(hits == 1):
            c.set_color('orange')
        elif(hits == 2):
            c.set_color('yellow')
        elif(hits == 3):
            c.set_color('lightgreen')
        else:
            c.set_color('green')

    fig.canvas.draw_idle()


tilt_slid.on_changed(update)
cone_slid.on_changed(update)

update(0)
plt.show()
