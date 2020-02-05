import matplotlib.pyplot as plt
import numpy as np

task_names = ['WRITING PRODUCTIVITY\nTRACKER', 'TIME SPENT\n PRODUCTIVE']
task_times = [12000, 4555]

plt.xkcd()

fig, ax = plt.subplots()

print(len(task_names))
plt.bar(np.arange(len(task_names)), task_times)
plt.xticks(task_times, task_names)

plt.title("PRODUCTIVITY SO FAR")

plt.draw()
plt.show()
# plt.pause(10)
# plt.clf()
