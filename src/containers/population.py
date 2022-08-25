from . import group as grp

class Population:

  def __init__(self, population_size, num_groups, group_size, genome_size,
      restrict_assignment = False, group_by_assignment = False, groups = None):
    self.population_size = population_size
    self.num_groups = num_groups
    self.group_size = group_size
    self.genome_size = genome_size

    self.restrict_assignment = restrict_assignment
    self.group_by_assignment = group_by_assignment

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

  def shuffle_by_assignment(self):
    all_individuals = []
    for g in self.groups:
      all_individuals += g.individuals

    for a in range(self.genome_size):
      self.groups[a].individuals = [i for i in all_individuals if i.assignment == a]

  def update_assignments(self):
    if self.restrict_assignment:
      for i, group in enumerate(self.groups):
        group.assignment = i
        for individual in group.individuals:
          individual.assignment = i

    else:
      enumerated = []
      for i, group in enumerate(self.groups):
        for j, individual in enumerate(group.individuals):
          enumerated.append({'group': i, 'index': j, 'individual': individual})

      for a in range(self.genome_size):
        sorted_for_a = sorted(enumerated, key = lambda e: e['individual'].genome.genes[a], reverse = True)
        unassigned = [e for e in sorted_for_a if e['individual'].assignment == -1]
        for k in range(self.group_size):
          group_no = unassigned[k]['group']
          individual_no = unassigned[k]['index']
          self.groups[group_no].individuals[individual_no].assignment = a

      if self.group_by_assignment:
        self.shuffle_by_assignment()

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
