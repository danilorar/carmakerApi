import csv
import matplotlib.pyplot as plt

LOG_PATH = "/home/danilo/Desktop/cth/vd-control/cm-vd/cmpython/logs/"

CSV_FILES = [
    f"{LOG_PATH}/acc_soft.csv",
    f"{LOG_PATH}/acc_medium.csv",
    f"{LOG_PATH}/acc_hard.csv"
]

CSV_LABELS = [
    "Soft",
    "Medium",
    "Hard"
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


# ==================================
# === Figure 1: Car v, Delta, ax ===
# ==================================

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 9))
plt.suptitle("Car Speed, Steering, Acceleration")

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

# ax
for data, label in zip(all_data, CSV_LABELS):
    axes[2].plot(data["Time [s]"], data["Car ax [m/s²]"], label=label)
axes[2].set_ylabel("ax [m/s²]")
axes[2].set_xlabel("Time [s]")
axes[2].grid(True)
axes[2].legend()

plt.tight_layout()


# ================================
# === Figure 2: IMU ax, ay, az ===
# ================================

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 9))
plt.suptitle("IMU Accelerations")

# ax
for data, label in zip(all_data, CSV_LABELS):
    axes[0].plot(data["Time [s]"], data["IMU ax [m/s²]"], label=label)
axes[0].set_ylabel("IMU ax [m/s²]")
axes[0].grid(True)
axes[0].legend()

# ay
for data, label in zip(all_data, CSV_LABELS):
    axes[1].plot(data["Time [s]"], data["IMU ay [m/s²]"], label=label)
axes[1].set_ylabel("IMU ay [m/s²]")
axes[1].grid(True)
axes[1].legend()

# az
for data, label in zip(all_data, CSV_LABELS):
    axes[2].plot(data["Time [s]"], data["IMU az [m/s²]"], label=label)
axes[2].set_ylabel("IMU az [m/s²]")
axes[2].set_xlabel("Time [s]")
axes[2].grid(True)
axes[2].legend()

plt.tight_layout()


# ================================
# === Figure 3: IMU wx, wy, wz ===
# ================================

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 9))
plt.suptitle("IMU Angular Velocities")

# wx
for data, label in zip(all_data, CSV_LABELS):
    axes[0].plot(data["Time [s]"], data["IMU wx [rad/s]"], label=label)
axes[0].set_ylabel("IMU wx [rad/s]")
axes[0].grid(True)
axes[0].legend()

# wy
for data, label in zip(all_data, CSV_LABELS):
    axes[1].plot(data["Time [s]"], data["IMU wy [rad/s]"], label=label)
axes[1].set_ylabel("IMU wy [rad/s]")
axes[1].grid(True)
axes[1].legend()

# wz
for data, label in zip(all_data, CSV_LABELS):
    axes[2].plot(data["Time [s]"], data["IMU wz [rad/s]"], label=label)
axes[2].set_ylabel("IMU wz [rad/s]")
axes[2].grid(True)
axes[2].legend()

plt.tight_layout()


# ==============================
# === Figure 4: pos x, pos_y ===
# ==============================

fig, ax = plt.subplots(figsize=(10, 9))
plt.suptitle("IMU Position")

for data, label in zip(all_data, CSV_LABELS):
    ax.plot(data["IMU pos X [m]"],data["IMU pos Y [m]"], label=label)
ax.set_xlabel("Time [s]")
ax.set_ylabel("IMU pos [m]")
ax.grid(True)
ax.legend() 

plt.tight_layout()

plt.show()

if __name__ == "__main__":
    pass