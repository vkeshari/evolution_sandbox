from enum import Enum

from metrics import fitness as fit

# Common params

class EvolutionStrategy(Enum):
  NO_RESTRICTIONS = 0                      #000
  NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT = 1  #001
  CROSSOVER_BY_GROUP_ONLY = 2              #100
  CROSSOVER_BY_ASSIGNMENT_ONLY = 3         #101
  ALL_RESTRICTIONS = 4                     #111

# Params for main.py

class LoopParams:
  MULTI_PARAMS = False

class WorldParams:
  NUM_RUNS = 10
  NUM_GENERATIONS = 100

  # These are ignored if LoopParams.MULTI_PARAMS
  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS
  RANDOMIZE_ASSIGNMENT_PRIORITIES = True
  RANDOMIZE_ASSIGNMENT_SIZES = True

class PopulationParams:
  POPULATION_SIZE = 100
  NUM_GROUPS = 10
  NUM_ASSIGNMENTS = 10

class AggregationParams:
  FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

class FitnessParams:
  TIME_TO_FITNESS_VALUES = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99]

class CrossoverParams:
  CROSSOVER_BETA_PARAM = 2.5
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

class DebugParams:
  SHOW_ITERATIONS = False
  NUM_CHECKPOINTS = 10

  SHOW_RUN_GENOMES = False
  SHOW_RUN_FITNESS = False
  SHOW_STATS_AT_CHECKPOINTS = False

  SHOW_AGGREGATED_FITNESS = False
  WRITE_AGGREGATED_FITNESS = False

# Params for data_viewer.py

class DataViewerParams:
  POPULATION_SIZE = 100
  NUM_ASSIGNMENTS = 10
  NUM_RUNS = 10
  NUM_ITERATIONS = 100
  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS
  RANDOMIZE_ASSIGNMENT_PRIORITIES = True
  RANDOMIZE_ASSIGNMENT_SIZES = True
  DATETIME_STRING = ''

class GraphParams:
  MAX_ITERATIONS = 100
  TIME_TO_FITNESS_VALUES = [0.9, 0.95, 0.99]
