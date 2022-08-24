import sys
from containers import population as pop
from evolution import crossover as crs
from evolution import world as wrd

class EvolutionParams:
  CROSSOVER_FRACTION = 0.8
  MUTATION_RATE = 0.001

class EvolutionConstraints:
  RESTRICT_CROSSOVER = False
  RESTRICT_ASSIGNMENT = False

class PopulationParams:
  POPULATION_SIZE = 100
  NUM_GROUPS = 10
  NUM_ASSIGNMENTS = 10

class WorldParams:
  NUM_GENERATIONS = 10000

def validate_params():
  assert (PopulationParams.POPULATION_SIZE % PopulationParams.NUM_GROUPS == 0)

def main():
  args = sys.argv[1:]
  validate_params()

  p = pop.Population(
    population_size = PopulationParams.POPULATION_SIZE,
    num_groups = PopulationParams.NUM_GROUPS,
    group_size = int(PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS),
    genome_size = PopulationParams.NUM_ASSIGNMENTS)

  c = crs.Crossover(
    crossover_fraction = EvolutionParams.CROSSOVER_FRACTION,
    mutation_rate = EvolutionParams.MUTATION_RATE)

  w = wrd.World(
    initial_population = p,
    crossover = c,
    num_generations = WorldParams.NUM_GENERATIONS,
    restrict_crossover = EvolutionConstraints.RESTRICT_CROSSOVER,
    restrict_assignment = EvolutionConstraints.RESTRICT_ASSIGNMENT)

  w.evolve()

if __name__=="__main__":
  main()
