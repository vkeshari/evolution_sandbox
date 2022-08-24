from . import individual as ind

class Group:

  def __init__(self, group_size, genome_size):
    self.group_size = group_size
    self.genome_size = genome_size

    self.individuals = [ind.Individual(genome_size) for i in range(group_size)]
    self.assignment = -1

  def __str__(self):
    return (
      "GROUP\n" +
      "Assignment: {},\tGroup Size: {}\n".format(self.assignment, self.group_size) +
      "".join([str(i) for i in self.individuals]) +
      "\n"
    )
