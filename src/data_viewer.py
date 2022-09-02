import params as par
from metrics import dataio as dat
from metrics import graph as gra

def main():
  fhio = dat.FitnessHistoryIO()
  itg = gra.FitnessCombinedGraph(max_iterations = par.GraphParams.MAX_ITERATIONS,
                                  time_to_fitness_values = par.GraphParams.TIME_TO_FITNESS_VALUES)

  for evolution_strategy in par.EvolutionStrategy:
    if evolution_strategy == par.EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT:
      continue
    filename = fhio.get_filename(par.DataViewerParams.POPULATION_SIZE,
                                  par.DataViewerParams.NUM_ASSIGNMENTS,
                                  par.DataViewerParams.NUM_RUNS,
                                  par.DataViewerParams.NUM_ITERATIONS,
                                  evolution_strategy.name,
                                  par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                                  par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES,
                                  par.DataViewerParams.DATETIME_STRING)
    fitness_history = fhio.read_fitness_history(filename, show = False)
    itg.add_fitness_history(key = evolution_strategy.name, fitness_history = fitness_history)

  itg.plot(show = True)


if __name__=="__main__":
  main()
