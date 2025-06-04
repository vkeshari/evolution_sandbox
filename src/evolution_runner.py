import numpy as np
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed, wait
from datetime import datetime
from time import sleep

import params as par
from containers import population as pop
from evolution import crossover as crs
from evolution import assignment as ass
from evolution import world as wrd
from metrics import fitness as fit
from metrics import dataio as dat

def get_evolution_constraints(evolution_strategy):
  restrict_crossover = evolution_strategy in [
                          par.EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY,
                          par.EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                          par.EvolutionStrategy.ALL_RESTRICTIONS]
  restrict_assignment = evolution_strategy == par.EvolutionStrategy.ALL_RESTRICTIONS
  group_by_assignment = evolution_strategy in [
                          par.EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT,
                          par.EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                          par.EvolutionStrategy.ALL_RESTRICTIONS]
  return (restrict_crossover, restrict_assignment, group_by_assignment)

def validate_params():
  assert par.PopulationParams.NUM_GROUPS > 0
  assert par.PopulationParams.NUM_GROUPS == par.PopulationParams.NUM_ASSIGNMENTS
  assert par.PopulationParams.POPULATION_SIZE > par.PopulationParams.NUM_GROUPS
  assert par.PopulationParams.POPULATION_SIZE % par.PopulationParams.NUM_GROUPS == 0
  assert par.PopulationParams.POPULATION_SIZE / par.PopulationParams.NUM_GROUPS > 2.0

  assert par.WorldParams.NUM_RUNS > 0
  assert par.WorldParams.NUM_GENERATIONS >= 10

  if par.DebugParams.SHOW_ITERATIONS \
      or par.DebugParams.SAVE_GENOMES_AT_CHECKPOINTS \
      or par.DebugParams.SHOW_STATS_AT_CHECKPOINTS:
    assert not par.LoopParams.MULTI_PARAMS and par.WorldParams.NUM_RUNS == 1

def initialize_world(population_size, num_iterations, num_assignments, evolution_strategy,
                     randomize_assignment_priorities, randomize_assignment_sizes, pio):
  (restrict_crossover, restrict_assignment, group_by_assignment) = \
      get_evolution_constraints(evolution_strategy)

  a = ass.Assignment(restrict_assignment = restrict_assignment,
                      group_by_assignment = group_by_assignment,
                      randomize_assignment_priorities = randomize_assignment_priorities,
                      randomize_assignment_sizes = randomize_assignment_sizes)
  (assignment_priorities, assignment_sizes) = \
      a.get_assignment_distribution(population_size, num_assignments)

  p = pop.Population(population_size = population_size,
                      num_groups = num_assignments,
                      genome_size = num_assignments,
                      assignment_priorities = assignment_priorities,
                      assignment_sizes = assignment_sizes)

  c = crs.Crossover(crossover_beta_param = par.CrossoverParams.CROSSOVER_BETA_PARAM,
                    mutation_rate = par.CrossoverParams.MUTATION_RATE,
                    interpolate_genes = par.CrossoverParams.INTERPOLATE_GENES)

  f = fit.FitnessHistory(time_to_fitness_values = par.FitnessParams.TIME_TO_FITNESS_VALUES,
                         genome_size = num_assignments)

  w = wrd.World(initial_population = p,
                assignment = a,
                crossover = c,
                fitness_history = f,
                num_generations = num_iterations,
                restrict_crossover = restrict_crossover,
                pio = pio)
  return w

