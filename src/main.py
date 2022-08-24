import sys
from containers import population as pop
from evolution import crossover as crs

class EvolutionParams:
  CROSSOVER_FRACTION = 0.8
  MUTATION_RATE = 0.01

class EvolutionConstraints:
  RESTRICT_CROSSOVER = False
  RESTRICT_ASSIGNMENT = False

class WorldParams:
  POPULATION_SIZE = 20
  NUM_GROUPS = 4
  NUM_ASSIGNMENTS = 4

def validate_params():
  assert (WorldParams.POPULATION_SIZE % WorldParams.NUM_GROUPS == 0)

def main():
  args = sys.argv[1:]
  validate_params()

  p = pop.Population(
    num_groups = WorldParams.NUM_GROUPS,
    group_size = int(WorldParams.POPULATION_SIZE / WorldParams.NUM_GROUPS),
    genome_size = WorldParams.NUM_ASSIGNMENTS)

  c = crs.Crossover(
    crossover_fraction = EvolutionParams.CROSSOVER_FRACTION,
    mutation_rate = EvolutionParams.MUTATION_RATE)

if __name__=="__main__":
  main()
