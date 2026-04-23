import csv
import matplotlib.pyplot as plt

# Log Folder: /home/danilo/Desktop/cth/vd-control/cm-vd/cmpython/logs

CSV_FILES = [
    "/home/danilo/Desktop/cth/vd-control/cm-vd/cmpython/logs/SuspF_Spring_case_1.csv",
    "/home/danilo/Desktop/cth/vd-control/cm-vd/cmpython/logs/SuspF_Spring_case_2.csv",
    "/home/danilo/Desktop/cth/vd-control/cm-vd/cmpython/logs/SuspF_Spring_case_3.csv"
]

CSV_LABELS = [
    "Baseline",
    "Modified",
    "Extra",
]

def read_csv(filename):
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    data = {name: [] for name in header}
    for row in rows:
        for i, name in enumerate(header):
            data[name].append(float(row[i]))

    return data

all_data = [read_csv(filename) for filename in CSV_FILES]

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 9))

# Speed
for data, label in zip(all_data, CSV_LABELS):
    axes[0].plot(data["Time [s]"], data["Speed [km/h]"], label=label)
axes[0].set_ylabel("Speed [km/h]")
axes[0].grid(True)
axes[0].legend()

# Steer
for data, label in zip(all_data, CSV_LABELS):
    axes[1].plot(data["Time [s]"], data["Steer [deg]"], label=label)
axes[1].set_ylabel("Steer [deg]")
axes[1].grid(True)
axes[1].legend()

# ay
for data, label in zip(all_data, CSV_LABELS):
    axes[2].plot(data["Time [s]"], data["ay [m/s²]"], label=label)
axes[2].set_ylabel("ay [m/s²]")
axes[2].set_xlabel("Time [s]")
axes[2].grid(True)
axes[2].legend()

plt.tight_layout()
plt.show()