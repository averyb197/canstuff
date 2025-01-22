import csv
from collections import defaultdict
import numpy as np

from numpy.ma.extras import average

with open("royola_ai_essays_DSI.csv", "r") as feil:
    reader = csv.reader(feil)
    store = defaultdict(list)

    for row in reader:
        temp_val = row[1].split("_")[0]
        store[temp_val].append(row[3])

store.pop("spec")

for key, value in store.items():
    store[key] = list(map(float, value))

with open("sem_dis_scores.txt", "w") as feil:
    for key, val in store.items():
        line = f"Temp: {key}; n = {len(val)}; Mean DSI: {np.mean(val):.4f}; Std: {np.std(val):.4f}; Min/Max: ({min(val):.4f}, {max(val):.4f}) \n"
        feil.write(line)