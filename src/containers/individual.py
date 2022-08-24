from . import genome as gen

class Individual:

  def __init__(self, genome_size):
    self.genome_size = genome_size

    self.genome = gen.Genome(genome_size, randomize=True)
    self.assignment = -1

  def __str__(self):
    return "Assignment: {}\tGene: {}\n".format(self.assignment, self.genome)
