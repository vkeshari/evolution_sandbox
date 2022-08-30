import random
import numpy as np

from . import crossover as crs
from containers import population as pop
from containers import group as grp
from metrics import fitness as fit

class World:

  def __init__(self, initial_population, assignment, crossover, fitness_history, num_generations, restrict_crossover = False):
    self.assignment = assignment
    self.crossover = crossover
    self.fitness_history = fitness_history
    self.num_generations = num_generations
    self.restrict_crossover = restrict_crossover

    self.current_generation = initial_population
    self.fitness_history.update_iteration(0, fit.FitnessData.from_population(initial_population))

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
      random.shuffle(crossed)
      already_assigned = 0
      for g in population.groups:
        new_group_individuals = crossed[already_assigned : already_assigned + g.group_size]
        new_groups.append(grp.Group(g.group_size, g.genome_size, individuals = new_group_individuals))
        already_assigned += g.group_size

    new_generation = pop.Population(population.population_size,
                                    population.num_groups,
                                    population.group_size,
                                    population.genome_size,
                                    groups = new_groups)

    # DEFAULT
    assignment_priorities = range(new_generation.num_groups)
    assignment_sizes = [new_generation.group_size] * new_generation.num_groups
    self.assignment.update_assignments(new_generation, assignment_priorities = assignment_priorities, assignment_sizes = assignment_sizes)

    return new_generation

  def evolve(self, show_iterations = False, show_every_n_iteration = 1, show_final_genomes = False, show_final_fitness = False):
    if (show_every_n_iteration == 0):
      show_every_n_iteration = 1

    for i in range(self.num_generations):
      if show_iterations and i % show_every_n_iteration == 0:
        total_fitness = self.current_generation.get_fitness()
        print("ITERATION: {}\tFitness: {:.2}".format(i, total_fitness))

      updated_generation = self.new_generation(self.current_generation)

      fitness_data = fit.FitnessData.from_population(updated_generation)
      self.fitness_history.update_iteration(i + 1, fitness_data)
      self.fitness_history.update_time_to(i + 1, fitness_data)

      self.current_generation = updated_generation

    fit.FitnessUtil.show_population_stats(self.current_generation, show_final_genomes, show_final_fitness)
    if show_final_fitness:
      self.fitness_history.print_time_to()
