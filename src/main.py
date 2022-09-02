import datetime
import sys

from containers import population as pop
from evolution import crossover as crs
from evolution import assignment as ass
from evolution import world as wrd
from metrics import fitness as fit
from metrics import dataio as dat

import params as par

def get_evolution_constraints(evolution_strategy):
  restrict_crossover = evolution_strategy in [par.EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY,
                                              par.EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                              par.EvolutionStrategy.ALL_RESTRICTIONS]
  restrict_assignment = evolution_strategy == par.EvolutionStrategy.ALL_RESTRICTIONS
  group_by_assignment = evolution_strategy in [par.EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT,
                                                par.EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                                par.EvolutionStrategy.ALL_RESTRICTIONS]
  return (restrict_crossover, restrict_assignment, group_by_assignment)

def validate_params():
  assert (par.PopulationParams.NUM_GROUPS > 0)
  assert (par.PopulationParams.NUM_GROUPS == par.PopulationParams.NUM_ASSIGNMENTS)
  assert (par.PopulationParams.POPULATION_SIZE > par.PopulationParams.NUM_GROUPS)
  assert (par.PopulationParams.POPULATION_SIZE % par.PopulationParams.NUM_GROUPS == 0)
  assert (par.PopulationParams.POPULATION_SIZE / par.PopulationParams.NUM_GROUPS > 2.0)

def initialize_world(population_size, num_iterations, num_assignments,
                      evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes):
  (restrict_crossover, restrict_assignment, group_by_assignment) = get_evolution_constraints(evolution_strategy)

  group_size = int(population_size / par.PopulationParams.NUM_GROUPS)
  initial_assignment_priorities = range(par.PopulationParams.NUM_GROUPS)
  initial_assignment_sizes = [group_size] * par.PopulationParams.NUM_GROUPS

  p = pop.Population(population_size = population_size,
                      num_groups = num_assignments,
                      genome_size = num_assignments,
                      assignment_priorities = initial_assignment_priorities,
                      assignment_sizes = initial_assignment_sizes)

  a = ass.Assignment(restrict_assignment = restrict_assignment,
                      group_by_assignment = group_by_assignment)
  a.update_assignments(population = p)

  c = crs.Crossover(crossover_beta_param = par.CrossoverParams.CROSSOVER_BETA_PARAM,
                    mutation_rate = par.CrossoverParams.MUTATION_RATE,
                    interpolate_genes = par.CrossoverParams.INTERPOLATE_GENES)

  f = fit.FitnessHistory(time_to_fitness_values = par.FitnessParams.TIME_TO_FITNESS_VALUES, genome_size = num_assignments)

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
  print("Fitness Aggregation: {}".format(par.AggregationParams.FITNESS_AGGREGATION_TYPE))
  print("Time Aggregation: {}".format(par.AggregationParams.TIME_AGGREGATION_TYPE))
  all_fitness_history = {}
  for r in range(num_runs):
    w = initialize_world(population_size, num_iterations, num_assignments,
                          evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes)

    print ("RUN: {}\tITERATIONS: {}".format(r + 1, w.num_generations))
    w.evolve(show_iterations = par.DebugParams.SHOW_ITERATIONS,
              show_every_n_iteration = int(num_iterations / par.DebugParams.NUM_CHECKPOINTS),
              show_final_genomes = par.DebugParams.SHOW_RUN_GENOMES,
              show_final_fitness = par.DebugParams.SHOW_RUN_FITNESS)
    all_fitness_history[r + 1] = w.fitness_history

  aggregate_fitness_history = fit.FitnessHistoryAggregate.get_aggregated_fitness(all_fitness_history,
                                                                                  fitness_aggregate_type = par.AggregationParams.FITNESS_AGGREGATION_TYPE,
                                                                                  time_to_aggregate_type = par.AggregationParams.TIME_AGGREGATION_TYPE)
  if par.DebugParams.SHOW_AGGREGATED_FITNESS:
    print("\nFINAL METRICS\n")
    aggregate_fitness_history.history['iterations'][num_iterations].print_fitness_data()
    print()
    aggregate_fitness_history.print_time_to()

  if par.DebugParams.WRITE_AGGREGATED_FITNESS:
    out_filename = fhio.get_filename(population_size, num_assignments, num_runs, num_iterations, 
                                      evolution_strategy.name, randomize_assignment_priorities, randomize_assignment_sizes,
                                      datetime_string)
    fhio.write_fitness_history(filename = out_filename, fitness_history = aggregate_fitness_history)


def main():
  args = sys.argv[1:]
  validate_params()

  fhio = dat.FitnessHistoryIO()
  datetime_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  if par.LoopParams.MULTI_PARAMS:
    for evolution_strategy in par.EvolutionStrategy:
      if evolution_strategy == par.EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT:
        continue
      for randomize_assignment_priorities in [False, True]:
        for randomize_assignment_sizes in [False, True]:
          run_evolution(fhio, datetime_string,
                        par.PopulationParams.POPULATION_SIZE, par.WorldParams.NUM_RUNS, par.WorldParams.NUM_GENERATIONS, par.PopulationParams.NUM_ASSIGNMENTS,
                        evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes)
  else:
    run_evolution(fhio, datetime_string,
                  par.PopulationParams.POPULATION_SIZE, par.WorldParams.NUM_RUNS, par.WorldParams.NUM_GENERATIONS, par.PopulationParams.NUM_ASSIGNMENTS,
                  par.WorldParams.EVOLUTION_STRATEGY, par.WorldParams.RANDOMIZE_ASSIGNMENT_PRIORITIES, par.WorldParams.RANDOMIZE_ASSIGNMENT_SIZES)

if __name__=="__main__":
  main()
