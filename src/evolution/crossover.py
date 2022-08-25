import numpy as np

from containers import genome as gen
from containers import individual as ind

class Crossover:

  INDIVIDUAL_RANDOMIZER = np.random.RandomState()
  CROSSOVER_RANDOMIZER = np.random.RandomState()
  MUTATION_RANDOMIZER = np.random.RandomState()
  MUTATED_GENE_RANDOMIZER = np.random.RandomState()
  CROSSOVER_BETA_PARAM = 0.25

  def __init__(self, crossover_fraction, mutation_rate, interpolate_genes):
    self.crossover_fraction = crossover_fraction
    self.mutation_rate = mutation_rate
    self.interpolate_genes = interpolate_genes

  def crossover_genomes(self, genome1, genome2, genome_size):
    g = gen.Genome(genome_size = genome_size, randomize = False)

    for i in range(genome_size):
      if self.interpolate_genes:
        sample = self.CROSSOVER_RANDOMIZER.beta(self.CROSSOVER_BETA_PARAM, self.CROSSOVER_BETA_PARAM)
        g.genes[i] = genome1[i] + sample * (genome2[i] - genome1[i])

      else:
        choice = self.CROSSOVER_RANDOMIZER.randint(0, 2)
        if choice == 0:
          g.genes[i] = genome1[i]
        elif choice == 1:
          g.genes[i] = genome2[i]

      if self.MUTATION_RANDOMIZER.rand() < self.mutation_rate:
        g.genes[i] = self.MUTATED_GENE_RANDOMIZER.rand()

    return g

  def crossover(self, individuals_1, individuals_2, out_size):
    if len(individuals_1) == 0 or len(individuals_2) == 0:
      return []

    genome_size = individuals_1[0].genome_size
    genome_size_check = individuals_2[0].genome_size
    assert(genome_size == genome_size_check)

    i1_size = int(len(individuals_1) * self.crossover_fraction)
    i1 = sorted(individuals_1, key = lambda i: i.get_fitness(), reverse = True)[:i1_size]

    i2_size = int(len(individuals_2) * self.crossover_fraction)
    i2 = sorted(individuals_2, key = lambda i: i.get_fitness(), reverse = True)[:i2_size]

    out = []
    for i in range(out_size):
      index1 = index2 = 0
      while (index1 == index2):
        index1 = self.INDIVIDUAL_RANDOMIZER.randint(0, i1_size)
        index2 = self.INDIVIDUAL_RANDOMIZER.randint(0, i2_size)
      g1 = i1[index1].genome.genes
      g2 = i2[index2].genome.genes

      o = ind.Individual(genome_size = genome_size, genome = self.crossover_genomes(g1, g2, genome_size))
      out.append(o)

    return out
