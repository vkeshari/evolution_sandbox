from datetime import datetime

import evolution_runner as evo
import params as par
from metrics import dataio as dat
from metrics import fitness as fit

def validate_range_steps(min_val, max_val, step_size):
  assert max_val > min_val
  assert (max_val - min_val) % step_size == 0

def validate_params():
  validate_range_steps(par.TuningParams.MIN_POPULATION,
                        par.TuningParams.MAX_POPULATION,
                        par.TuningParams.POPULATION_STEP)
  validate_range_steps(par.TuningParams.MIN_GROUP_SIZE,
                        par.TuningParams.MAX_GROUP_SIZE,
                        par.TuningParams.GROUP_SIZE_STEP)
  
  par.LoopParams.MULTI_PARAMS = False

  par.WorldParams.NUM_RUNS = par.TuningParams.NUM_RUNS
  par.WorldParams.NUM_GENERATIONS = par.TuningParams.NUM_ITERATIONS
  par.WorldParams.RANDOMIZE_ASSIGNMENT_PRIORITIES = par.TuningParams.RANDOMIZE_ASSIGNMENT_PRIORITIES

  par.FitnessParams.TIME_TO_FITNESS_VALUES = par.TuningParams.TIME_TO_FITNESS_VALUES
  par.AggregationParams.FITNESS_AGGREGATION_TYPE = par.TuningParams.FITNESS_AGGREGATION_TYPE
  par.AggregationParams.TIME_AGGREGATION_TYPE = par.TuningParams.TIME_AGGREGATION_TYPE

  par.DebugParams.SHOW_RUN_STATUS = False
  par.DebugParams.SHOW_RUN_STATUS_DELAY = 1
  par.DebugParams.SHOW_RUN_TIME_SUMMARY = False
  par.DebugParams.SHOW_ITERATIONS = False
  par.DebugParams.NUM_CHECKPOINTS = 2
  par.DebugParams.SAVE_GENOMES_AT_CHECKPOINTS = False
  par.DebugParams.SHOW_RUN_GENOMES = False
  par.DebugParams.SHOW_RUN_FITNESS = False
  par.DebugParams.SHOW_STATS_AT_CHECKPOINTS = False
  par.DebugParams.SHOW_AGGREGATED_FITNESS = False
  par.DebugParams.WRITE_AGGREGATED_FITNESS = True

def get_population_group_pairs():

  pop_range = range(par.TuningParams.MIN_POPULATION,
                    par.TuningParams.MAX_POPULATION + 1,
                    par.TuningParams.POPULATION_STEP)
  group_size_range = range(par.TuningParams.MIN_GROUP_SIZE,
                            par.TuningParams.MAX_GROUP_SIZE + 1,
                            par.TuningParams.GROUP_SIZE_STEP)

  # Pairs of feasible population size and num groups
  pg_vals = []
  for p in pop_range:
    for gs in group_size_range:
      if p % gs == 0:
        g = int(p / gs)
        if g % 5 == 0:
          pg_vals.append(tuple([p, g]))

  print("Total Population and Group Count Pairs: {}".format(len(pg_vals)))
  for p, g in pg_vals:
    print ("POPULATION:\t{}\tGROUPS:\t{}".format(p, g))
  print()

  return pg_vals

def generate_data_for_population_group_pairs(pg_vals, datetime_string):

  for i, (p, g) in enumerate(pg_vals):
    print ("{} OF {} TUNING RUNS".format(i, len(pg_vals)))
    print ("POPULATION:\t{}\tGROUPS:\t{}".format(p, g))
    print()

    par.PopulationParams.POPULATION_SIZE = p
    par.PopulationParams.NUM_GROUPS = g
    par.PopulationParams.NUM_ASSIGNMENTS = g

    for es in par.TuningParams.EVOLUTION_STRATEGY_VALS:
      for ras in par.TuningParams.RANDOM_ASSIGNMENT_SIZES_VALS:
        par.WorldParams.EVOLUTION_STRATEGY = es
        par.WorldParams.RANDOMIZE_ASSIGNMENT_SIZES = ras

        evo.evolution_runner(datetime_string)

def make_tuning_graph(fhio, tio, pg_vals, num_runs, num_iterations, evolution_strategy_name,
                      randomize_assignment_priorities, randomize_assignment_sizes):
  
  for (p, g) in pg_vals:
    data_filename = fhio.get_data_filename(
                        population_size = p, num_assignments = g,
                        num_runs = num_runs, num_iterations = num_iterations,
                        evolution_strategy_name = evolution_strategy_name,
                        randomize_assignment_priorities = randomize_assignment_priorities,
                        randomize_assignment_sizes = randomize_assignment_sizes)
    
    fitness_history = fhio.read_fitness_history(data_filename)
  
  save_filename = tio.get_tuning_filename(num_runs, num_iterations,
                                          evolution_strategy_name,
                                          randomize_assignment_priorities,
                                          randomize_assignment_sizes)

def make_tuning_graphs(pg_vals, datetime_string):
  fhio = dat.FitnessHistoryIO(datetime_string)
  tio = dat.TuningIO(datetime_string)
  for es in par.TuningParams.EVOLUTION_STRATEGY_VALS:
    for ras in par.TuningParams.RANDOM_ASSIGNMENT_SIZES_VALS:

      make_tuning_graph(
          fhio, tio, pg_vals,
          num_runs = par.TuningParams.NUM_RUNS,
          num_iterations = par.TuningParams.NUM_ITERATIONS,
          evolution_strategy_name = es.name,
          randomize_assignment_priorities = par.TuningParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
          randomize_assignment_sizes = ras)


def tuning_run():
  validate_params()

  if par.TuningParams.CUSTOM_DATETIME_STRING:
    datetime_string = par.TuningParams.CUSTOM_DATETIME_STRING
  else:
    datetime_string = datetime.now().strftime("%Y%m%d%H%M%S")
  print ("TIMESTAMP:\t{}\n".format(datetime_string))

  pg_vals = get_population_group_pairs()

  if not par.TuningParams.GRAPHS_ONLY:
    generate_data_for_population_group_pairs(pg_vals, datetime_string)
  make_tuning_graphs(pg_vals, datetime_string)

  print ("TIMESTAMP:\t{}\n".format(datetime_string))

if __name__ == "__main__":
  tuning_run()
