# evolution_sandbox

> [!IMPORTANT]
> You must attribute references to this or any derivative work to the original author.

The Evolution Sandbox simulates and compares strategies for optimal evolution in a population with specialization of labor.

### Where things are

+ `src/params.py` : All config lives here. Treat this as command-line params.
+ `data/`         : Metrics from runs are stored here in binary format.
+ `out/`          : Graphs made from above data are stored here as PNG images.

Sample data and graphs available in `data/` and `out/` respectively.
> Sample generated with the following parameters:
> ```
> POPULATION_SIZE = 100
> NUM_ASSIGNMENTS = 5
> NUM_GROUPS = 5
> NUM_GENERATIONS = 100
> NUM_RUNS        = 100
> ```

### Key Parameters

#### Evolution Strategies
+ `NO_RESTRICTIONS`             : No restrictions on crossover or assignment (Null/Baseline result)
+ `CROSSOVER_BY_ASSIGNMENT_ONLY`: Crossover restricted to individuals with the same assignment
+ `CROSSOVER_BY_GROUP_ONLY`     : Population divided into groups. Crossover restricted to individuals in the same group, no restrictions on assignment.
+ `ALL_RESTRICTIONS`            : Population divided into groups. Crossover restricted to individuals in the same group, and each group has a pre-determined assignment (Artificial Niches).

#### Assignment Strategies
+ `ASSIGNMENT_PRIORITY`: Tasks have priorities. The best available Individuals are assigned to tasks greedily, highest task priority first.
+ `ASSIGNMENT_MATCHING`: Tasks and individuals are matched using linear sum optimization to achieve the maximum possible population fitness.

#### Assignment Randomization
+ `RANDOMIZE_ASSIGNMENT_PRIORITIES`: If using assignment strategy `ASSIGNMENT_PRIORITY`, the priority of tasks is randomized in every generation.
+ `RANDOMIZE_ASSIGNMENT_SIZES`     : Available slots for each task are randomized in every generation.

### To Run

> [!NOTE]
> Start here. This wrapper runs simulations for variations of multiple parameters and generates graphs for comparison between them.
> 
> `$python3 src/multi_param_run.py`
  
#### Debugging and targeted scripts
+ `$python3 src/evolution_runner.py`: Generates data from simulation
+ `$python3 src/data_viewer.py`     : Generates graphs from data

### Parameter tuning scripts
+ `$python3 src/tuning_run.py`   : Compares various combinations of population and group sizes.
+ `$python3 src/ga_tuning_run.py`: Compares various combinations of assignment and group sizes (only for evolution strategy `CROSSOVER_BY_GROUP_ONLY`)
