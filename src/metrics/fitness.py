
class FitnessData:

  @classmethod
  def get_subgroup_fitness(cls, individuals):
    fitness = 0.0
    for i in individuals:
      fitness += i.get_fitness() / len(individuals)
    return fitness

  @classmethod
  def get_fitness_percentiles(cls, individuals):
    percentile_data = {}
    percentile_data[0] = individuals[0].get_fitness()
    for i in range(10, 100, 10):
      percentile_data[i] = individuals[int(i * len(individuals) / 100)].get_fitness()
    percentile_data[100] = individuals[-1].get_fitness()
    return percentile_data

  @classmethod
  def pretty_print_percentiles(cls, a):
    return "Min: {:.2}\t10P: {:.2}\t50P: {:.2}\t90P: {:.2}\tMax: {:.2}".format(a[0], a[10], a[50], a[90], a[100])

  @classmethod
  def get_fitness_data(cls, population):
    fitness_data = {}

    all_individuals = population.get_all_individuals(sort = True)
    fitness_data['population'] = {}
    fitness_data['population']['fitness'] = cls.get_subgroup_fitness(all_individuals)
    fitness_data['population']['percentiles'] = cls.get_fitness_percentiles(all_individuals)

    fitness_data['assignment'] = {}
    for a in range(population.genome_size):
      assignment_individuals = [i for i in all_individuals if i.assignment == a]
      fitness_data['assignment'][a] = {}
      fitness_data['assignment'][a]['fitness'] = cls.get_subgroup_fitness(assignment_individuals)
      fitness_data['assignment'][a]['percentiles'] = cls.get_fitness_percentiles(assignment_individuals)

    return fitness_data

  @classmethod
  def show_fitness(cls, population):
    all_individuals = population.get_all_individuals(sort = True)
    print("TOTAL FITNESS: {:.2}".format(cls.get_subgroup_fitness(all_individuals)))
    print("Percentiles: {}".format(cls.pretty_print_percentiles(cls.get_fitness_percentiles(all_individuals))))
    print("FITNESS BY ASSIGNMENT")
    for a in range(population.genome_size):
      assignment_individuals = [i for i in all_individuals if i.assignment == a]
      print("Assignment {}\tCount: {}\tFitness: {:.2}"
        .format(a, len(assignment_individuals), cls.get_subgroup_fitness(assignment_individuals)))
      print("Percentiles: {}".format(cls.pretty_print_percentiles(cls.get_fitness_percentiles(assignment_individuals))))

  @classmethod
  def show_stats(cls, population, show_genomes = False, show_fitness = False):
    if show_genomes:
      print("FINAL POPULATION\n")
      print(population)
    if show_fitness:
      cls.show_fitness(population)


class FitnessHistory:

  def __init__(self, time_to_fitness_values, genome_size):
    self.time_to_fitness_values = time_to_fitness_values
    self.genome_size = genome_size

    self.history = {}
    self.initialize_history(self.genome_size)

  def initialize_history(self, genome_size):
    self.history['iterations'] = {}
    self.history['time_to'] = {}
    self.history['time_to']['population'] = {}
    self.history['time_to']['assignment'] = {}
    for a in range(genome_size):
      if a not in self.history['time_to']['assignment']:
        self.history['time_to']['assignment'][a] = {}

  def update_iteration(self, iteration_no, fitness_data):
    self.history['iterations'][iteration_no] = fitness_data

  def update_time_to(self, iteration_no, fitness_data):
    for f in self.time_to_fitness_values:
      if f not in self.history['time_to']['population'] and fitness_data['population']['fitness'] > f:
        self.history['time_to']['population'][f] = iteration_no
      for a in fitness_data['assignment']:
        if f not in self.history['time_to']['assignment'][a] and fitness_data['assignment'][a]['fitness'] > f:
          self.history['time_to']['assignment'][a][f] = iteration_no

  def print_time_to(self):
    print ("TIME TO FITNESS")
    population_string = ""
    for v in self.time_to_fitness_values:
      if v not in self.history['time_to']['population']:
        it = "N/A"
      else:
        it = str(self.history['time_to']['population'][v])
      population_string += "{}: {:3}\t".format(v, it)
    print ("Population:\t" + population_string)

    for a in range(self.genome_size):
      assignment_string = ""
      for v in self.time_to_fitness_values:
        if v not in self.history['time_to']['assignment'][a]:
          it = "N/A"
        else:
          it = str(self.history['time_to']['assignment'][a][v])
        assignment_string += "{}: {:3}\t".format(v, it)
      print ("Assignment {}:\t".format(a) + assignment_string)
