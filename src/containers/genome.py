import numpy as np

class Genome:

  GENOME_RANDOMIZER = np.random.RandomState()

  def __init__(self, genome_size, randomize=False):
    self.genome_size = genome_size

    if randomize:
      self.genes = self.GENOME_RANDOMIZER.random_sample(genome_size)
    else:
      self.genes = np.zeros(genome_size)

  def __str__(self):
    # return str(["{:.2}".format(g) for g in self.genes])
    np.set_printoptions(precision=2)
    return str(self.genes)
