import cmapi
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# Vehicle and Test run path without hardcode into cmConfig
def select_file(title: str, initial_dir: Path) -> Path:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    selected = filedialog.askopenfilename(
        title=title,
        initialdir=str(initial_dir)
    )

    root.destroy()

    if not selected:
        raise RuntimeError(f"No file selected for: {title}")

    print(f"{title}: {selected}")

    return Path(selected)

# Start IPGMovie and attach to CarMaker instance in the variation
async def start_ipgMovie(variation):
    run_name = variation.get_name()

    descriptions = variation.get_resource_descriptions()

    carmaker = None
    for desc in descriptions:
        if desc.type == cmapi.ResourceType.CarMaker:
            carmaker = desc.resource
            print(f"[{run_name}] Found CarMaker resource: {desc.name}")
            break

    if carmaker is None:
        raise RuntimeError(f"[{run_name}] No CarMaker resource found")

    movie = cmapi.IPGMovie()
    movie.set_host(cmapi.get_hostname())

    movie.attach_to_cm(carmaker)
    print(f"[{run_name}] IPGMovie attached")

    await movie.start()
    print(f"[{run_name}] IPGMovie started")

    return movie
