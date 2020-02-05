from win32gui import GetForegroundWindow
import psutil
import matplotlib.animation as animation
import time
import win32process
import matplotlib.pyplot as plt
import numpy as np
import sys

process_time = {}
timestamp = {}


plt.xkcd()
fig, ax = plt.subplots()

def draw_chart(frame):
    process_dict = get_process_times()
    tasks = ['WRITING PRODUCTIVITY\nTRACKER']
    times = [600]
    for i in process_dict:
        if(process_dict[i] > 20):
            tasks.append(i.upper())
            times.append(process_dict[i])

    y_pos = np.arange(len(times))


    ax.clear()
    plt.xkcd()
    ax.bar(y_pos, times, align='center')
    y_pos = np.arange(len(tasks))
    ax.set_ylabel('TIME SPENT')
    ax.set_title("PRODUCTIVITY SO FAR")
    plt.xticks(y_pos, tasks)


anim_interval = 1
process_time={}


def get_process_times():
    try:
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
    except:
        print('error getting process')
        return process_time

    if current_app not in process_time.keys():
        process_time[current_app] = 0
    process_time[current_app] += anim_interval
    print(process_time)
    return process_time


animator = animation.FuncAnimation(fig, draw_chart, interval=500)

plt.show()
