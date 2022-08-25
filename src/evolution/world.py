import random
import numpy as np

from . import crossover as crs
from containers import population as pop
from containers import group as grp

class World:

  def __init__(self, initial_population, crossover, num_generations, restrict_crossover = False):
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
                                    population.restrict_assignment,
                                    population.group_by_assignment,
                                    groups = new_groups)
    new_generation.update_assignments()

    return new_generation

  def evolve(self):
    for i in range(self.num_generations):
      total_fitness = self.current_generation.get_fitness() / self.current_generation.population_size
      print("ITERATION: {}\tFitness: {:.2}".format(i, total_fitness))

      updated_generation = self.new_generation(self.current_generation)
      self.generation_history.append(updated_generation)
      self.current_generation = updated_generation

    print("FINAL POPULATION\n")
    print(self.current_generation)

    print("FITNESS BY ASSIGNMENT\n")
    for a in range(self.current_generation.genome_size):
      a_sum = 0.0
      a_count = 0
      for g in self.current_generation.groups:
        for i in g.individuals:
          if i.assignment == a:
            a_sum += i.genome.genes[a]
            a_count += 1
      print("Assignment {}\tCount: {}\tFitness: {:.2}".format(a, a_count, a_sum / a_count))