def run_evolution(fhio, datetime_string,
                  population_size, num_runs, num_iterations, num_assignments,
                  evolution_strategy, randomize_assignment_priorities, randomize_assignment_sizes):

  print("Evolution Strategy: {}".format(evolution_strategy))
  print("Randomize Assignment Priorities: {}".format(randomize_assignment_priorities))
  print("Randomize Assignment Sizes: {}".format(randomize_assignment_sizes))
  print("Fitness Aggregation: {}".format(par.AggregationParams.FITNESS_AGGREGATION_TYPE))
  print("Time Aggregation: {}".format(par.AggregationParams.TIME_AGGREGATION_TYPE))
  print()

  start_time = datetime.now()

  all_fitness_history = {}
  run_times = []
  with ProcessPoolExecutor() as executor:
    evolve_futures = []
    for r in range(num_runs):
      pio = dat.PopulationIO(
                  population_size = population_size,
                  num_groups = num_assignments,
                  evolution_strategy_name = evolution_strategy.name,
                  randomize_assignment_priorities = randomize_assignment_priorities,
                  randomize_assignment_sizes = randomize_assignment_sizes,
                  datetime_string = datetime_string)
      w = initialize_world(population_size, num_iterations, num_assignments, evolution_strategy,
                            randomize_assignment_priorities, randomize_assignment_sizes, pio)
      
      evolve_futures.append(
          executor.submit(
              w.evolve,
              show_iterations = par.DebugParams.SHOW_ITERATIONS,
              show_every_n_iteration = int(num_iterations / par.DebugParams.NUM_CHECKPOINTS),
              show_run_genomes = par.DebugParams.SHOW_RUN_GENOMES,
              show_run_fitness = par.DebugParams.SHOW_RUN_FITNESS,
              show_stats_at_checkpoints = par.DebugParams.SHOW_STATS_AT_CHECKPOINTS,
              save_genomes_at_checkpoints = par.DebugParams.SAVE_GENOMES_AT_CHECKPOINTS))
    
    print ("STARTED: {} RUNS".format(len(evolve_futures)))
    
    if par.DebugParams.SHOW_RUN_STATUS:
      ef_status = [ef.done() for ef in evolve_futures]
      while not all(ef_status):
        ef_status = [ef.done() for ef in evolve_futures]
        num_completed = sum(ef_status)
        print ("COMPLETED: {}\tOF {} RUNS".format(num_completed, num_runs))
        if num_completed < num_runs:
          sleep(par.DebugParams.SHOW_RUN_STATUS_DELAY)
    else:
      wait(evolve_futures)
      print ("COMPLETED: {} RUNS".format(num_runs))
      
    for r, ef in enumerate(as_completed(evolve_futures)):
      fitness_history, run_time = ef.result()
      all_fitness_history[r + 1] = fitness_history
      run_times.append(run_time)
  
  total_time = datetime.now() - start_time
  
  if par.DebugParams.SHOW_RUN_TIME_SUMMARY:
    print()
    print("RUN DURATION AVERAGE:\t{}".format(np.average(run_times)))
    print("RUN DURATION MEDIAN :\t{}".format(np.median(run_times)))
    print()
    print("TOTAL DURATION      :\t{}".format(total_time))
    print("DURATION PER RUN    :\t{}".format(total_time / num_runs))
    print()

  aggregate_fitness_history = \
      fit.FitnessHistoryAggregate.get_aggregated_fitness(
          all_fitness_history,
          fitness_aggregate_type = par.AggregationParams.FITNESS_AGGREGATION_TYPE,
          time_to_aggregate_type = par.AggregationParams.TIME_AGGREGATION_TYPE)
  if par.DebugParams.SHOW_AGGREGATED_FITNESS:
    print("\nFINAL AGGREGATED METRICS\n")
    aggregate_fitness_history.history['iterations'][num_iterations].print_fitness_data()
    print()
    aggregate_fitness_history.print_time_to()

  if par.DebugParams.WRITE_AGGREGATED_FITNESS:
    out_filename = fhio.get_data_filename(
                      population_size, num_assignments, num_runs, num_iterations, 
                      evolution_strategy.name, randomize_assignment_priorities,
                      randomize_assignment_sizes)
    fhio.write_fitness_history(filename = out_filename, fitness_history = aggregate_fitness_history)
    print()


def evolution_runner():
  validate_params()

  datetime_string = datetime.now().strftime("%Y%m%d%H%M%S")
  print ("TIMESTAMP:\t{}\n".format(datetime_string))

  fhio = dat.FitnessHistoryIO(datetime_string = datetime_string)

  if par.LoopParams.MULTI_PARAMS:
    for evolution_strategy in par.EvolutionStrategy:
      if evolution_strategy == par.EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT:
        continue
      for randomize_assignment_priorities in [False, True]:
        for randomize_assignment_sizes in [False, True]:
          run_evolution(fhio, datetime_string, par.PopulationParams.POPULATION_SIZE,
                        par.WorldParams.NUM_RUNS, par.WorldParams.NUM_GENERATIONS,
                        par.PopulationParams.NUM_ASSIGNMENTS, evolution_strategy,
                        randomize_assignment_priorities, randomize_assignment_sizes)
  else:
    run_evolution(fhio, datetime_string, par.PopulationParams.POPULATION_SIZE,
                  par.WorldParams.NUM_RUNS, par.WorldParams.NUM_GENERATIONS,
                  par.PopulationParams.NUM_ASSIGNMENTS, par.WorldParams.EVOLUTION_STRATEGY,
                  par.WorldParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                  par.WorldParams.RANDOMIZE_ASSIGNMENT_SIZES)
  
  print ("TIMESTAMP:\t{}\n".format(datetime_string))
  return datetime_string

if __name__=="__main__":
  evolution_runner()
