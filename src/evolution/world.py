import numpy as np

from . import crossover as crs
from containers import population as pop
from containers import group as grp
from metrics import fitness as fit

class World:

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
    self.assign_purge_measure(self.current_generation, iteration_no = 0)

  def assign_purge_measure(self, population, iteration_no):
    self.assignment.update_assignments(population)
    fitness_data = fit.FitnessData.from_population(population)
    self.fitness_history.update_fitness_history(iteration_no, fitness_data)

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
        new_groups.append(grp.Group(g.group_size, g.genome_size,
                                    individuals = new_group_individuals))
        already_assigned += g.group_size

    (assignment_priorities, assignment_sizes) = \
        self.assignment.get_assignment_distribution(population.population_size,
                                                    population.genome_size)
    new_generation = pop.Population(population.population_size,
                                    population.num_groups,
                                    population.genome_size,
                                    assignment_priorities = assignment_priorities,
                                    assignment_sizes = assignment_sizes,
                                    groups = new_groups)
    return new_generation

  def evolve(self, show_iterations = False,
              show_every_n_iteration = 1,
              show_run_genomes = False,
              show_run_fitness = False,
              show_stats_at_checkpoints = False):
    if (show_every_n_iteration == 0):
      show_every_n_iteration = 1

    for i in range(self.num_generations):
      is_checkpoint = (i + 1) % show_every_n_iteration == 0
      if is_checkpoint:
        if show_iterations:
          total_fitness = self.current_generation.get_fitness()
          print("ITERATION: {}\tFitness: {:.2}".format(i + 1, total_fitness))
        if show_stats_at_checkpoints:
          fit.FitnessUtil.show_population_stats(self.current_generation, show_run_genomes,
                                                show_run_fitness)

      updated_generation = self.new_generation(self.current_generation)
      self.assign_purge_measure(updated_generation, iteration_no = i + 1)
      self.current_generation = updated_generation

    if show_run_genomes or show_run_fitness:
      print("RUN STATS\n")
      fit.FitnessUtil.show_population_stats(self.current_generation, show_run_genomes,
                                            show_run_fitness)
      if show_run_fitness:
        self.fitness_history.print_time_to()

    return self.fitness_history
