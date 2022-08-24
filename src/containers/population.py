from . import group as grp

class Population:

  def __init__(self, num_groups, group_size, genome_size, groups = None):
    self.num_groups = num_groups
    self.group_size = group_size
    self.genome_size = genome_size

    if groups:
      self.groups = group_size
    else:
      self.groups = [grp.Group(group_size, genome_size) for _ in range(num_groups)]

  def get_fitness(self):
    sum = 0.0
    for g in self.groups:
      sum += g.get_fitness()
    return sum

  def __str__(self):
    return (
      "POPULATION\n" +
      "Num Groups: {},\tGroup Size: {}\n\n".format(self.num_groups, self.group_size) +
      "".join([str(g) for g in self.groups]) +
      "\n")
