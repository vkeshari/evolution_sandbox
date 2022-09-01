from metrics import dataio as dat

FILENAME = ""

def main():
  fhio = dat.FitnessHistoryIO()
  fhio.read_fitness_history(FILENAME, show = True)

if __name__=="__main__":
  main()
