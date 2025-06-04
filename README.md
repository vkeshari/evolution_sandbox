# evolution_sandbox

> **Note:** You must attribute references to this or any derivative work to the original author.

### Where things are

+ `src/params.py` : All config lives here. Treat this as command-line params.
+ `data/`         : Metrics from runs are stored here in binary format
+ `out/`          : Graphs made from above data are stored here as PNG images

Sample data and graphs available in `data/` and `out/` (run with the following parameters):
```
POPULATION_SIZE = 100
NUM_ASSIGNMENTS = 5
NUM_GENERATIONS = 100
NUM_RUNS        = 10
```

### To Run

+ `$python3 src/main.py`        : Generates data from simulation
+ `$python3 src/data_viewer.py` : Generates graphs from data
