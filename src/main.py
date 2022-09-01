import datetime
import sys
from enum import Enum

from containers import population as pop
from evolution import crossover as crs
from evolution import assignment as ass
from evolution import world as wrd
from metrics import fitness as fit
from metrics import dataio as dat

class LoopParams:
  MULTI_PARAMS = True

class DebugParams:
  SHOW_ITERATIONS = False
  NUM_CHECKPOINTS = 10

  SHOW_RUN_GENOMES = False
  SHOW_RUN_FITNESS = False

  SHOW_AGGREGATED_FITNESS = True
  WRITE_AGGREGATED_FITNESS = True

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
  NUM_RUNS = 10
  NUM_GENERATIONS = 100

  EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS  # Ignored if LoopParams.MULTI_PARAMS
  RANDOMIZE_ASSIGNMENT_PRIORITIES = True                  # Ignored if LoopParams.MULTI_PARAMS
  RANDOMIZE_ASSIGNMENT_SIZES = True                       # Ignored if LoopParams.MULTI_PARAMS

class AggregationParams:
  FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

class FitnessParams:
  TIME_TO_FITNESS_VALUES = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99]

class CrossoverParams:
  CROSSOVER_BETA_PARAM = 2.5
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

def get_evolution_constraints(evolution_strategy):
  restrict_crossover = evolution_strategy in [EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY,
                                              EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                              EvolutionStrategy.ALL_RESTRICTIONS]
  restrict_assignment = evolution_strategy == EvolutionStrategy.ALL_RESTRICTIONS
  group_by_assignment = evolution_strategy in [EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT,
                                                EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                                EvolutionStrategy.ALL_RESTRICTIONS]
  return (restrict_crossover, restrict_assignment, group_by_assignment)

def validate_params():
  assert (PopulationParams.NUM_GROUPS > 0)
  assert (PopulationParams.NUM_GROUPS == PopulationParams.NUM_ASSIGNMENTS)
  assert (PopulationParams.POPULATION_SIZE > PopulationParams.NUM_GROUPS)
  assert (PopulationParams.POPULATION_SIZE % PopulationParams.NUM_GROUPS == 0)
  assert (PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS > 2.0)

def initialize_world(population_size, num_iterations, num_assignments,
                      evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes):
  (restrict_crossover, restrict_assignment, group_by_assignment) = get_evolution_constraints(evolution_strategy)

  group_size = int(population_size / PopulationParams.NUM_GROUPS)
  initial_assignment_priorities = range(PopulationParams.NUM_GROUPS)
  initial_assignment_sizes = [group_size] * PopulationParams.NUM_GROUPS

  p = pop.Population(population_size = population_size,
                      num_groups = num_assignments,
                      genome_size = num_assignments,
                      assignment_priorities = initial_assignment_priorities,
                      assignment_sizes = initial_assignment_sizes)

  a = ass.Assignment(restrict_assignment = restrict_assignment,
                      group_by_assignment = group_by_assignment)
  a.update_assignments(population = p)

  c = crs.Crossover(crossover_beta_param = CrossoverParams.CROSSOVER_BETA_PARAM,
                    mutation_rate = CrossoverParams.MUTATION_RATE,
                    interpolate_genes = CrossoverParams.INTERPOLATE_GENES)

  f = fit.FitnessHistory(time_to_fitness_values = FitnessParams.TIME_TO_FITNESS_VALUES, genome_size = num_assignments)

  w = wrd.World(initial_population = p,
                assignment = a,
                crossover = c,
                fitness_history = f,
                num_generations = num_iterations,
                restrict_crossover = restrict_crossover,
                randomize_assignment_priorities = randomize_assignment_priorities,
                randomize_assignment_sizes = randomize_assignment_sizes)
  return w

def run_evolution(fhio, datetime_string,
                  population_size, num_runs, num_iterations, num_assignments,
                  evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes):

  print("Evolution Strategy: {}".format(evolution_strategy))
  print("Randomize Assignment Priorities: {}".format(randomize_assignment_priorities))
  print("Randomize Assignment Sizes: {}".format(randomize_assignment_sizes))
  print("Fitness Aggregation: {}".format(AggregationParams.FITNESS_AGGREGATION_TYPE))
  print("Time Aggregation: {}".format(AggregationParams.TIME_AGGREGATION_TYPE))
  all_fitness_history = {}
  for r in range(num_runs):
    w = initialize_world(population_size, num_iterations, num_assignments,
                          evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes)

    print ("RUN: {}\tITERATIONS: {}".format(r + 1, w.num_generations))
    w.evolve(show_iterations = DebugParams.SHOW_ITERATIONS,
              show_every_n_iteration = int(num_iterations / DebugParams.NUM_CHECKPOINTS),
              show_final_genomes = DebugParams.SHOW_RUN_GENOMES,
              show_final_fitness = DebugParams.SHOW_RUN_FITNESS)
    all_fitness_history[r + 1] = w.fitness_history

  aggregate_fitness_history = fit.FitnessHistoryAggregate.get_aggregated_fitness(all_fitness_history,
                                                                                  fitness_aggregate_type = AggregationParams.FITNESS_AGGREGATION_TYPE,
                                                                                  time_to_aggregate_type = AggregationParams.TIME_AGGREGATION_TYPE)
  if DebugParams.SHOW_AGGREGATED_FITNESS:
    print("\nFINAL METRICS\n")
    aggregate_fitness_history.history['iterations'][num_iterations].print_fitness_data()
    print()
    aggregate_fitness_history.print_time_to()

  if DebugParams.WRITE_AGGREGATED_FITNESS:
    out_filename = "Run_p{}_a{}_r{}_i{}_{}_{}_{}_{}.data".format(population_size, num_assignments, num_runs, num_iterations, 
                                                                  evolution_strategy.name, randomize_assignment_priorities, randomize_assignment_sizes,
                                                                  datetime_string)
    fhio.write_fitness_history(filename = out_filename, fitness_history = aggregate_fitness_history)


def main():
  args = sys.argv[1:]
  validate_params()

  fhio = dat.FitnessHistoryIO()
  datetime_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  if LoopParams.MULTI_PARAMS:
    for evolution_strategy in EvolutionStrategy:
      if evolution_strategy == EvolutionStrategy.NO_RESTRICTIONS:
        continue
      for randomize_assignment_priorities in [False, True]:
        for randomize_assignment_sizes in [False, True]:
          run_evolution(fhio, datetime_string,
                        PopulationParams.POPULATION_SIZE, WorldParams.NUM_RUNS, WorldParams.NUM_GENERATIONS, PopulationParams.NUM_ASSIGNMENTS,
                        evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes)
  else:
    run_evolution(fhio, datetime_string,
                  PopulationParams.POPULATION_SIZE, WorldParams.NUM_RUNS, WorldParams.NUM_GENERATIONS, PopulationParams.NUM_ASSIGNMENTS,
                  WorldParams.EVOLUTION_STRATEGY, WorldParams.RANDOMIZE_ASSIGNMENT_PRIORITIES, WorldParams.RANDOMIZE_ASSIGNMENT_SIZES)

if __name__=="__main__":
  main()
