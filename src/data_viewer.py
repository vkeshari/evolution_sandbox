from metrics import dataio as dat

FILENAME = "Run_p100_r10_i100_a10_CROSSOVER_BY_ASSIGNMENT_ONLY_False_False_20220901094226.data"

def main():
  fhio = dat.FitnessHistoryIO()
  fhio.read_fitness_history(FILENAME, show = True)

if __name__=="__main__":
  main()
