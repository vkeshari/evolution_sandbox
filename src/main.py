import sys
from enum import Enum

from containers import population as pop
from evolution import crossover as crs
from evolution import world as wrd

class CrossoverParams:
  CROSSOVER_FRACTION = 0.7
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

class PopulationParams:
  POPULATION_SIZE = 100
  NUM_GROUPS = 10
  NUM_ASSIGNMENTS = 10

class WorldParams:
  NUM_GENERATIONS = 100

class EvolutionStrategy(Enum):
  NO_RESTRICTIONS = 0                      #000
  NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT = 1  #001
  CROSSOVER_BY_GROUP_ONLY = 2              #100
  CROSSOVER_BY_ASSIGNMENT_ONLY = 3         #101
  ALL_RESTRICTIONS = 4                     #11_
EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS

def get_evolution_constraints():
  restrict_crossover = EVOLUTION_STRATEGY in [EvolutionStrategy.CROSSOVER_BY_GROUP_ONLY,
                                              EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                              EvolutionStrategy.ALL_RESTRICTIONS]
  restrict_assignment = EVOLUTION_STRATEGY == EvolutionStrategy.ALL_RESTRICTIONS
  group_by_assignment = EVOLUTION_STRATEGY in [EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT,
                                              EvolutionStrategy.CROSSOVER_BY_ASSIGNMENT_ONLY,
                                              EvolutionStrategy.ALL_RESTRICTIONS]
  return (restrict_crossover, restrict_assignment, group_by_assignment)                                              

def validate_params():
  assert (PopulationParams.POPULATION_SIZE % PopulationParams.NUM_GROUPS == 0)
  assert (PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS > 1)

def initialize_world():
  (restrict_crossover, restrict_assignment, group_by_assignment) = get_evolution_constraints()

  p = pop.Population(
    population_size = PopulationParams.POPULATION_SIZE,
    num_groups = PopulationParams.NUM_GROUPS,
    group_size = int(PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS),
    genome_size = PopulationParams.NUM_ASSIGNMENTS,
    restrict_assignment = restrict_assignment,
    group_by_assignment = group_by_assignment)
  p.update_assignments()

  c = crs.Crossover(
    crossover_fraction = CrossoverParams.CROSSOVER_FRACTION,
    mutation_rate = CrossoverParams.MUTATION_RATE,
    interpolate_genes = CrossoverParams.INTERPOLATE_GENES)

  w = wrd.World(
    initial_population = p,
    crossover = c,
    num_generations = WorldParams.NUM_GENERATIONS,
    restrict_crossover = restrict_crossover)
  return w


def main():
  args = sys.argv[1:]
  validate_params()

  w = initialize_world()
  w.evolve()

if __name__=="__main__":
  main()
