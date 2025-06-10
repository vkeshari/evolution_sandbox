from enum import Enum

from metrics import fitness as fit

# Common params

class EvolutionStrategy(Enum):
  # Binary code in description represents:
  #   restrict crossover (to group),
  #   restrict assignment (to group),
  #   group individuals by assignment
  #     (only to aid crossover and visualization),
  #     NUM_GROUPS must be the same as NUM_ASSIGNMENTS if this setting is enabled.
  # e.g. CROSSOVER_BY_ASSIGNMENT_ONLY groups individuals by assignment, then restricts crossover
  #   to those groups, effectively restricting crossover by assignment.

  # 000 -- no restrictions of any kind. Null/baseline result.
  NO_RESTRICTIONS = 0

  # 001 -- same results as NO_RESTRICTIONS, useful for debugging and visualization only.
  NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT = 1

  # 100 -- split population into groups, restrict crossover to within each group.
  CROSSOVER_BY_GROUP_ONLY = 2

  # 101 -- restrict crossover only with other individuals with the same assignment.
  CROSSOVER_BY_ASSIGNMENT_ONLY = 3

  # 111 -- both of the above restrictions.
  ALL_RESTRICTIONS = 4

class AssignmentStrategy(Enum):
  # Assign individuals to assignments greedily based on assignment priority.
  #   By default, assignment priority is highest to lowest for assignments 0 to NUM_ASSIGNMENTS - 1,
  #   The priority order can be randomized in each generation with RANDOMIZE_ASSIGNMENT_PRIORITIES.
  ASSIGNMENT_PRIORITY = 0

  # Assign individuals to assignments using the assignment matching algorithm.
  #   The cost of assigning individual i to assignment a is 1 - (i's fitness for a)
  ASSIGNMENT_MATCHING = 1

# Params for evolution_runner.py

class WorldParams:
  # Average over these many runs.
  NUM_RUNS = 100
  # Run evolution for these many iterations (per run).
  NUM_GENERATIONS = 100

  # Evolution strategy for crossover and assignment as defined above.
  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS

  # Strategy for assignment of individuals to tasks as defined above.
  ASSIGNMENT_STRATEGY = AssignmentStrategy.ASSIGNMENT_MATCHING

  # Change the priority of assignments every iteration.
  #   Only applicable if AssignmentStrategy is ASSIGNMENT_PRIORITY.
  RANDOMIZE_ASSIGNMENT_PRIORITIES = False
  # Change the no. of available spots for each assignment to a random value in every iteration,
  # Each assignment will have at least half the default no. of available spots,
  #   (by default, all assignments have the same no. of available spots).
  RANDOMIZE_ASSIGNMENT_SIZES = False

class PopulationParams:
  # Total no. of individuals in the population.
  POPULATION_SIZE = 100

  # Total no. of graoups and assignments available.
  # These should be the same unless using an evolution strategy that doesn't group by assignment.
  NUM_GROUPS = 5
  NUM_ASSIGNMENTS = 5

class FitnessParams:
  # Record the time to reach these fitness levels.
  TIME_TO_FITNESS_VALUES = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99]

class AggregationParams:
  # When aggragating over multiple runs, use this metric for fitness.
  FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  # When aggragating over multiple runs, use this metric for time to reach fitness levels
  #   defined above.
  TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

class CrossoverParams:
  # Specifics of crossover (do not touch)
  CROSSOVER_BETA_PARAM = 2.5
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

class DebugParams:
  # Periodically show no. of completed parallel runs
  SHOW_RUN_STATUS = True
  # Time in seconds to wait between showing runs
  SHOW_RUN_STATUS_DELAY = 1
  # Show average and median runtime of each run
  SHOW_RUN_TIME_SUMMARY = True

  # Show iteration no. and fitness at checkpoints during a run.
  SHOW_ITERATIONS = False
  # Show these many checkpoints during a run.
  NUM_CHECKPOINTS = 10
  # Save graphs of full population genomes at every checkpoint.
  SAVE_GENOMES_AT_CHECKPOINTS = False

  # Show final genomes of the entire population at the end of a run.
  SHOW_RUN_GENOMES = False
  # Show fitness for the entire population at the end of a run.
  SHOW_RUN_FITNESS = False
  # Also show above stats at each checkpoint (super verbose, for debugging).
  SHOW_STATS_AT_CHECKPOINTS = False

  # After all runs, show a summary of aggregated population metrics.
  SHOW_AGGREGATED_FITNESS = False
  # Write aggregated population metrics above to a file in data/
  #   (filename is generated based on datetime and above parameters).
  # Writing this data is required for creating graphs in DataViewer.
  WRITE_AGGREGATED_FITNESS = True

# Params for data_viewer.py

