from . import individual as ind

class Group:

  def __init__(self, group_size, genome_size, individuals = None):
    self.group_size = group_size
    self.genome_size = genome_size

    if individuals:
      self.individuals = individuals
    else:
      self.individuals = [ind.Individual(genome_size) for _ in range(group_size)]
    self.assignment = -1

  def get_fitness(self):
    sum = 0.0
    for i in self.individuals:
      sum += i.get_fitness()
    return sum

  def __str__(self):
    return (
      "GROUP\n" +
      "Assignment: {},\tGroup Size: {}\n".format(self.assignment, self.group_size) +
      "".join([str(i) for i in self.individuals]) +
      "\n")
