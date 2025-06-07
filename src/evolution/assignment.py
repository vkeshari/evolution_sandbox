import numpy as np

class Assignment:

  ASSIGNMENT_PRIORITY_RANDOMIZER = np.random.RandomState()
  ASSIGNMENT_SIZE_RANDOMIZER = np.random.RandomState()

  def __init__(self, restrict_assignment = False, group_by_assignment = False,
                randomize_assignment_priorities = False, randomize_assignment_sizes = False):
    self.restrict_assignment = restrict_assignment
    self.group_by_assignment = group_by_assignment
    self.randomize_assignment_priorities = randomize_assignment_priorities
    self.randomize_assignment_sizes = randomize_assignment_sizes

  def get_assignment_distribution(self, population_size, genome_size):
    assignment_priorities = [*range(genome_size)]
    if self.randomize_assignment_priorities:
      self.ASSIGNMENT_PRIORITY_RANDOMIZER.shuffle(assignment_priorities)

    default_group_size = int(population_size / genome_size)
    assignment_sizes = {i: default_group_size for i in range(genome_size)}
    if self.randomize_assignment_sizes:
      for i in range(population_size):
        swap_indices = self.ASSIGNMENT_SIZE_RANDOMIZER.randint(0, genome_size, 2)
        if assignment_sizes[swap_indices[0]] > int(default_group_size / 2):
          assignment_sizes[swap_indices[0]] -= 1
          assignment_sizes[swap_indices[1]] += 1
    return (assignment_priorities, assignment_sizes)

  def shuffle_by_assignment(self, population):
    all_individuals = population.get_all_individuals(assigned = True)

    for a in range(population.genome_size):
      group = population.groups[a]
      group.assignment = a
      group.group_size = population.assignment_sizes[a]
      group.individuals = [i for i in all_individuals if i.assignment == a]

  def update_assignments(self, population):
    if self.restrict_assignment:
      for a in range(population.genome_size):
        group = population.groups[a]
        for individual in sorted(group.individuals, key = lambda i: i.genome.genes[a],
                                 reverse = True) \
                              [:population.assignment_sizes[a]]:
          individual.assignment = a

    else:
      enumerated = []
      for i, group in enumerate(population.groups):
        for j, individual in enumerate(group.individuals):
          enumerated.append({'group': i, 'index': j, 'individual': individual})

      for a in population.assignment_priorities:
        sorted_for_a = sorted(enumerated, key = lambda e: e['individual'].genome.genes[a],
                              reverse = True)
        unassigned = [e for e in sorted_for_a if not e['individual'].has_assignment()]
        for k in range(population.assignment_sizes[a]):
          group_no = unassigned[k]['group']
          individual_no = unassigned[k]['index']
          population.groups[group_no].individuals[individual_no].assignment = a

    if self.group_by_assignment:
      self.shuffle_by_assignment(population)
