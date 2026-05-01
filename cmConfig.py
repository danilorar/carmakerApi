import math
from pathlib import Path

PROJECT_PATH = Path("/home/danilo/Desktop/cth/vd-control/cm-vd")
TESTRUN_PATH = Path(f"{PROJECT_PATH}/Data/TestRun/acceleration")
VEHICLE_PATH = Path(f"{PROJECT_PATH}/Data/Vehicle/PolestarPy")

# cm-signal, label, conversion function (hover in IPGControl to see signal names)
SIGNALS = [

    ("Time", "Time [s]", lambda x: x),
    ("Driver.Steer.Ang", "Steer [deg]", math.degrees),

    # other signals
    ("Car.v", "Speed [km/h]", lambda x: x * 3.6),    
    ("Car.ax", "Car ax [m/s²]", lambda x: x),
    ("Car.ay", "Car ay [m/s²]", lambda x: x),
    ("Car.az", "Car az [m/s²]", lambda x: x),

    # IMU 
    # accelerometer
    ("Sensor.Inertial.Vhcl.Veh_IMU.Acc_0.x", "IMU ax [m/s²]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Acc_0.y", "IMU ay [m/s²]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Acc_0.z", "IMU az [m/s²]", lambda x: x),

    # gyroscope
    ("Sensor.Inertial.Vhcl.Veh_IMU.Omega_0.x", "IMU wx [rad/s]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Omega_0.y", "IMU wy [rad/s]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Omega_0.z", "IMU wz [rad/s]", lambda x: x), 
    
    # gps
    ("Sensor.Inertial.Vhcl.Veh_IMU.Pos_0.x", "IMU pos [m]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Pos_0.y", "IMU pos [m]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Pos_0.z", "IMU pos [m]", lambda x: x),
 
]

# if RUN_MODE is set to "cases" or "sequential"
CASES = [
    {
        "run_name": "acc_base",
        "parameter_changes": {}
    },
    {
        "run_name": "acc_soft",
        "parameter_changes": {
            "SuspF.Spring": 40000,
            "SuspR.Spring": 60000
        }
    },
    {
        "run_name": "acc_medium",
        "parameter_changes": {
            "SuspR.Spring": 80000,
            "SuspF.Spring": 90000   
        }
    },
    {
        "run_name": "acc_hard",
        "parameter_changes": {
            "SuspF.Spring": 90000,
            "SuspR.Spring": 110000
        }
    }
]