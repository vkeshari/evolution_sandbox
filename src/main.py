import sys
from containers import population as pop
from evolution import crossover as crs
from evolution import world as wrd

class CrossoverParams:
  CROSSOVER_FRACTION = 0.7
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

class EvolutionConstraints:
  RESTRICT_CROSSOVER = False
  RESTRICT_ASSIGNMENT = False
  #GROUP_BY_ASSIGNMENT = False

class PopulationParams:
  POPULATION_SIZE = 100
  NUM_GROUPS = 10
  NUM_ASSIGNMENTS = 10

class WorldParams:
  NUM_GENERATIONS = 1000

def validate_params():
  assert (PopulationParams.POPULATION_SIZE % PopulationParams.NUM_GROUPS == 0)
  assert (PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS > 1)
  assert (EvolutionConstraints.RESTRICT_CROSSOVER or not EvolutionConstraints.RESTRICT_ASSIGNMENT)

def main():
  args = sys.argv[1:]
  validate_params()

  p = pop.Population(
    population_size = PopulationParams.POPULATION_SIZE,
    num_groups = PopulationParams.NUM_GROUPS,
    group_size = int(PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS),
    genome_size = PopulationParams.NUM_ASSIGNMENTS)

  c = crs.Crossover(
    crossover_fraction = CrossoverParams.CROSSOVER_FRACTION,
    mutation_rate = CrossoverParams.MUTATION_RATE,
    interpolate_genes = CrossoverParams.INTERPOLATE_GENES)

  w = wrd.World(
    initial_population = p,
    crossover = c,
    num_generations = WorldParams.NUM_GENERATIONS,
    restrict_crossover = EvolutionConstraints.RESTRICT_CROSSOVER,
    restrict_assignment = EvolutionConstraints.RESTRICT_ASSIGNMENT)

  w.evolve()

if __name__=="__main__":
  main()
