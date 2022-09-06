import params as par
from metrics import dataio as dat
from metrics import graph as gra

def graph_by_strategy(fitness_history_io, show = False, save = False):
  fcg = gra.FitnessCombinedGraph(max_iterations = par.GraphParams.MAX_ITERATIONS,
                                  time_to_fitness_values = par.GraphParams.TIME_TO_FITNESS_VALUES)

  for evolution_strategy in par.EvolutionStrategy:
    if evolution_strategy == par.EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT:
      continue
    datafile = fitness_history_io.get_data_filename(par.DataViewerParams.POPULATION_SIZE,
                                                    par.DataViewerParams.NUM_ASSIGNMENTS,
                                                    par.DataViewerParams.NUM_RUNS,
                                                    par.DataViewerParams.NUM_ITERATIONS,
                                                    evolution_strategy.name,
                                                    par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                                                    par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES,
                                                    par.DataViewerParams.DATETIME_STRING)
    fitness_history = fitness_history_io.read_fitness_history(datafile, show = False)
    fcg.add_fitness_history(key = evolution_strategy.name, fitness_history = fitness_history)

  fig_type = 'Evolution by Strategy'
  variable = 'EvolutionStrategy'
  fixed = 'RandomPriorities: {}, RandomSizes: {}'.format(
      str(par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES),
      str(par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES))
  savefile = None
  if save:
    savefile = fitness_history_io.get_graph_filename(par.DataViewerParams.POPULATION_SIZE,
                                                      par.DataViewerParams.NUM_ASSIGNMENTS,
                                                      par.DataViewerParams.NUM_RUNS,
                                                      par.DataViewerParams.NUM_ITERATIONS,
                                                      "VAR",
                                                      par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                                                      par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES,
                                                      par.DataViewerParams.DATETIME_STRING,
                                                      "BYSTRATEGY",
                                                      "FIT" if par.GraphParams.FIT_CURVE else "NOFIT")
  fcg.plot(title = fig_type + '\n' + fixed + '\nKey: ' + variable,
            show = show, fit_curve = par.GraphParams.FIT_CURVE, savefile = savefile)

def graph_by_assignment_variations(fitness_history_io, show = False, save = False):
  fcg = gra.FitnessCombinedGraph(max_iterations = par.GraphParams.MAX_ITERATIONS,
                                  time_to_fitness_values = par.GraphParams.TIME_TO_FITNESS_VALUES)

  for randomize_assignment_priorities in [False, True]:
    for randomize_assignment_sizes in [False, True]:
      datafile = fitness_history_io.get_data_filename(par.DataViewerParams.POPULATION_SIZE,
                                                      par.DataViewerParams.NUM_ASSIGNMENTS,
                                                      par.DataViewerParams.NUM_RUNS,
                                                      par.DataViewerParams.NUM_ITERATIONS,
                                                      par.DataViewerParams.EVOLUTION_STRATEGY.name,
                                                      randomize_assignment_priorities,
                                                      randomize_assignment_sizes,
                                                      par.DataViewerParams.DATETIME_STRING)
      fitness_history = fitness_history_io.read_fitness_history(datafile, show = False)
      key = '(' + str(randomize_assignment_priorities) + ', ' + str(randomize_assignment_sizes) + ')'
      fcg.add_fitness_history(key = key, fitness_history = fitness_history)
  
  fig_type = 'Evolution by Assignment Types'
  variable = '(RandomPriorities, RandomSizes)'
  fixed = 'EvolutionStrategy: {}'.format(par.DataViewerParams.EVOLUTION_STRATEGY.name)
  savefile = None
  if save:
    savefile = fitness_history_io.get_graph_filename(par.DataViewerParams.POPULATION_SIZE,
                                                      par.DataViewerParams.NUM_ASSIGNMENTS,
                                                      par.DataViewerParams.NUM_RUNS,
                                                      par.DataViewerParams.NUM_ITERATIONS,
                                                      par.DataViewerParams.EVOLUTION_STRATEGY.name,
                                                      "VAR",
                                                      "VAR",
                                                      par.DataViewerParams.DATETIME_STRING,
                                                      "BYRANDOMNESS",
                                                      "FIT" if par.GraphParams.FIT_CURVE else "NOFIT")
  fcg.plot(title = fig_type + '\n' + fixed + '\nKey: ' + variable,
            show = show, fit_curve = par.GraphParams.FIT_CURVE, savefile = savefile)

def graph_by_assignment(fitness_history_io, show = False, save = False):
  fcg = gra.FitnessCombinedGraph(max_iterations = par.GraphParams.MAX_ITERATIONS,
                                  time_to_fitness_values = par.GraphParams.TIME_TO_FITNESS_VALUES)

  datafile = fitness_history_io.get_data_filename(par.DataViewerParams.POPULATION_SIZE,
                                                  par.DataViewerParams.NUM_ASSIGNMENTS,
                                                  par.DataViewerParams.NUM_RUNS,
                                                  par.DataViewerParams.NUM_ITERATIONS,
                                                  par.DataViewerParams.EVOLUTION_STRATEGY.name,
                                                  par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                                                  par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES,
                                                  par.DataViewerParams.DATETIME_STRING)
  fitness_history = fitness_history_io.read_fitness_history(datafile, show = False)
  for assignment in range(par.DataViewerParams.NUM_ASSIGNMENTS):
    fcg.add_fitness_history(key = 'Assignment {}'.format(assignment) , fitness_history = fitness_history)
  
  fig_type = 'Evolution by Assignment'
  variable = 'AssignmentNo'
  fixed = 'EvolutionStrategy: {}, RandomPriorities: {}, RandomSizes: {}'.format(
      par.DataViewerParams.EVOLUTION_STRATEGY.name,
      str(par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES),
      str(par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES))
  savefile = None
  if save:
    savefile = fitness_history_io.get_graph_filename(par.DataViewerParams.POPULATION_SIZE,
                                                      par.DataViewerParams.NUM_ASSIGNMENTS,
                                                      par.DataViewerParams.NUM_RUNS,
                                                      par.DataViewerParams.NUM_ITERATIONS,
                                                      par.DataViewerParams.EVOLUTION_STRATEGY.name,
                                                      par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                                                      par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES,
                                                      par.DataViewerParams.DATETIME_STRING,
                                                      "BYASSIGNMENT",
                                                      "FIT" if par.GraphParams.FIT_CURVE else "NOFIT")
  fcg.plot(title = fig_type + '\n' + fixed + '\nKey: ' + variable,
            show = show, by_assignment = True, fit_curve = par.GraphParams.FIT_CURVE, savefile = savefile)

def main():
  fhio = dat.FitnessHistoryIO()

  if par.GraphTypes.BY_EVOLUTION_STRATEGY:
    graph_by_strategy(fitness_history_io = fhio, show = par.GraphParams.SHOW_GRAPHS, save = par.GraphParams.SAVE_GRAPHS)
  if par.GraphTypes.BY_ASSIGNMENT_RANDOMIZATION:
    graph_by_assignment_variations(fitness_history_io = fhio, show = par.GraphParams.SHOW_GRAPHS, save = par.GraphParams.SAVE_GRAPHS)
  if par.GraphTypes.BY_ASSIGNMENT:
    graph_by_assignment(fitness_history_io = fhio, show = par.GraphParams.SHOW_GRAPHS, save = par.GraphParams.SAVE_GRAPHS)

if __name__=="__main__":
  main()
