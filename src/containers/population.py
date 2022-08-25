from . import group as grp

class Population:

  def __init__(self, population_size, num_groups, group_size, genome_size, groups = None):
    self.population_size = population_size
    self.num_groups = num_groups
    self.group_size = group_size
    self.genome_size = genome_size

    if groups:
      self.groups = groups
    else:
      self.groups = [grp.Group(group_size, genome_size) for _ in range(num_groups)]

  def __str__(self):
    return (
      "POPULATION\n" +
      "Num Groups: {},\tGroup Size: {}\n".format(self.num_groups, self.group_size) +
      "Fitness: {:.2}\n\n".format(self.get_fitness() / self.population_size) +
      "".join([str(g) for g in self.groups]) +
      "\n")

  def get_fitness(self):
    sum = 0.0
    for g in self.groups:
      sum += g.get_fitness()
    return sum

  def show_all_fitness(self):
    total_fitness = self.get_fitness() / self.population_size
    print("TOTAL FITNESS: {:.2}".format(total_fitness))
    print("FITNESS BY ASSIGNMENT")
    for a in range(self.genome_size):
      a_sum = 0.0
      a_count = 0
      for g in self.groups:
        for i in g.individuals:
          if i.assignment == a:
            a_sum += i.genome.genes[a]
            a_count += 1
      print("Assignment {}\tCount: {}\tFitness: {:.2}".format(a, a_count, a_sum / a_count))

  def show_stats(self, show_all_genomes = False, show_all_fitness = False):
    if show_all_genomes:
      print("FINAL POPULATION\n")
      print(self)
    if show_all_fitness:
      self.show_all_fitness()
