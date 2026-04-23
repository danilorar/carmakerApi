import math
from pathlib import Path

PROJECT_PATH = Path("/home/danilo/Desktop/cth/vd-control/cm-vd")
TESTRUN_PATH = Path("/opt/ipg/carmaker/linux64-14.1.1/Data/TestRun/Examples/VehicleDynamics/Handling/Slalom18m")
VEHICLE_PATH = Path("/opt/ipg/carmaker/linux64-14.1.1/Data/Vehicle/Examples/Demo_Tesla_Y")

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
            "SuspF.Spring": [[0.0, 0.0], [0.1, 5000.0], [1.0, 50000.0]]
        }
    },
    {
        "run_name": "rear_spring_6000",
        "parameter_changes": {
            "SuspR.Spring": [[0.0, 0.0], [0.1, 6000.0], [1.0, 60000.0]]
        }
    },
    {
        "run_name": "front_rear_combo",
        "parameter_changes": {
            "SuspF.Spring": [[0.0, 0.0], [0.1, 5000.0], [1.0, 50000.0]],
            "SuspR.Spring": [[0.0, 0.0], [0.1, 6000.0], [1.0, 60000.0]]
        }
        }
]