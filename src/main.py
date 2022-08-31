import sys
from enum import Enum

from containers import population as pop
from evolution import crossover as crs
from evolution import assignment as ass
from evolution import world as wrd
from metrics import fitness as fit

class DebugParams:
  SHOW_ITERATIONS = False
  NUM_CHECKPOINTS = 10

  SHOW_RUN_GENOMES = False
  SHOW_RUN_FITNESS = False

  SHOW_AGGREGATED_FITNESS = True

class PopulationParams:
  POPULATION_SIZE = 100
  NUM_GROUPS = 10
  NUM_ASSIGNMENTS = 10

class EvolutionStrategy(Enum):
  NO_RESTRICTIONS = 0                      #000
  NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT = 1  #001
  CROSSOVER_BY_GROUP_ONLY = 2              #100
  CROSSOVER_BY_ASSIGNMENT_ONLY = 3         #101
  ALL_RESTRICTIONS = 4                     #111

class WorldParams:
  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS
  NUM_GENERATIONS = 100
  NUM_RUNS = 10
  RANDOMIZE_ASSIGNMENT_PRIORITIES = True
  RANDOMIZE_ASSIGNMENT_SIZES = True

class AggregationParams:
  FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

class FitnessParams:
  TIME_TO_FITNESS_VALUES = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99]

class CrossoverParams:
  CROSSOVER_BETA_PARAM = 2.5
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

def get_evolution_constraints():
  restrict_crossover = WorldParams.EVOLUTION_STRATEGY in [EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY,
                                                          EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                                          EvolutionStrategy.ALL_RESTRICTIONS]
  restrict_assignment = WorldParams.EVOLUTION_STRATEGY == EvolutionStrategy.ALL_RESTRICTIONS
  group_by_assignment = WorldParams.EVOLUTION_STRATEGY in [EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT,
                                                            EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                                            EvolutionStrategy.ALL_RESTRICTIONS]
  return (restrict_crossover, restrict_assignment, group_by_assignment)                                        

def validate_params():
  assert (PopulationParams.NUM_GROUPS > 0)
  assert (PopulationParams.NUM_GROUPS == PopulationParams.NUM_ASSIGNMENTS)
  assert (PopulationParams.POPULATION_SIZE > PopulationParams.NUM_GROUPS)
  assert (PopulationParams.POPULATION_SIZE % PopulationParams.NUM_GROUPS == 0)
  assert (PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS > 2.0)

def initialize_world():
  (restrict_crossover, restrict_assignment, group_by_assignment) = get_evolution_constraints()

  group_size = int(PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS)
  initial_assignment_priorities = range(group_size)
  initial_assignment_sizes = [group_size] * PopulationParams.NUM_GROUPS

  p = pop.Population(population_size = PopulationParams.POPULATION_SIZE,
                      num_groups = PopulationParams.NUM_GROUPS,
                      genome_size = PopulationParams.NUM_ASSIGNMENTS,
                      assignment_priorities = initial_assignment_priorities,
                      assignment_sizes = initial_assignment_sizes)

  a = ass.Assignment(restrict_assignment = restrict_assignment,
                      group_by_assignment = group_by_assignment)
  a.update_assignments(population = p)

  c = crs.Crossover(crossover_beta_param = CrossoverParams.CROSSOVER_BETA_PARAM,
                    mutation_rate = CrossoverParams.MUTATION_RATE,
                    interpolate_genes = CrossoverParams.INTERPOLATE_GENES)

  f = fit.FitnessHistory(time_to_fitness_values = FitnessParams.TIME_TO_FITNESS_VALUES, genome_size = PopulationParams.NUM_ASSIGNMENTS)

  w = wrd.World(initial_population = p,
                assignment = a,
                crossover = c,
                fitness_history = f,
                num_generations = WorldParams.NUM_GENERATIONS,
                restrict_crossover = restrict_crossover,
                randomize_assignment_priorities = WorldParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                randomize_assignment_sizes = WorldParams.RANDOMIZE_ASSIGNMENT_SIZES)
  return w

def main():
  args = sys.argv[1:]
  validate_params()

  print("Evolution Strategy: {}".format(WorldParams.EVOLUTION_STRATEGY))
  print("Fitness Aggregation: {}".format(AggregationParams.FITNESS_AGGREGATION_TYPE))
  print("Time Aggregation: {}".format(AggregationParams.TIME_AGGREGATION_TYPE))
  all_fitness_history = {}
  for r in range(WorldParams.NUM_RUNS):
    w = initialize_world()
    print ("RUN: {}\tITERATIONS: {}".format(r + 1, w.num_generations))

    w.evolve(show_iterations = DebugParams.SHOW_ITERATIONS,
              show_every_n_iteration = int(WorldParams.NUM_GENERATIONS / DebugParams.NUM_CHECKPOINTS),
              show_final_genomes = DebugParams.SHOW_RUN_GENOMES,
              show_final_fitness = DebugParams.SHOW_RUN_FITNESS)
    all_fitness_history[r + 1] = w.fitness_history

  aggregate_fitness_history = fit.FitnessHistoryAggregate.get_aggregated_fitness(all_fitness_history,
                                                                                  fitness_aggregate_type = AggregationParams.FITNESS_AGGREGATION_TYPE,
                                                                                  time_to_aggregate_type = AggregationParams.TIME_AGGREGATION_TYPE)
  if DebugParams.SHOW_AGGREGATED_FITNESS:
    print("\nFINAL METRICS\n")
    aggregate_fitness_history.history['iterations'][WorldParams.NUM_GENERATIONS].print_fitness_data()
    print()
    aggregate_fitness_history.print_time_to()

if __name__=="__main__":
  main()
