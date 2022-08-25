import random
import numpy as np

from . import crossover as crs
from containers import population as pop
from containers import group as grp

class World:

  def __init__(self, initial_population, assignment, crossover, num_generations, restrict_crossover = False):
    self.assignment = assignment
    self.crossover = crossover
    self.num_generations = num_generations
    self.restrict_crossover = restrict_crossover

    self.current_generation = initial_population
    self.generation_history = [initial_population]

  def new_generation(self, population):
    new_groups = []

    if self.restrict_crossover:
      for g in population.groups:
        crossed = self.crossover.crossover(g.individuals, g.individuals, population.group_size)
        new_groups.append(grp.Group(population.group_size, population.genome_size, individuals = crossed))

    else:
      all_individuals = []
      for g in population.groups:
        all_individuals += g.individuals
      crossed = self.crossover.crossover(all_individuals, all_individuals, population.population_size)
      random.shuffle(crossed)
      for i in range(population.num_groups):
        group_individuals = crossed[i * population.group_size : (i + 1) * population.group_size]
        new_groups.append(grp.Group(population.group_size, population.genome_size, individuals = group_individuals))

    new_generation = pop.Population(population.population_size,
                                    population.num_groups,
                                    population.group_size,
                                    population.genome_size,
                                    groups = new_groups)
    self.assignment.update_assignments(new_generation)

    return new_generation

  def evolve(self, show_iterations = False, show_all_genomes = False, show_all_fitness = False):
    print("NUM_ITERATIONS: {}".format(self.num_generations))
    for i in range(self.num_generations):
      if show_iterations:
        total_fitness = self.current_generation.get_fitness() / self.current_generation.population_size
        print("ITERATION: {}\tFitness: {:.2}".format(i, total_fitness))

      updated_generation = self.new_generation(self.current_generation)
      self.generation_history.append(updated_generation)
      self.current_generation = updated_generation

    self.current_generation.show_stats(show_all_genomes, show_all_fitness)
