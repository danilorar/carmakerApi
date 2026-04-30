from pathlib import Path
import asyncio
import csv
import sys
import time
import math 
import subprocess

import cmapi 
from cmapi import Project, Runtime, Variation
from cmConfig import PROJECT_PATH, TESTRUN_PATH, VEHICLE_PATH, SIGNALS, CASES

# ======= User defined parameters =======

# check params with readParams.py
READ_PARAMS =False
READ_MODE = "vehicle" # or "testrun"

# parameter change 
MAX_PARALLEL_CARMAKERS = 3
RUN_MODE = "cases"  # "sweep" or "cases" or "sequential"
MOVIE = False

# set params to sweep
# cm API
SWEEP_PARAMETER = {
   "SuspF.Spring": [
        [[0.0, 0.0], [0.1, 3000.0], [1.0, 30000.0]], # case 1 
        [[0.0, 0.0], [0.1, 6000.0], [1.0, 60000.0]], # case 2
        [[0.0, 0.0], [0.1, 9000.0], [1.0, 90000.0]], # case 3  
    ]
} 

# ======= Helper functions =======

# modify one vehicle parameter
def modify_veh_param(vehicle, parameter_name, new_value): 
    if parameter_name not in vehicle.params_by_key:
        raise ValueError(f"{parameter_name} not found")
    
    old_value = vehicle.get_parameter_value(parameter_name)
    vehicle.set_parameter_value(parameter_name, new_value)
    updated_value = vehicle.get_parameter_value(parameter_name)
    
    print(f"{parameter_name} old: {old_value}, new: {updated_value}")
    
# save data in csv    
def save_csv(signal_rows, run_name): 
    csv_path = PROJECT_PATH / "cmpython" / "logs" / f"{run_name}.csv" # save in /logs
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([label for _, label, _ in SIGNALS])
        writer.writerows(signal_rows)
    print(f"Saved to {csv_path}")
    
    
# ======= Execution policy =======
#(from cmapi example)

class DVAExecutionPolicy(cmapi.VariationExecutionPolicyInteractive):
    @classmethod
    async def run_variation(cls, variation):
        simcontrol = variation.get_simcontrol() # simcontrol tied to variation
        run_name = variation.get_name() # save name to csv after
        signal_rows = [] # signal storage
        
        # start simulation
        
        wall_start = time.time()
        print(f"Starting simulation for {run_name}")
        await simcontrol.start_sim()
        
        started_logging = False
        
        # detects when simulations is stopped or reset
        last_time = None
        frozen_count = 0
        
    
        # main loop
        while True: 
            # read time
            current_time, = await simcontrol.simio.dva_read_async("Time")

            # wait until sim really starts
            if not started_logging: 
                if current_time > 0.0: 
                    started_logging = True
                else: 
                    await asyncio.sleep(0.05)
                    continue
                
            # read SIGNALS 
            row = []
            for name, label, convert in SIGNALS:
                raw_value, = await simcontrol.simio.dva_read_async(name)
                row.append(convert(raw_value)) # append to list converted signal
                
            signal_rows.append(row) # save in row list and print
            # print(
            #     " | ".join(
            #         f"{SIGNALS[k][1]}: {row[k]:.3f}"
            #         for k in range(len(SIGNALS))
            #     )
            # )
            
            # end conditions:
            # 1. time reset backwards 2. time stopped advancing for too long
            if last_time is not None:
                if current_time < last_time:
                    print("Detected time reset. Ending log.")
                    break

                if abs(current_time - last_time) < 1e-9:
                    frozen_count += 1
                else:
                    frozen_count = 0

            last_time = current_time

            if frozen_count > 20:
                print("Simulation time stopped advancing. Ending log.")
                break

            await asyncio.sleep(0.01)
        
        # save in csv 
        save_csv(signal_rows, run_name)

        wall_end = time.time()
        # print(f"[{run_name}] ELAPSED = {wall_end - wall_start:.3f} s") # delta time
        
        
# ======= Main loop =======

async def main(): 
    
    # trigger vehParam list if true
    if READ_PARAMS:
         subprocess.run([sys.executable, "inspect/readParams.py", READ_MODE],check=True)
         return
    
    # to allocate pool = 1 when sequential
    if RUN_MODE == "sequential":
        max_parallel = 1
    else:
        max_parallel = MAX_PARALLEL_CARMAKERS
    
    # load project, runtime
    Project.load(PROJECT_PATH)
    runtime = Runtime.create_default_runtime()
    
    # create pool for parallel simulation (from cmapi doc)
    pool = cmapi.StaticConfigResourcePoolCarMaker()
    pool.set_app_nodes([cmapi.AppNode.create(cmapi.get_hostname(), 0, max_parallel)])
    runtime.set_resourcepool(cmapi.ResourceType.CarMaker, pool)
    print(f"Configured CM resource pool with max parallel: {max_parallel}")
    
    # sequential or cases
    if RUN_MODE in ["sequential", "cases"]:
        for case in CASES: 
            run_name = case["run_name"]
            parameter_changes = case["parameter_changes"]
            
            print(f"\nPreparing {RUN_MODE} case: {run_name}")
            
            testrun = Project.instance().load_testrun_parametrization(TESTRUN_PATH)
            vehicle = Project.instance().load_vehicle_parametrization(VEHICLE_PATH)
            
            try: 
                for parameter_name, new_value in parameter_changes.items():
                    modify_veh_param(vehicle, parameter_name, new_value)
            except ValueError as e:
                print(e)
                return
            
            # put modified vehicle into the testrun
            testrun.set_parameter_value("Vehicle", vehicle)
            
            # create variation from modified Testrun 
            variation = Variation.create_from_testrun(testrun.clone())
            variation.set_name(run_name)
            
            variation.set_execution_policy(DVAExecutionPolicy)
            await runtime.queue_variation(variation)
            
            
    # sweep mode
    elif RUN_MODE == "sweep": 
        for parameter_name, values in SWEEP_PARAMETER.items(): 
            for idx, value in enumerate(values, start=1): 
                
                testrun = Project.instance().load_testrun_parametrization(TESTRUN_PATH)
                vehicle = Project.instance().load_vehicle_parametrization(VEHICLE_PATH)
                print(f"\nPreparing case for {parameter_name} = {value}")
                
                try: 
                    modify_veh_param(vehicle, parameter_name, value)
                except ValueError as e: 
                    print(e)
                    return
                
                # put modified vehicle into the testrun
                testrun.set_parameter_value("Vehicle", vehicle)
                
                # name in saved csv 
                short_param = parameter_name.replace(".", "_")
                case_name = f"{short_param}_case_{idx}"
                
                # create variation from modified Testrun 
                variation = Variation.create_from_testrun(testrun.clone())
                variation.set_name(case_name)
                
                variation.set_execution_policy(DVAExecutionPolicy)
                await runtime.queue_variation(variation)
                
    else:
        raise ValueError(f"Unsupported RUN_MODE: {RUN_MODE}")

    overall_start = time.time()
    await runtime.start()
    
    await runtime.wait_until_completed()
    print("\nRun(s) completed")

    await runtime.stop()
    print("Runtime stopped")

    overall_end = time.time()
    print(f"\nOVERALL SIMULATION TIME  = {overall_end - overall_start:.3f} s")


# Entry point of the script
if __name__ == "__main__":
    cmapi.Task.run_main_task(main())