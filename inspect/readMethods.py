from pathlib import Path
import cmapi
from cmapi import Project

PROJECT_PATH = Path("/home/danilo/Desktop/cth/vd-control/cm-vd")
TESTRUN_PATH = Path("/opt/ipg/carmaker/linux64-14.1.1/Data/TestRun/Examples/VehicleDynamics/Handling/Slalom18m")
VEHICLE_PATH = Path("/opt/ipg/carmaker/linux64-14.1.1/Data/Vehicle/Examples/Demo_Tesla_Y")
TARGET_TYPE = "vehicle"   # "vehicle" or "testrun"


def load_target():
    if TARGET_TYPE == "vehicle":
        target = Project.instance().load_vehicle_parametrization(VEHICLE_PATH)
        print(f"Loaded vehicle parametrization: {VEHICLE_PATH}")
        return target

    elif TARGET_TYPE == "testrun":
        target = Project.instance().load_testrun_parametrization(TESTRUN_PATH)
        print(f"Loaded testrun parametrization: {TESTRUN_PATH}")
        return target
    else:
        raise ValueError(f"Unsupported TARGET_TYPE: {TARGET_TYPE}")


async def main():
    # Load CarMaker project first
    Project.load(PROJECT_PATH)
    print(f"Loaded project: {PROJECT_PATH}")
    print()

    # Load chosen object
    target = load_target()
    print()

    # Print available public methods / attributes
    print(f"Available methods / attributes for {TARGET_TYPE}:")
    for name in dir(target):
        if not name.startswith("_"):
            print(name)


if __name__ == "__main__":
    cmapi.Task.run_main_task(main())