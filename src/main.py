import sys
from containers import population as pop

class EvolutionParams:
  MUTATION_RATE = 0.01

class EvolutionConstraints:
  RESTRICT_CROSSOVER = False
  RESTRICT_ASSIGNMENT = False

class WorldParams:
  POPULATION_SIZE = 100
  NUM_GROUPS = 4
  GENOME_SIZE = 4

def validate_params():
  assert (WorldParams.POPULATION_SIZE % WorldParams.NUM_GROUPS == 0)

def main():
  args = sys.argv[1:]
  validate_params()

  p = pop.Population(
    num_groups = WorldParams.NUM_GROUPS,
    group_size = int(WorldParams.POPULATION_SIZE / WorldParams.NUM_GROUPS),
    genome_size = WorldParams.GENOME_SIZE
  )
  print(p)

if __name__=="__main__":
  main()
