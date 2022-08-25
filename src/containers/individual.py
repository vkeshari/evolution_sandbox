from . import genome as gen

class Individual:

  def __init__(self, genome_size, genome = None):
    self.genome_size = genome_size

    if genome:
      self.genome = genome
    else:
      self.genome = gen.Genome(genome_size, randomize = True)
    self.assignment = -1

  def __str__(self):
    return "Assignment: {}\tGene: {}\n".format(self.assignment, self.genome)

  def get_fitness(self):
    if self.assignment == -1:
      return 0.0
    else:
      return self.genome.genes[self.assignment]
