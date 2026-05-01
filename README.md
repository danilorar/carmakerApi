Python utilities for running repeated [IPG CarMaker](https://ipg-automotive.com/en/products-solutions/software/ipg-carmaker/) Simulations
similar to IPG's Test Manager.

```text
configure → run cases/sweeps → save CSV logs → plot results
```

---

## 📁 Main Scripts

| File | Purpose |
|---|---|
| `cmConfig.py` | Configure project path, TestRun, Vehicle, signals, and cases |
| `cmSimulate.py` | Run simulations |
| `cmPlot.py` | Plot saved CSV results |
| `cmPlotRt.py` | Plot live signals from a GUI-started simulation |
| `cmHelpers.py` | Shared helper functions |
| `inspect/` | Parameter/API inspection scripts |
| `logs/` | Generated CSV outputs |

---

## 🚦 Run Modes

Run modes are selected in:

```text
cmpython/cmSimulate.py
```

| Mode | Description |
|---|---|
| `cases` | Run all cases defined in `cmConfig.py`. Can run in parallel. |
| `sequential` | Run the same cases one after another. Good for debugging and IPGMovie. |
| `sweep` | Run predefined values for one selected parameter. |

Parallel execution is controlled with:

```text
MAX_PARALLEL_CARMAKERS
```

---

## ⚙️ Simulation Setup

Most setup is done in:

```text
cmpython/cmConfig.py
```

Configure:

```text
PROJECT_PATH    CarMaker project path
TESTRUN_PATH    selected TestRun file
VEHICLE_PATH    selected Vehicle file
SIGNALS         DVA signals to save
CASES           simulation variants
```

The file selectors start from:

```text
Data/TestRun
Data/Vehicle
```

The workflow currently focuses on **Vehicle parameter changes**. Full TestRun configuration from Python is not implemented yet.

---

## 🎥 IPGMovie

`cmSimulate.py` can optionally start IPGMovie during scripted runs.

Recommended setup:

```text
RUN_MODE = "sequential"
ENABLE_IPG_MOVIE = True
```

For normal batch/data runs, keep IPGMovie disabled.

---

## 📊 Output and Plotting

Simulation results are saved as CSV files in:

```text
cmpython/logs/
```

Example outputs:

```text
baseline.csv
front_spring_5000.csv
rear_spring_6000.csv
front_rear_combo.csv
```

Use `cmPlot.py` to plot and compare saved CSV results.

```text
cmSimulate.py → logs/*.csv → cmPlot.py
```

---

## 📡 Runtime Plotting

`cmPlotRt.py` is for live plotting.

Current workflow:

```text
Run cmPlotRt.py in parallel
        ↓
Run cmPlotRt.py in parallel
        ↓
Plot selected signals while simulation is running
```

---

## 🔎 Parameter Inspection

Use the scripts in:

```text
cmpython/inspect/
```

to inspect available CarMaker parameters and API methods.

Useful when defining parameter changes in `cmConfig.py`.

---

## ▶️ Basic Usage

From inside `cmpython/`:

```bash
PYTHONPATH=/opt/ipg/carmaker/linux64-14.1.1/Python/python3.12 python3.12 cmSimulate.py
```

Adjust the CarMaker version path if needed.

---


## 🚧 Future Improvements

- auto-generate plots after runs
- improve TestRun configuration
- add command-line options for run mode and visualization