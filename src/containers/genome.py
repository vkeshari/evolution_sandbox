import numpy as np

class Genome:

  GENE_RANDOMIZER = np.random.RandomState()

  def __init__(self, genome_size, randomize = False):
    self.genome_size = genome_size

    if randomize:
      self.genes = self.GENE_RANDOMIZER.random_sample(genome_size)
    else:
      self.genes = np.zeros(genome_size)

  def __str__(self):
    np.set_printoptions(precision = 4)
    return str(self.genes)
