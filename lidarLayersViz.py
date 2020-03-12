import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# the actual math
height = 1.1
coneHeight = 0.3

# distance at which it switches to equidistant (ca 89deg)
desiredDistance = 120
maxDistance = 0

#the first cone we want to be able to detect
minDist = 1.5
maxAngle = 0
tilt = 0
a = np.arctan(minDist / height)
angles = [0] * 64
angles[0] = a
safePoints = 3

if(len(sys.argv) > 1):
    safePoints = int(sys.argv[1])


def newA():
    return (np.arctan(np.tan(a) * height / (height - coneHeight)))


def distanceFloor(angle):
    return np.tan(angle) * height


def formatDist(angle):
    if(distanceFloor(angle) > 0):
        return "{:5.1f}".format(distanceFloor(angle))
    else:
        return " --- "


def formatDeg(angle):
    return "{:+3.2f}".format(np.rad2deg(angle))


def ousterAngle(layer):
    #print('layer:', layer, '   ', formatDeg(np.deg2rad(layer * (45 / 64) + 90 - 22.5)))
    return np.deg2rad(layer * (45 / 64) + 90 - 22.5)


def calcAngles(prt=False):
    global a
    global maxDistance
    global maxAngle
    delta = 0
    maxDistance = 0
    a = np.arctan(minDist / height)
    for n in range(0, 64, safePoints):
        maxDistance = max(maxDistance, distanceFloor(a))
        if(a > np.arctan(desiredDistance / height)):
            a += delta
        else:
            a = newA()
            delta = a - angles[max(0, n - safePoints)]
        angles[n] = a
        if(prt):
            print("{:3d}".format(n), '    angle: ', formatDeg(a), '  distance:', formatDist(a), '     delta a:', formatDeg(
                a - angles[max(0, n - safePoints)]), '       diff to ouster: ', formatDeg(a - ousterAngle(n)))
        for i in range(safePoints):
            angles[n - i] = a - (i * delta / safePoints)
    maxAngle = a
    # print('all angles', angles)
    if(prt):
        print()
        print('maxDistance:   \t', "{:.1f}".format(maxDistance))
        print('max angle:     \t', formatDeg(maxAngle))


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
        if(distanceFloor(alpha) > 0):
            cone, = plt.plot([distanceFloor(alpha), distanceFloor(alpha)], [
                         0, coneHeight], color='orange')
            cone.set_linewidth(5)

            cones.append(cone)
    else:
        line.set_color('lightblue')
    lines.append(line)

for d in np.arange(3, 120):
    cone, = plt.plot([d, d], [
                 0, coneHeight], color='orange')
    cone.set_linewidth(0.5)

    cones.append(cone)


ax.set_xlim(0, 120)
ax.set_ylim(0, 2 * height)

ax.margins(x=0)

axtilt = plt.axes([0.25, 0.1, 0.65, 0.03])
axcone = plt.axes([0.25, 0.15, 0.65, 0.03])

tilt_slid = Slider(axtilt, 'tilt', -5, 5, valinit=0)
cone_slid = Slider(axcone, 'cone height', 0.05, 0.3, valinit=0.3)

# place a text box in upper left in axes coords
textb = plt.text(0.05, 0.95, 'initial text',
                 transform=ax.transAxes, verticalalignment='top')


def lHitsC(l, c):
    if(l.get_ydata()[1] > 0.3):
        return False

    slope = (l.get_ydata()[1] - height) / l.get_xdata()[1]
    heightAtCone = slope * c.get_xdata()[0] + height
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

    global twopcdist
    twopcdist = 999
    for c in cones:
        hits = 0
        for laser in lines:
            if(lHitsC(laser, c)):
                hits += 1
        if(hits == 0):
            c.set_color('red')
            twopcdist = min(twopcdist, c.get_xdata()[0])
        elif(hits == 1):
            c.set_color('orange')
            twopcdist = min(twopcdist, c.get_xdata()[0])
        elif(hits == 2):
            c.set_color('yellow')
            #twopcdist = min(twopcdist, c.get_xdata()[0])
        elif(hits == 3):
            c.set_color('lightgreen')
        else:
            c.set_color('green')

    tstr = ''.join([
        'maxAngle: ', formatDeg(maxAngle + tilt),
        '\nideal max distance: ', "{:5.1f}".format(maxDistance),
        '\n closest undetectable cone: ', "{:5.1f}".format(twopcdist),
        '\nsafePoints: ', str(safePoints)])
    textb.set_text(tstr)

    fig.canvas.draw_idle()


def out(event):
    print('\n\n\nData Print')
    calcAngles(True)
    print()

    print('coneHeight:  \t', coneHeight)
    print('maxDistance: \t', maxDistance)
    print('tilt:        \t', formatDeg(tilt))
    print('twopcdist:   \t', twopcdist)
    print('safePoints:  \t', safePoints)



axbtn = plt.axes([0.05, 0.05, 0.1, 0.075])
bprint = Button(axbtn, 'print')
bprint.on_clicked(out)

tilt_slid.on_changed(update)
cone_slid.on_changed(update)

update(0)
ax.set_title('lidar angle visuzlizer \n(5deg look like a lot due to y scaling)')
plt.show()
