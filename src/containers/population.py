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

  def get_subgroup_fitness(self, individuals):
    fitness = 0.0
    for i in individuals:
      fitness += i.get_fitness() / len(individuals)
    return fitness

  def get_percentiles(self, individuals):
    percentile_data = {}
    percentile_data[0] = individuals[0].get_fitness()
    for i in range(10, 100, 10):
      percentile_data[i] = individuals[int(i * len(individuals) / 100)].get_fitness()
    percentile_data[100] = individuals[-1].get_fitness()
    return percentile_data

  def pretty_print_percentiles(self, a):
    return "Min: {:.2}\t10P: {:.2}\t50P: {:.2}\t90P: {:.2}\tMax: {:.2}".format(a[0], a[10], a[50], a[90], a[100])

  def get_fitness_data(self):
    fitness_data = {}

    all_individuals = self.get_all_individuals(sort = True)
    fitness_data['population'] = {}
    fitness_data['population']['fitness'] = self.get_subgroup_fitness(all_individuals)
    fitness_data['population']['percentiles'] = self.get_percentiles(all_individuals)

    fitness_data['assignment'] = {}
    for a in range(self.genome_size):
      assignment_individuals = [i for i in all_individuals if i.assignment == a]
      fitness_data['assignment'][a] = {}
      fitness_data['assignment'][a]['fitness'] = self.get_subgroup_fitness(assignment_individuals)
      fitness_data['assignment'][a]['percentiles'] = self.get_percentiles(assignment_individuals)

    return fitness_data

  def show_fitness(self):
    all_individuals = self.get_all_individuals(sort = True)
    print("TOTAL FITNESS: {:.2}".format(self.get_subgroup_fitness(all_individuals)))
    print("Percentiles: {}".format(self.pretty_print_percentiles(self.get_percentiles(all_individuals))))
    print("FITNESS BY ASSIGNMENT")
    for a in range(self.genome_size):
      assignment_individuals = [i for i in all_individuals if i.assignment == a]
      print("Assignment {}\tCount: {}\tFitness: {:.2}"
        .format(a, len(assignment_individuals), self.get_subgroup_fitness(assignment_individuals)))
      print("Percentiles: {}".format(self.pretty_print_percentiles(self.get_percentiles(assignment_individuals))))

  def show_stats(self, show_genomes = False, show_fitness = False):
    if show_genomes:
      print("FINAL POPULATION\n")
      print(self)
    if show_fitness:
      self.show_fitness()
