import math
from pathlib import Path

MANEUVER = "cornering"  # or "acc_brake"
PROJECT_PATH = Path("/home/danilo/Desktop/cth/vd-control/cm-vd")
TESTRUN_PATH = Path(f"{PROJECT_PATH}/Data/TestRun/{MANEUVER}")
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

    # IMU (B)
    # accelerometer
    ("Sensor.Inertial.Vhcl.Veh_IMU.Acc_B.x", "IMU ax [m/s²]", lambda x: -x), # inverted for dataproc
    ("Sensor.Inertial.Vhcl.Veh_IMU.Acc_B.y", "IMU ay [m/s²]", lambda x: x), 
    ("Sensor.Inertial.Vhcl.Veh_IMU.Acc_B.z", "IMU az [m/s²]", lambda x: x),

    # gyroscope
    ("Sensor.Inertial.Vhcl.Veh_IMU.Omega_B.x", "IMU wx [rad/s]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Omega_B.y", "IMU wy [rad/s]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Omega_B.z", "IMU wz [rad/s]", lambda x: -x), # inverted for dataproc
    
    # gps
    ("Sensor.Inertial.Vhcl.Veh_IMU.Pos_B.x", "IMU pos X [m]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Pos_B.y", "IMU pos Y [m]", lambda x: x),
    ("Sensor.Inertial.Vhcl.Veh_IMU.Pos_B.z", "IMU pos Z [m]", lambda x: x),
 
]

# if RUN_MODE is set to "cases" or "sequential"
CASES = [
    {
        "run_name": f"{MANEUVER}_base",
        "parameter_changes": {
             # no changes  
        }
    },
     {
        "run_name": f"{MANEUVER}_soft",
        "parameter_changes": {
            "SuspF.Damp_Push.Amplify": 0.5,
            "SuspF.Damp_Pull.Amplify": 0.5,
            "SuspR.Damp_Push.Amplify": 0.5,
            "SuspR.Damp_Pull.Amplify": 0.5
        }
    },
    {
        "run_name": f"{MANEUVER}_medium",
        "parameter_changes": {
            "SuspF.Damp_Push.Amplify": 1.5,
            "SuspF.Damp_Pull.Amplify": 1.5,
            "SuspR.Damp_Push.Amplify": 1.5,
            "SuspR.Damp_Pull.Amplify": 1.5
        }
    },
    {
        "run_name": f"{MANEUVER}_hard",
        "parameter_changes": {
            "SuspF.Damp_Push.Amplify": 2.5,
            "SuspF.Damp_Pull.Amplify": 2.5,
            "SuspR.Damp_Push.Amplify": 2.5,
            "SuspR.Damp_Pull.Amplify": 2.5
        }
    }
]