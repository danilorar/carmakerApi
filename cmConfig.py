import math
from pathlib import Path

PROJECT_PATH = Path("/home/danilo/Desktop/cth/vd-control/cm-vd")
TESTRUN_PATH = Path("/home/danilo/Desktop/cth/vd-control/cm-vd/Data/TestRun/acceleration")    
VEHICLE_PATH = Path("/home/danilo/Desktop/cth/vd-control/cm-vd/Data/Vehicle/PolestarPy")

# cm-signal, label, conversion function
SIGNALS = [
    ("Time", "Time [s]", lambda x: x),
    ("Car.v", "Speed [km/h]", lambda x: x * 3.6),
    ("Driver.Steer.Ang", "Steer [deg]", math.degrees),
    ("Car.ax", "ax [m/s²]", lambda x: x),
    ("Car.ay", "ay [m/s²]", lambda x: x),
    ("Car.az", "az [m/s²]", lambda x: x),
]   

# if RUN_MODE is set to "cases"
CASES = [
    {
        "run_name": "baseline",
        "parameter_changes": {}
    },
    {
        "run_name": "front_spring_5000",
        "parameter_changes": {
            "SuspF.Spring": 50000
        }
    },
    {
        "run_name": "rear_spring_6000",
        "parameter_changes": {
            "SuspR.Spring": 60000
        }
    },
    {
        "run_name": "front_rear_combo",
        "parameter_changes": {
            "SuspF.Spring": 50000,
            "SuspR.Spring": 100000
        }
        }
]