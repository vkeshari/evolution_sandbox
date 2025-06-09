from datetime import datetime

import evolution_runner as evo
import params as par
from metrics import dataio as dat
from metrics import graph as gra

def validate_range_steps(min_val, max_val, step_size):
  assert step_size > 0
  assert max_val > min_val > 0
  assert (max_val - min_val) % step_size == 0

def validate_params():
  validate_range_steps(par.GATuningParams.MIN_GA,
                        par.GATuningParams.MAX_GA,
                        par.GATuningParams.GA_STEP)
  
  has_custom_datetime_string = len(par.GATuningParams.CUSTOM_DATETIME_STRING) > 0
  assert not has_custom_datetime_string ^ par.GATuningParams.GRAPHS_ONLY
  
  assert len(par.GATuningParams.TIME_TO_FITNESS_VALUES) > 0
  assert par.GATuningParams.PLOT_TIME_TO_FITNESS in par.GATuningParams.TIME_TO_FITNESS_VALUES

  par.WorldParams.NUM_RUNS = par.GATuningParams.NUM_RUNS
  par.WorldParams.NUM_GENERATIONS = par.GATuningParams.NUM_ITERATIONS
  par.WorldParams.EVOLUTION_STRATEGY = par.EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY
  par.WorldParams.ASSIGNMENT_STRATEGY = par.AssignmentStrategy.ASSIGNMENT_MATCHING

  par.PopulationParams.POPULATION_SIZE = par.GATuningParams.POPULATION_SIZE

  par.FitnessParams.TIME_TO_FITNESS_VALUES = par.GATuningParams.TIME_TO_FITNESS_VALUES
  par.AggregationParams.FITNESS_AGGREGATION_TYPE = par.GATuningParams.FITNESS_AGGREGATION_TYPE
  par.AggregationParams.TIME_AGGREGATION_TYPE = par.GATuningParams.TIME_AGGREGATION_TYPE

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

def get_group_assignment_pairs(population_size):

  num_groups_range = range(par.GATuningParams.MIN_GA,
                            par.GATuningParams.MAX_GA + 1,
                            par.GATuningParams.GA_STEP)
  num_assignments_range = range(par.GATuningParams.MIN_GA,
                                par.GATuningParams.MAX_GA + 1,
                                par.GATuningParams.GA_STEP)

  # Pairs of feasible num groups and num assignments
  ga_vals = []
  for g in num_groups_range:
    for a in num_assignments_range:
      if population_size % g == 0 and population_size % a == 0:
        if g >= 5 and a >= 5:
          ga_vals.append(tuple([g, a]))

  print("Total Groups and Assignment Count Pairs: {}".format(len(ga_vals)))
  for g, a in ga_vals:
    print ("GROUPS:\t{}\tASSIGNMENTS:\t{}".format(g, a))
  print()

  return ga_vals

def generate_data_for_group_assignment_pairs(ga_vals, datetime_string):

  for i, (g, a) in enumerate(ga_vals):
    print ("{} OF {} TUNING RUNS".format(i, len(ga_vals)))
    print ("GROUPS:\t{}\tASSIGNMENTS:\t{}".format(g, a))
    print()

    par.PopulationParams.NUM_GROUPS = g
    par.PopulationParams.NUM_ASSIGNMENTS = a

    for rap in par.GATuningParams.RANDOM_ASSIGNMENT_PRIORITIES_VALS:
      for ras in par.GATuningParams.RANDOM_ASSIGNMENT_SIZES_VALS:
        par.WorldParams.RANDOMIZE_ASSIGNMENT_SIZES = ras
        par.WorldParams.RANDOMIZE_ASSIGNMENT_PRIORITIES = rap

        evo.evolution_runner(datetime_string)

def make_tuning_graph(fhio, tio, ga_vals, num_runs, num_iterations,
                      population_size, evolution_strategy_name,
                      randomize_assignment_priorities, randomize_assignment_sizes):

  graph_vals = {}
  graph_vals['final_fitness'] = {}
  graph_vals['time_to_fitness'] = {}
  for (g, a) in ga_vals:
    data_filename = fhio.get_data_filename(
                        population_size = population_size, num_assignments = a, num_groups = g,
                        num_runs = num_runs, num_iterations = num_iterations,
                        evolution_strategy_name = evolution_strategy_name,
                        randomize_assignment_priorities = randomize_assignment_priorities,
                        randomize_assignment_sizes = randomize_assignment_sizes)
    
    fitness_history = fhio.read_fitness_history(data_filename)
    final_population_fitness = \
        fitness_history.history['iterations'][num_iterations].data['population']['fitness']
    f = par.GATuningParams.PLOT_TIME_TO_FITNESS
    time_to_fitness = fitness_history.history['time_to']['population'][f]

    ga_tuple = tuple([g, a])
    graph_vals['final_fitness'][ga_tuple] = final_population_fitness
    graph_vals['time_to_fitness'][ga_tuple] = time_to_fitness
  
  save_filename = tio.get_ga_tuning_filename(num_runs, num_iterations, population_size,
                                              randomize_assignment_priorities,
                                              randomize_assignment_sizes)
  
  tuning_graph = gra.TuningGraph(ga_vals, type = 'GA')
  graph_title_text = ("Average Population Fitness after {} generations\n" \
                        + "Population Size: {}\n" \
                        + "Random Assignment Priorities: {}, Random Assignment Sizes: {}") \
      .format(num_iterations, population_size,
              randomize_assignment_priorities, randomize_assignment_sizes)
  tuning_graph.plot(graph_vals, title_text = graph_title_text, savefile = save_filename)

def make_tuning_graphs(ga_vals, datetime_string):

  fhio = dat.FitnessHistoryIO(datetime_string)
  tio = dat.TuningIO(datetime_string)

  for rap in par.GATuningParams.RANDOM_ASSIGNMENT_PRIORITIES_VALS:
    for ras in par.GATuningParams.RANDOM_ASSIGNMENT_SIZES_VALS:
      make_tuning_graph(
          fhio, tio, ga_vals,
          num_runs = par.GATuningParams.NUM_RUNS,
          num_iterations = par.GATuningParams.NUM_ITERATIONS,
          population_size = par.GATuningParams.POPULATION_SIZE,
          evolution_strategy_name = par.GATuningParams.POPULATION_SIZE.name,
          randomize_assignment_priorities = rap,
          randomize_assignment_sizes = ras)


def ga_tuning_run():
  validate_params()

  if par.GATuningParams.CUSTOM_DATETIME_STRING:
    datetime_string = par.GATuningParams.CUSTOM_DATETIME_STRING
  else:
    datetime_string = datetime.now().strftime("%Y%m%d%H%M%S")
  print ("TIMESTAMP:\t{}\n".format(datetime_string))

  ga_vals = get_group_assignment_pairs(par.GATuningParams.POPULATION_SIZE)

  if not par.GATuningParams.GRAPHS_ONLY:
    generate_data_for_group_assignment_pairs(ga_vals, datetime_string)
  make_tuning_graphs(ga_vals, datetime_string)

  print ("TIMESTAMP:\t{}\n".format(datetime_string))

if __name__ == "__main__":
  ga_tuning_run()
