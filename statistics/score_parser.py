import csv
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from scipy.optimize import curve_fit

def exponential_model(T, beta0, beta1):
    return beta0 * np.exp(beta1 * T)

with open("royola_ai_essays_DSI.csv", "r") as feil:
    reader = csv.reader(feil)
    store = defaultdict(list)

    for row in reader:
        temp_val = row[1].split("_")[0]
        store[temp_val].append(row[3])

store.pop("spec")

for key, value in store.items():
    store[key] = list(map(float, value))

pts = []
xval = 0
for key, value in store.items():
    for n in value:
        pts.append((xval, n))
    xval += 0.2

x, y = zip(*pts)
np.save('temp_vs_dsi.npy', (np.array(x), np.array(y)))


# print(np.mean(y), np.std(y))
# r = pearsonr(x, y)
#
# params, covariance = curve_fit(exponential_model, x, y)
# print(f"params = {params}")
# print(f"covariance = {covariance}")
# print("=====")
# print(r)


# with open("sem_dis_scores.txt", "w") as feil:
#     lines = []
#     for key, val in store.items():
#         lines.append(f"Temp: {key}; n = {len(val)}; Mean DSI: {np.mean(val):.4f}; Std: {np.std(val):.4f}; Min/Max: ({min(val):.4f}, {max(val):.4f}) \n")
#     with open("sem_dis_scores.txt", "w") as feil:
#         feil.write(f"r = {r[0]:.4f}; p = {r[1]:.4f}\n")
#         for i in lines:
#             feil.write(i)

#
# T_fit = np.linspace(min(x), max(x), 100)
# y_fit = exponential_model(T_fit, params[0], params[1])
#
# plt.plot(T_fit, y_fit)
# plt.scatter(x, y)
# plt.show()

