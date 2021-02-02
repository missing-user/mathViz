import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons


# the actual math
height = 1.1
coneHeight = 0.3

# distance at which it switches to equidistant (ca 89deg)
desiredDistance = 100
maxDistance = 0

# the first cone we want to be able to detect
minDist = 2.5
maxAngle = 0
tilt = 0
a = np.arctan(minDist / height)
angles = [0] * 64
angles[0] = a
safePoints = 3

highPerformance = True
baseline = False

if(len(sys.argv) > 1):
    safePoints = int(sys.argv[1])


def newA():
    return (np.arctan(np.tan(a) * height / (height - coneHeight)))


def distanceFloor(angle):
    return np.tan(angle) * height


def formatDist(angle):
    if(distanceFloor(angle) > 0):
        return "{:5.1f}".format(distanceFloor(angle))
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
fig, ax = plt.subplots(figsize=(15, 8))
plt.subplots_adjust(bottom=0.25)

lines = []
cones = []
fineCones = []
ind = -1
for alpha in angles:
    ind += 1
    line, = plt.plot([0, distanceFloor(alpha)], [height, 0])
    if(ind % safePoints) == 0:
        line.set_color('blue')
        if(distanceFloor(alpha) > 0):
            cone, = plt.plot([distanceFloor(alpha), distanceFloor(alpha)], [
                0, coneHeight], color='orange')
            cone.set_linewidth(5)
            cones.append(cone)
    else:
        line.set_color('lightblue')
    lines.append(line)

# indicator lines for the slider values
tilt_line, = plt.plot([0, 120], [height, 0], color='red')
equidistant_line, = plt.plot(
    [0, 1000*np.cos(tilt)], [height, height + 1000*np.sin(tilt)], color='red')

for d in np.arange(minDist+1, 80, 0.5):
    cone, = plt.plot([d, d], [0, coneHeight], color='orange')
    cone.set_linewidth(0.5)
    fineCones.append(cone)


ax.set_xlim(0, 80)
ax.set_ylim(0, 2 * height)
ax.set_ylabel("height")
ax.set_xlabel("distance from lidar")

ax.margins(x=0)

axcone = plt.axes([0.25, 0.01, 0.65, 0.03])
axspt = plt.axes([0.25, 0.06, 0.65, 0.03])
axtilt = plt.axes([0.25, 0.11, 0.65, 0.03])
axcut = plt.axes([0.25, 0.16, 0.65, 0.03])

tilt_slid = Slider(axtilt, 'tilt', -10, 5, valinit=0)
cutoff_slid = Slider(axcut, 'switch to equidistant',
                     5, 250, valinit=120, valstep=5)
safe_slid = Slider(axspt, 'safe points', 1, 10, valinit=3, valstep=1)
cone_slid = Slider(axcone, 'main laser density', 0.05, 0.3, valinit=0.25)

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


def update(_):
    global tilt
    global coneHeight
    global desiredDistance
    global safePoints
    tilt = np.deg2rad(tilt_slid.val)
    coneHeight = cone_slid.val
    desiredDistance = cutoff_slid.val
    safePoints = int(safe_slid.val)

    tilt_line.set_xdata([0, cutoff_slid.val])
    equidistant_line.set_xdata([0, 1000*np.cos(tilt)])
    equidistant_line.set_ydata([height, height + 1000*np.sin(tilt)])

    if not baseline:
        calcAngles()

    for n in range(0, 64, 1 if highPerformance else safePoints):
        if(angles[n] + tilt <= np.pi / 2):
            lines[n].set_xdata([0, distanceFloor(angles[n] + tilt)])
            lines[n].set_ydata([height, 0])
        else:
            lines[n].set_xdata([0, -distanceFloor(angles[n] + tilt)])
            lines[n].set_ydata([height, 2 * height])

        if((n % safePoints) == 0):
            lines[n].set_color('blue')
        else:
            lines[n].set_color('lightblue')

    global twopcdist
    twopcdist = 999
    for c in (cones+fineCones if highPerformance else cones):
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
        'maxAngle: ', formatDeg(
            maxAngle if not baseline else max(angles) + tilt), "°",
        '\nideal max distance: ', "{:5.1f}".format(maxDistance), " m",
        '\nclosest undetectable cone: ', "{:5.1f}".format(twopcdist), " m",
        '\nideal points per cone: ', str(safePoints)])
    textb.set_text(tstr)

    fig.canvas.draw_idle()


def out(_):
    print('\n\n\nData Print')
    calcAngles(True)
    print()

    print('coneHeight:  \t', coneHeight)
    print('maxDistance: \t', maxDistance)
    print('tilt:        \t', formatDeg(tilt))
    print('twopcdist:   \t', twopcdist)
    print('safePoints:  \t', safePoints)
    print()
    print(angles)
    print()
    for i in range(64):
        print("{:3d}".format(i), '    angle: ', formatDeg((np.pi/2)-angles[i]), '  distance:', formatDist(angles[i]), '     delta a:', formatDeg(
            angles[i] - angles[max(0, i - 1)]), '       diff to ouster: ', formatDeg(angles[i] - ousterAngle(i)))

    plt.figure(2)
    plt.plot(range(64), angles)


def togglePerformance(event):
    if event == "baseline":
        toggleBaseline(event)
    else:
        global highPerformance
        highPerformance = not highPerformance
        for c in fineCones:
            c.set_visible(highPerformance)

        for n in range(0, 64):
            if(not (n % safePoints) == 0):
                lines[n].set_visible(highPerformance)

    update(0)
    fig.canvas.draw_idle()


def toggleBaseline(event):
    global baseline
    global angles
    baseline = not baseline
    angles = []
    angles.extend(np.arange(np.deg2rad(90-22.5),
                            np.deg2rad(90+23), np.deg2rad(0.703125)))


rax = plt.axes([0.91, 0.8, 0.075, 0.15])
check = CheckButtons(rax, ["simplified", "baseline"], [
                     not highPerformance, baseline])


check.on_clicked(togglePerformance)

axbtn = plt.axes([0.05, 0.90, 0.1, 0.075])
bprint = Button(axbtn, 'print')
bprint.on_clicked(out)

tilt_slid.on_changed(update)
cutoff_slid.on_changed(update)
safe_slid.on_changed(update)
cone_slid.on_changed(update)

update(0)
ax.set_title('lidar angle visuzlizer \n(5deg look like a lot due to y scaling)')
plt.show()
