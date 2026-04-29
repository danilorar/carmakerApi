Short "replica" of Ipg's Test Manager in Python

## Files

* `cmConfig.py`
  Shared configuration, signal definitions, and case definitions.

* `cmSimulate.py`
  Runs CarMaker simulations in sweep or batch mode and saves CSV logs.

* `cmPlot.py`
  Post-processes saved CSV logs and plots selected signals.

* `cmPlotRT.py`
  Realtime plotting tool for simulations started manually from the CarMaker GUI.

* `inspect/`
  Helper scripts for reading vehicle and TestRun parameters.

## Workflow

1. Configure signals and cases in `cmConfig.py`
2. Run simulations with `cmSimulate.py`
3. Compare results with `cmPlot.py`
