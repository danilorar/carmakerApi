import cmapi
from cmapi import Project, Runtime, Variation

from cmConfig import PROJECT_PATH, TESTRUN_PATH, VEHICLE_PATH, CASES
from cmSimulate import modify_veh_param

SELECTED_CASE = "front_rear_combo"

def get_case_by_name(case_name):
    for case in CASES:
        if case["run_name"] == case_name:
            return case
    raise ValueError(f"Case '{case_name}' not found")

class VisualExecutionPolicy(cmapi.VariationExecutionPolicyInteractive):
    @classmethod
    async def run_variation(cls, variation):
        run_name = variation.get_name()
        simcontrol = variation.get_simcontrol()

        print(f"[{run_name}] Preparing visual run")

        try:
            descriptions = variation.get_resource_descriptions()

            carmaker = None
            for desc in descriptions:
                if desc.type == cmapi.ResourceType.CarMaker:
                    carmaker = desc.resource
                    print(f"[{run_name}] Found CarMaker resource: {desc.name}")
                    break

            if carmaker is None:
                raise ValueError("No CarMaker resource found")

            movie = cmapi.IPGMovie()
            movie.set_host(cmapi.get_hostname())

            movie.attach_to_cm(carmaker)
            print(f"[{run_name}] IPGMovie attached")

            await movie.start()
            print(f"[{run_name}] IPGMovie started")

        except Exception as e:
            print(f"[{run_name}] IPGMovie setup failed: {e}")

        await simcontrol.start_sim()
        print(f"[{run_name}] Simulation started")

        await simcontrol.await_condition(simcontrol.simstate.condition_finished)
        print(f"[{run_name}] Simulation finished")


async def main():
    Project.load(PROJECT_PATH)
    print(f"Loaded Project: {PROJECT_PATH}")

    case = get_case_by_name(SELECTED_CASE)
    run_name = case["run_name"]
    parameter_changes = case["parameter_changes"]

    print(f"Selected visual case: {run_name}")

    testrun = Project.instance().load_testrun_parametrization(TESTRUN_PATH)
    vehicle = Project.instance().load_vehicle_parametrization(VEHICLE_PATH)

    for parameter_name, new_value in parameter_changes.items():
        modify_veh_param(vehicle, parameter_name, new_value)

    testrun.set_parameter_value("Vehicle", vehicle)

    variation = Variation.create_from_testrun(testrun.clone())
    variation.set_name(run_name)
    variation.set_execution_policy(VisualExecutionPolicy)

    runtime = Runtime.create_default_runtime()

    pool = cmapi.StaticConfigResourcePoolCarMaker()
    pool.set_app_nodes([
        cmapi.AppNode.create(cmapi.get_hostname(), 0, 1)
    ])
    runtime.set_resourcepool(cmapi.ResourceType.CarMaker, pool)

    await runtime.queue_variation(variation)

    print("Starting visual runtime")
    await runtime.start()
    await runtime.wait_until_completed()
    await runtime.stop()
    print("Visual runtime stopped")


if __name__ == "__main__":
    cmapi.Task.run_main_task(main())