from enum import Enum

from metrics import fitness as fit

# Common params

class EvolutionStrategy(Enum):
  NO_RESTRICTIONS = 0                      #000 -- no restrictions of any kind. Null/baseline result.
  NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT = 1  #001 -- same results as NO_RESTRICTIONS, useful for debugging only.
  CROSSOVER_BY_GROUP_ONLY = 2              #100 -- split population into groups, restrict crossover within each group.
  CROSSOVER_BY_ASSIGNMENT_ONLY = 3         #101 -- restrict crossover only with other individuals with the same assignment.
  ALL_RESTRICTIONS = 4                     #111 -- both of the above restrictions.

# Params for main.py

class LoopParams:
  # Iterate over 3 categorical params with 16 possible values:
  # Evolution strategy (4 keys) and Assignment randomness (4 keys).
  MULTI_PARAMS = True

class WorldParams:
  # Average over these many runs.
  NUM_RUNS = 100
  # Run evolution for these many iterations (per run).
  NUM_GENERATIONS = 100

  # These are ignored if LoopParams.MULTI_PARAMS is True,
  # Evolution strategy for crossover and assignment as defined above.
  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS
  # Change the priority of assignments every iteration,
  # By default, priority is highest for assignment 0 and decreases by assignment no.
  RANDOMIZE_ASSIGNMENT_PRIORITIES = True
  # Change the no. of available spots for each assignment every iteration,
  # Each assignment has at least half the default no. of availanle spots,
  # By default, all assignments have the same no. of available spots.
  RANDOMIZE_ASSIGNMENT_SIZES = True

class PopulationParams:
  # Total no. of individuals in the population.
  POPULATION_SIZE = 100

  # Total no. of assignments available,
  # An equal no. of groups will be created (but enforced only if restricted by evolution strategy),
  # These should always be the same.
  NUM_GROUPS = 4
  NUM_ASSIGNMENTS = 4

class FitnessParams:
  # Record the time to reach these fitness levels.
  TIME_TO_FITNESS_VALUES = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99]

class AggregationParams:
  # When aggragating over multiple runs, use this metric for fitness.
  FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  # When aggragating over multiple runs, use this metric for time to reach fitness levels defined above.
  TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

class CrossoverParams:
  # Specifics of crossover (do not touch)
  CROSSOVER_BETA_PARAM = 2.5
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

class DebugParams:
  # Show iteration no. and fitness at checkpoints during a run.
  SHOW_ITERATIONS = False
  # Show these many checkpoints during a run.
  NUM_CHECKPOINTS = 10

  # Show final genomes of the entire population at the end of a run.
  SHOW_RUN_GENOMES = False
  # Show fitness for the entire population at the end of a run.
  SHOW_RUN_FITNESS = False
  # Also show above stats at each checkpoint (super verbose, for debugging).
  SHOW_STATS_AT_CHECKPOINTS = False

  # After all runs, show a summary of aggregated population metrics.
  SHOW_AGGREGATED_FITNESS = True
  # Write aggregated population metrics above to a file in data/ (filename is generated based on datetime and above parameters).
  WRITE_AGGREGATED_FITNESS = False

# Params for data_viewer.py

class DataViewerParams:
  # The date and time when the script to generate data was run (not the time at which it was actually stored).
  # By default, this is for the sample data found under data/ and out/
  DATETIME_STRING = '20220905210808'

  # Same as for main.py
  POPULATION_SIZE = 100
  NUM_ASSIGNMENTS = 4
  NUM_RUNS = 100
  NUM_ITERATIONS = 100

  # Same as for main.py, ignored depending on graph type
  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS
  RANDOMIZE_ASSIGNMENT_PRIORITIES = True
  RANDOMIZE_ASSIGNMENT_SIZES = True

class GraphTypes:
  # Plot by evolution strategy (4 keys) (same assignment randomization).
  BY_EVOLUTION_STRATEGY = True
  # Plot by assignment randomization (4 keys) (same evolution strategy).
  BY_ASSIGNMENT_RANDOMIZATION = True
  # Plot by assignment (NUM_ASSIGNMENTS keys) (same evolution strategy and assignment randomization),
  # Very unreadable for large no. of assignments.
  BY_ASSIGNMENT = False

class GraphParams:
  # Plot the time taken to reach these fitness values.
  TIME_TO_FITNESS_VALUES = [0.9, 0.95, 0.99]
  # Only show these many iterations in graph.
  MAX_ITERATIONS = 100
  # Fit an exponential curve to each series in graph.
  FIT_CURVE = False

  # Show graphs (UI)
  SHOW_GRAPHS = True
  # Save graphs to out/ (filename is generated based on above parameters)
  SAVE_GRAPHS = False
  # Iterate over all variations of the graph type (described as 'same' under GraphTypes)
  ALL_GRAPHS = False
