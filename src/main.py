import sys
from enum import Enum

from containers import population as pop
from evolution import crossover as crs
from evolution import assignment as ass
from evolution import fitness as fit
from evolution import world as wrd

class DebugParams:
  SHOW_ITERATIONS = True
  NUM_CHECKPOINTS = 10

  SHOW_FINAL_GENOMES = False
  SHOW_FINAL_FITNESS = True

class FitnessParams:
  TIME_TO_FITNESS_VALUES = [0.9, 0.95, 0.99]

class CrossoverParams:
  CROSSOVER_BETA_PARAM = 2.5
  INTERPOLATE_GENES = True
  MUTATION_RATE = 0.01

class PopulationParams:
  POPULATION_SIZE = 100
  NUM_GROUPS = 10
  NUM_ASSIGNMENTS = 10

class WorldParams:
  NUM_GENERATIONS = 1000

class EvolutionStrategy(Enum):
  NO_RESTRICTIONS = 0                      #000
  NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT = 1  #001
  CROSSOVER_BY_GROUP_ONLY = 2              #100
  CROSSOVER_BY_ASSIGNMENT_ONLY = 3         #101
  ALL_RESTRICTIONS = 4                     #11_
EVOLUTION_STRATEGY = EvolutionStrategy.NO_RESTRICTIONS_GROUP_BY_ASSIGNMENT
print(EVOLUTION_STRATEGY)

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
  assert (PopulationParams.NUM_GROUPS == PopulationParams.NUM_ASSIGNMENTS)
  assert (PopulationParams.POPULATION_SIZE % PopulationParams.NUM_GROUPS == 0)
  assert (PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS > 2.0)

def initialize_world():
  (restrict_crossover, restrict_assignment, group_by_assignment) = get_evolution_constraints()

  p = pop.Population(population_size = PopulationParams.POPULATION_SIZE,
                      num_groups = PopulationParams.NUM_GROUPS,
                      group_size = int(PopulationParams.POPULATION_SIZE / PopulationParams.NUM_GROUPS),
                      genome_size = PopulationParams.NUM_ASSIGNMENTS)

  a = ass.Assignment(restrict_assignment = restrict_assignment,
                      group_by_assignment = group_by_assignment)
  a.update_assignments(population = p)

  c = crs.Crossover(crossover_beta_param = CrossoverParams.CROSSOVER_BETA_PARAM,
                    mutation_rate = CrossoverParams.MUTATION_RATE,
                    interpolate_genes = CrossoverParams.INTERPOLATE_GENES)

  f = fit.Fitness(time_to_fitness_values = FitnessParams.TIME_TO_FITNESS_VALUES, genome_size = PopulationParams.NUM_ASSIGNMENTS)

  w = wrd.World(initial_population = p,
                assignment = a,
                crossover = c,
                fitness = f,
                num_generations = WorldParams.NUM_GENERATIONS,
                restrict_crossover = restrict_crossover)
  return w

def main():
  args = sys.argv[1:]
  validate_params()

  w = initialize_world()
  w.evolve(show_iterations = DebugParams.SHOW_ITERATIONS,
            show_every_n_iteration = int(WorldParams.NUM_GENERATIONS / DebugParams.NUM_CHECKPOINTS),
            show_final_genomes = DebugParams.SHOW_FINAL_GENOMES,
            show_final_fitness = DebugParams.SHOW_FINAL_FITNESS)
  fitness_history = w.fitness

if __name__=="__main__":
  main()
