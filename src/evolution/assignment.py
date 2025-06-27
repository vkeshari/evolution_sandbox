import numpy as np
from scipy.optimize import linear_sum_assignment

import params as par

class Assignment:

  RANDOM_ASSIGNMENT_PICKER = np.random.RandomState()
  ASSIGNMENT_PRIORITY_RANDOMIZER = np.random.RandomState()
  ASSIGNMENT_SIZE_RANDOMIZER = np.random.RandomState()

  def __init__(self, assignment_strategy,
                restrict_assignment = False, group_by_assignment = False,
                randomize_assignment_priorities = False, randomize_assignment_sizes = False):
    self.assignment_strategy = assignment_strategy
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
  
  def random_assignment(self, population):
    enumerated = []
    for i, group in enumerate(population.groups):
      for j, individual in enumerate(group.individuals):
        enumerated.append({'group': i, 'index': j, 'individual': individual})
    self.RANDOM_ASSIGNMENT_PICKER.shuffle(enumerated)

    assigned = 0
    for a, size in population.assignment_sizes.items():
      for e in enumerated[assigned : assigned + size]:
        population.groups[e['group']].individuals[e['index']].assignment = a
      assigned += size

  def greedy_assignment(self, population):
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
  
  def assignment_matching(self, population):
    individual_group_and_indices = []
    assignment_cost_matrix = np.array([])
    for i, group in enumerate(population.groups):
      for j, individual in enumerate(group.individuals):
        individual_group_and_indices.append(tuple([i, j]))
        i_costs = individual.get_genes()
        i_costs_expanded = np.array([])
        for a in sorted(population.assignment_sizes.keys()):
          i_costs_expanded = np.append(i_costs_expanded,
                                       np.repeat(i_costs[a], population.assignment_sizes[a]))
        if assignment_cost_matrix.size == 0:
          assignment_cost_matrix = i_costs_expanded
        else:
          assignment_cost_matrix = np.vstack((assignment_cost_matrix, i_costs_expanded))

    assignments_expanded = np.array([])
    for a in sorted(population.assignment_sizes.keys()):
      if assignments_expanded.size == 0:
        assignments_expanded = np.repeat(a, population.assignment_sizes[a])
      else:
        assignments_expanded = np.append(assignments_expanded,
                                          np.repeat(a, population.assignment_sizes[a]))

    [i_match_indices, a_match_indices] = \
        linear_sum_assignment(assignment_cost_matrix, maximize = True)

    for i in i_match_indices:
      (group_no, individual_no) = individual_group_and_indices[i]
      population.groups[group_no].individuals[individual_no].assignment = \
          assignments_expanded[a_match_indices[i]]

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
      if self.assignment_strategy == par.AssignmentStrategy.RANDOM:
        self.random_assignment(population)
      elif self.assignment_strategy == par.AssignmentStrategy.ASSIGNMENT_PRIORITY:
        self.greedy_assignment(population)
      elif self.assignment_strategy == par.AssignmentStrategy.ASSIGNMENT_MATCHING:
        self.assignment_matching(population)
    
    if self.group_by_assignment:
      self.shuffle_by_assignment(population)