class DataViewerParams:
  # The date and time when the script to generate data was run
  #   (not the time at which it was actually stored).
  # By default, this is for the sample data found under data/ and out/
  DATETIME_STRING = '20250608012047'

  # Same as for evolution_runner.py
  POPULATION_SIZE = 100
  NUM_GROUPS = 5
  NUM_ASSIGNMENTS = 5
  NUM_RUNS = 100
  NUM_ITERATIONS = 100

  # Same as for evolution_runner.py
  #   Ignored depending on GraphTypes and GraphParams.ALL_GRAPHS below.
  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS
  RANDOMIZE_ASSIGNMENT_PRIORITIES = False
  RANDOMIZE_ASSIGNMENT_SIZES = False

class GraphTypes:
  # Plot by evolution strategy (4 keys) (same assignment randomization).
  BY_EVOLUTION_STRATEGY = True
  # Plot by assignment randomization (4 keys) (same evolution strategy).
  BY_ASSIGNMENT_RANDOMIZATION = True
  # Plot by assignment (NUM_ASSIGNMENTS keys)
  #   (same evolution strategy and assignment randomization),
  # Very unreadable for large no. of assignments.
  BY_ASSIGNMENT = False

class GraphParams:
  # Plot the time taken to reach these fitness values.
  TIME_TO_FITNESS_VALUES = [0.8, 0.9, 0.95]
  # Only show these many iterations in graph.
  MAX_ITERATIONS = 100
  # Fit an exponential curve to each series in graph.
  #   Not recommended: Fitness data over time does not seem to follow an exponential series.
  FIT_CURVE = False

  # Show graphs (UI)
  SHOW_GRAPHS = False
  # Save graphs to out/ (filename is generated based on above parameters)
  SAVE_GRAPHS = True
  # Iterate over all variations (4 + 4) of the graph type (described as 'same' under GraphTypes)
  ALL_GRAPHS = True

# Params for multi_param_run.py
# All other params above are ignored or modified

class MultiParams:
  # Use these to generate graphs from saved fitness history data
  CUSTOM_DATETIME_STRING = ''
  GRAPHS_ONLY = False
  
  ASSIGNMENT_STRATEGY = AssignmentStrategy.ASSIGNMENT_MATCHING

  POPULATION_SIZE = 100
  NUM_ASSIGNMENTS = 5
  NUM_RUNS = 100
  NUM_ITERATIONS = 100
  GRAPH_MAX_ITERATIONS = 100
  
  SHOW_RUN_STATUS_DELAY = 1
  TIME_TO_FITNESS_VALUES = [0.8, 0.9, 0.95]

# Params for tuning_run.py
# All other params above are ignored or modified

class TuningParams:
  # Use these to generate graphs from saved fitness history data
  CUSTOM_DATETIME_STRING = ''
  GRAPHS_ONLY = False

  NUM_RUNS = 10
  NUM_ITERATIONS = 100

  EVOLUTION_STRATEGY_VALS = [EvolutionStrategy.ALL_RESTRICTIONS,
                              EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY,
                              EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY]
  RANDOM_ASSIGNMENT_PRIORITIES_VALS = [False]
  RANDOM_ASSIGNMENT_SIZES_VALS = [False, True]
  ASSIGNMENT_STRATEGY = AssignmentStrategy.ASSIGNMENT_MATCHING

  MIN_POPULATION = 100
  MAX_POPULATION = 600
  POPULATION_STEP = 100

  MIN_GROUP_SIZE = 10
  MAX_GROUP_SIZE = 60
  GROUP_SIZE_STEP = 5

  FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

  TIME_TO_FITNESS_VALUES = [0.8, 0.9, 0.95]
  PLOT_TIME_TO_FITNESS = 0.9

  # If this is False, NUM_ASSIGNMENTS below is ignored.
  # If this is True, EVOLUTION_STRATEGY_VALS must only have one value:
  #   EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY
  DIFFERENT_GROUP_AND_ASSIGNMENT_COUNT = False
  NUM_ASSIGNMENTS = 20

# Params for ga_tuning_run.py
# All other params above are ignored or modified

class GATuningParams:
  # Use these to generate graphs from saved fitness history data
  CUSTOM_DATETIME_STRING = ''
  GRAPHS_ONLY = False

  NUM_RUNS = 10
  NUM_ITERATIONS = 100

  RANDOM_ASSIGNMENT_PRIORITIES_VALS = [False]
  RANDOM_ASSIGNMENT_SIZES_VALS = [False, True]
  ASSIGNMENT_STRATEGY = AssignmentStrategy.ASSIGNMENT_MATCHING
  
  POPULATION_SIZE = 300

  MIN_GA = 10
  MAX_GA = 30
  GA_STEP = 5

  FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

  TIME_TO_FITNESS_VALUES = [0.8, 0.9, 0.95]
  PLOT_TIME_TO_FITNESS = 0.9
