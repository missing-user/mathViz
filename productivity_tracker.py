from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import matplotlib.pyplot as plt
import numpy as np

process_time={}
timestamp = {}


plt.xkcd()

def draw_chart(process_dict):

    tasks = ['WRITING PRODUCTIVITY\nTRACKER']
    times = [600]
    for i in process_dict:
        tasks.append(i)
        times.append(process_dict[i])


    y_pos = np.arange(len(tasks))

    plt.clf()
    plt.bar(y_pos, times, align='center')
    plt.xticks(y_pos, tasks)
    plt.ylabel('USAGE TIME')

    plt.title("PRODUCTIVITY SO FAR")
    plt.pause(1)



while True:
    current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
    timestamp[current_app] = int(time.time())
    time.sleep(1)
    if current_app not in process_time.keys():
        process_time[current_app] = 0
    process_time[current_app] = process_time[current_app]+int(time.time())-timestamp[current_app]
    print(process_time)
    draw_chart(process_time)
