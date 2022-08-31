import random
import numpy as np

from . import crossover as crs
from containers import population as pop
from containers import group as grp
from metrics import fitness as fit

class World:

  ASSIGNMENT_PRIORITY_RANDOMIZER = np.random.RandomState()
  ASSIGNMENT_SIZE_RANDOMIZER = np.random.RandomState()
  INDIVIDUALS_ORDER_RANDOMIZER = np.random.RandomState()

  def __init__(self, initial_population, assignment, crossover, fitness_history, num_generations,
                restrict_crossover = False,
                randomize_assignment_priorities = False,
                randomize_assignment_sizes = False):
    self.assignment = assignment
    self.crossover = crossover
    self.fitness_history = fitness_history
    self.num_generations = num_generations
    self.restrict_crossover = restrict_crossover
    self.randomize_assignment_priorities = randomize_assignment_priorities
    self.randomize_assignment_sizes = randomize_assignment_sizes

    self.current_generation = initial_population
    self.fitness_history.update_iteration(0, fit.FitnessData.from_population(initial_population))

  def get_assignment_distribution(self, population_size, genome_size):
    assignment_priorities = [*range(genome_size)]
    if self.randomize_assignment_priorities:
      self.ASSIGNMENT_PRIORITY_RANDOMIZER.shuffle(assignment_priorities)

    default_group_size = int(population_size / genome_size)
    assignment_sizes = {i: default_group_size for i in range(genome_size)}
    if self.randomize_assignment_sizes:
      for i in range(population_size):
        swap_indices = self.ASSIGNMENT_SIZE_RANDOMIZER.randint(0, genome_size, 2)
        if assignment_sizes[swap_indices[0]] > int(default_group_size / 2):
          assignment_sizes[swap_indices[0]] -= 1
          assignment_sizes[swap_indices[1]] += 1
    return (assignment_priorities, assignment_sizes)

  def new_generation(self, population):
    new_groups = []

    if self.restrict_crossover:
      for g in population.groups:
        crossover_pool = [i for i in g.individuals if i.has_assignment()]
        crossed = self.crossover.crossover(crossover_pool, crossover_pool, g.group_size)
        new_groups.append(grp.Group(g.group_size, g.genome_size, individuals = crossed))

    else:
      crossover_pool = []
      for g in population.groups:
        for i in g.individuals:
          if i.has_assignment():
            crossover_pool += g.individuals
      crossed = self.crossover.crossover(crossover_pool, crossover_pool, population.population_size)
      self.INDIVIDUALS_ORDER_RANDOMIZER.shuffle(crossed)
      already_assigned = 0
      for g in population.groups:
        new_group_individuals = crossed[already_assigned : already_assigned + g.group_size]
        new_groups.append(grp.Group(g.group_size, g.genome_size, individuals = new_group_individuals))
        already_assigned += g.group_size

    (assignment_priorities, assignment_sizes) = self.get_assignment_distribution(population.population_size, population.num_groups)
    new_generation = pop.Population(population.population_size,
                                    population.num_groups,
                                    population.genome_size,
                                    assignment_priorities,
                                    assignment_sizes,
                                    groups = new_groups)

    self.assignment.update_assignments(new_generation)

    return new_generation

  def evolve(self, show_iterations = False, show_every_n_iteration = 1, show_final_genomes = False, show_final_fitness = False):
    if (show_every_n_iteration == 0):
      show_every_n_iteration = 1

    for i in range(self.num_generations):
      if show_iterations and (i + 1) % show_every_n_iteration == 0:
        total_fitness = self.current_generation.get_fitness()
        print("ITERATION: {}\tFitness: {:.2}".format(i + 1, total_fitness))

      updated_generation = self.new_generation(self.current_generation)

      fitness_data = fit.FitnessData.from_population(updated_generation)
      self.fitness_history.update_iteration(i + 1, fitness_data)
      self.fitness_history.update_time_to(i + 1, fitness_data)

      self.current_generation = updated_generation

    fit.FitnessUtil.show_population_stats(self.current_generation, show_final_genomes, show_final_fitness)
    if show_final_fitness:
      self.fitness_history.print_time_to()
