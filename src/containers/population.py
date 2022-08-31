from . import group as grp

class Population:

  def __init__(self, population_size, num_groups, genome_size, assignment_priorities, assignment_sizes, groups = None):
    self.population_size = population_size
    self.num_groups = num_groups
    self.genome_size = genome_size
    self.assignment_priorities = assignment_priorities
    self.assignment_sizes = assignment_sizes

    if groups:
      self.groups = groups
    else:
      self.groups = [grp.Group(int(population_size / num_groups), genome_size) for i in range(num_groups)]

  def __str__(self):
    return (
      "POPULATION\n" +
      "Num Groups: {},\tGroup Sizes: {}\n".format(self.num_groups, ' '.join([str(g.group_size) for g in self.groups])) +
      "Fitness: {:.2}\n\n".format(self.get_fitness()) +
      "".join([str(g) for g in self.groups]) +
      "\n")

  def get_fitness(self):
    sum = 0.0
    for g in self.groups:
      sum += g.get_fitness() * g.group_size
    return sum / self.population_size

  def get_all_individuals(self, sort = False, descending = False):
    all_individuals = []
    for g in self.groups:
      all_individuals += g.individuals
    if sort:
      all_individuals = sorted(all_individuals, key = lambda i: i.get_fitness(), reverse = descending)
    return all_individuals
