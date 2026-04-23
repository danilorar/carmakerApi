from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cmapi
from cmapi import Project
from cmConfig import PROJECT_PATH, TESTRUN_PATH, VEHICLE_PATH

# read Parameters either using either: 
# vehicle_parametrization or testrun_parametrization or [more]

READ_MODE = "vehicle"
if len(sys.argv) > 1:
    READ_MODE = sys.argv[1].lower()
USER_PARAMETER = "SuspF.Spring"

def load_target_parametrization():
    if READ_MODE == "vehicle": 
        target = Project.instance().load_vehicle_parametrization(VEHICLE_PATH)
        print(f"Loaded vehicle parametrization: {VEHICLE_PATH}")
        return target 
    elif READ_MODE == "testrun":
        target = Project.instance().load_testrun_parametrization(TESTRUN_PATH)
        print(f"Loaded testrun parametrization: {TESTRUN_PATH}")
        return target
    else:
        raise ValueError(f"Unsupported READ_MODE {READ_MODE}")
    
        
async def main(): 
    # load project 
    Project.load(PROJECT_PATH)
    print(f"Loaded Project: {PROJECT_PATH}")
    
    # load target parametrization 
    target =  load_target_parametrization()
    print()
    
    print(f"Available {READ_MODE} keys -> values:") # list all veh or testtun values
    for key in target.params_by_key:
        value = target.get_parameter_value(key)
        print(f"{key} -> {value}")

    # If a specific parameter is requested, print it separately
    if USER_PARAMETER:
        print()

        if USER_PARAMETER not in target.params_by_key:
            print(f"Parameter '{USER_PARAMETER}' not found in {READ_MODE}.")
            return

        value = target.get_parameter_value(USER_PARAMETER)

        print(f"Selected parameter from {READ_MODE}:")
        print(f"Parameter: {USER_PARAMETER}")
        print(f"Value: {value}")
        print()

if __name__ == "__main__":
    cmapi.Task.run_main_task(main())