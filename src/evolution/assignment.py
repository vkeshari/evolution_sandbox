class Assignment:

  def __init__(self, restrict_assignment = False, group_by_assignment = False):
    self.restrict_assignment = restrict_assignment
    self.group_by_assignment = group_by_assignment

  def shuffle_by_assignment(self, population):
    all_individuals = []
    for g in population.groups:
      all_individuals += g.individuals

    for a in range(population.genome_size):
      population.groups[a].individuals = [i for i in all_individuals if i.assignment == a]

  def update_assignments(self, population):
    if self.restrict_assignment:
      for i, group in enumerate(population.groups):
        group.assignment = i
        for individual in group.individuals:
          individual.assignment = i

    else:
      enumerated = []
      for i, group in enumerate(population.groups):
        for j, individual in enumerate(group.individuals):
          enumerated.append({'group': i, 'index': j, 'individual': individual})

      for a in range(population.genome_size):
        sorted_for_a = sorted(enumerated, key = lambda e: e['individual'].genome.genes[a], reverse = True)
        unassigned = [e for e in sorted_for_a if e['individual'].assignment == -1]
        for k in range(population.group_size):
          group_no = unassigned[k]['group']
          individual_no = unassigned[k]['index']
          population.groups[group_no].individuals[individual_no].assignment = a

      if self.group_by_assignment:
        self.shuffle_by_assignment(population)
