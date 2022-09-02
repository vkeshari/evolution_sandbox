from metrics import dataio as dat
from metrics import graph as gra

FILENAME = "Run_p100_a10_r10_i100_ALL_RESTRICTIONS_False_False_20220901130953.data"

def main():
  fhio = dat.FitnessHistoryIO()
  fitness_history = fhio.read_fitness_history(FILENAME, show = False)

  itg = gra.FitnessCombinedGraph(10)
  itg.add_fitness_history("TEST", fitness_history)
  itg.plot(show = True)


if __name__=="__main__":
  main()
