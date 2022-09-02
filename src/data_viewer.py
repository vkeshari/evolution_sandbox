import params as par
from metrics import dataio as dat
from metrics import graph as gra

def main():
  fhio = dat.FitnessHistoryIO()

  filename = fhio.get_filename(par.DataViewerParams.POPULATION_SIZE,
                                par.DataViewerParams.NUM_ASSIGNMENTS,
                                par.DataViewerParams.NUM_RUNS,
                                par.DataViewerParams.NUM_ITERATIONS,
                                par.DataViewerParams.EVOLUTION_STRATEGY.name,
                                par.DataViewerParams.RANDOMIZE_ASSIGNMENT_PRIORITIES,
                                par.DataViewerParams.RANDOMIZE_ASSIGNMENT_SIZES,
                                par.DataViewerParams.DATETIME_STRING)
  fitness_history = fhio.read_fitness_history(filename, show = False)

  itg = gra.FitnessCombinedGraph(par.GraphParams.MAX_ITERATIONS)
  itg.add_fitness_history("TEST", fitness_history)
  itg.plot(show = True)


if __name__=="__main__":
  main()
