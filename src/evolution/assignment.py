class Assignment:

  def __init__(self, restrict_assignment = False, group_by_assignment = False):
    self.restrict_assignment = restrict_assignment
    self.group_by_assignment = group_by_assignment

  def shuffle_by_assignment(self, population):
    all_individuals = []
    for group in population.groups:
      all_individuals += group.individuals

    for a in range(population.genome_size):
      group = population.groups[a]
      group.assignment = a
      group.group_size = population.assignment_sizes[a]
      group.individuals = [i for i in all_individuals if i.assignment == a]

  def update_assignments(self, population):
    if self.restrict_assignment:
      for a in range(population.genome_size):
        group = population.groups[a]
        for individual in sorted(group.individuals, key = lambda i: i.genome.genes[a], reverse = True)[:population.assignment_sizes[a]]:
          individual.assignment = a

    else:
      enumerated = []
      for i, group in enumerate(population.groups):
        for j, individual in enumerate(group.individuals):
          enumerated.append({'group': i, 'index': j, 'individual': individual})

      for a in population.assignment_priorities:
        sorted_for_a = sorted(enumerated, key = lambda e: e['individual'].genome.genes[a], reverse = True)
        unassigned = [e for e in sorted_for_a if not e['individual'].has_assignment()]
        for k in range(population.assignment_sizes[a]):
          group_no = unassigned[k]['group']
          individual_no = unassigned[k]['index']
          population.groups[group_no].individuals[individual_no].assignment = a

    if self.group_by_assignment:
      self.shuffle_by_assignment(population)

    #for g in population.groups:
    #  assert(len(g.individuals) == g.group_size)
