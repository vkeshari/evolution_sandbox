# evolution_sandbox

> [!IMPORTANT]
> You must attribute references to this or any derivative work to the original author.

The Evolution Sandbox simulates and compares strategies for optimal evolution in a population with specialization of labor.

### Where things are

+ `src/params.py` : All config lives here. Treat this as command-line params.
+ `data/`         : Metrics from runs are stored here in binary format
+ `out/`          : Graphs made from above data are stored here as PNG images

Sample data and graphs available in `data/` and `out/` respectively.
> Sample generated with the following parameters:
> ```
> POPULATION_SIZE = 100
> NUM_ASSIGNMENTS = 5
> NUM_GENERATIONS = 100
> NUM_RUNS        = 10
> ```

### To Run

> [!NOTE]
> Start here. This wrapper runs simulations for variations of multiple parameters and generates graphs for comparison between them.
> 
> `$python3 src/multi_param_run.py`
  
#### Debugging and targeted scripts
+ `$python3 src/evolution_runner.py` : Generates data from simulation
+ `$python3 src/data_viewer.py`      : Generates graphs from data

### Parameter tuning scripts
+ `$python3 src/tuning_run.py`      : Compares various combinations of population and group sizes.
