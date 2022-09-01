from enum import Enum
import numpy as np

class FitnessUtil:

  @staticmethod
  def get_subgroup_fitness(individuals, expected_size):
    fitness = 0.0
    for i in individuals:
      fitness += i.get_fitness() / expected_size
    return fitness

  @staticmethod
  def get_fitness_percentiles(individuals):
    percentile_data = {}
    percentile_data[0] = individuals[0].get_fitness()
    for i in range(10, 100, 10):
      percentile_data[i] = individuals[int(i * len(individuals) / 100)].get_fitness()
    percentile_data[100] = individuals[-1].get_fitness()
    return percentile_data

  @staticmethod
  def pretty_print_percentiles(a):
    return "Min: {:.2}\t10P: {:.2}\t50P: {:.2}\t90P: {:.2}\tMax: {:.2}".format(a[0], a[10], a[50], a[90], a[100])

  @staticmethod
  def show_population_stats(population, show_genomes = False, show_fitness = False):
    if show_genomes:
      print("FINAL POPULATION\n")
      print(population)
    if show_fitness:
      FitnessData.from_population(population).print_fitness_data()


class FitnessData:

  def __init__(self, genome_size):
    self.genome_size = genome_size

    self.initialize_data(genome_size)

  def initialize_data(self, genome_size):
    self.data = {}
    self.data['population'] = {}
    self.data['population']['percentiles'] = {}
    self.data['assignment'] = {}
    for a in range(self.genome_size):
      self.data['assignment'][a] = {}
      self.data['assignment'][a]['percentiles'] = {}

  @staticmethod
  def from_population(population):
    fitness_data = FitnessData(genome_size = population.genome_size)

    all_individuals = population.get_all_individuals(sort = True)
    fitness_data.data['population']['fitness'] = FitnessUtil.get_subgroup_fitness(all_individuals, population.population_size)
    fitness_data.data['population']['percentiles'] = FitnessUtil.get_fitness_percentiles(all_individuals)

    for a in range(population.genome_size):
      assignment_individuals = [i for i in all_individuals if i.assignment == a]
      fitness_data.data['assignment'][a]['fitness'] = FitnessUtil.get_subgroup_fitness(assignment_individuals, population.assignment_sizes[a])
      fitness_data.data['assignment'][a]['percentiles'] = FitnessUtil.get_fitness_percentiles(assignment_individuals)

    return fitness_data

  def print_fitness_data(self):
    print("FITNESS")
    print("POPULATION:\tFitness: {:.2}".format(self.data['population']['fitness']))
    print(FitnessUtil.pretty_print_percentiles(self.data['population']['percentiles']))
    for a in range(self.genome_size):
      print("ASSIGNMENT {}:\tFitness: {:.2}".format(a, self.data['assignment'][a]['fitness']))
      print(FitnessUtil.pretty_print_percentiles(self.data['assignment'][a]['percentiles']))


class FitnessHistory:

  def __init__(self, time_to_fitness_values, genome_size):
    self.time_to_fitness_values = time_to_fitness_values
    self.genome_size = genome_size

    self.initialize_history(self.genome_size)

  def initialize_history(self, genome_size):
    self.history = {}
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
      if f not in self.history['time_to']['population'] and fitness_data.data['population']['fitness'] > f:
        self.history['time_to']['population'][f] = iteration_no
      for a in fitness_data.data['assignment']:
        if f not in self.history['time_to']['assignment'][a] and fitness_data.data['assignment'][a]['fitness'] > f:
          self.history['time_to']['assignment'][a][f] = iteration_no

  def print_time_to(self):
    print("TIME TO FITNESS")
    population_string = ""
    for v in self.time_to_fitness_values:
      if v not in self.history['time_to']['population']:
        it = "N/A"
      else:
        it = str(self.history['time_to']['population'][v])
      population_string += "{}: {:3}\t".format(v, it)
    print("Population:\t" + population_string)

    for a in range(self.genome_size):
      assignment_string = ""
      for v in self.time_to_fitness_values:
        if v not in self.history['time_to']['assignment'][a]:
          it = "N/A"
        else:
          it = str(self.history['time_to']['assignment'][a][v])
        assignment_string += "{}: {:3}\t".format(v, it)
      print("Assignment {}:\t".format(a) + assignment_string)


class AggregateType(Enum):
  AVERAGE = 0
  STDEV = 1
  MIN = 2
  MAX = 3
  MEDIAN = 4
  P10 = 5
  P20 = 6
  P80 = 7
  P90 = 8


class FitnessHistoryAggregate:

  MINIMUM_FRACTION_FOR_ORDINAL_METRIC = 0.5

  @classmethod
  def get_aggregate(cls, vals, num_runs, aggregate_type):
    if len(vals) == 0:
      return np.NaN

    if aggregate_type == AggregateType.AVERAGE:
      return np.mean(vals)
    elif aggregate_type == AggregateType.STDEV:
      return np.std(vals)

    if len(vals) < cls.MINIMUM_FRACTION_FOR_ORDINAL_METRIC * num_runs:
      return np.NaN

    if aggregate_type == AggregateType.MIN:
      return sorted(vals)[0]
    elif aggregate_type == AggregateType.MAX:
      return sorted(vals)[-1]
    elif aggregate_type == AggregateType.MEDIAN:
      return sorted(vals)[int(0.5 * len(vals))]
    elif aggregate_type == AggregateType.P10:
      return sorted(vals)[int(0.1 * len(vals))]
    elif aggregate_type == AggregateType.P20:
      return sorted(vals)[int(0.2 * len(vals))]
    elif aggregate_type == AggregateType.P80:
      return sorted(vals)[int(0.8 * len(vals))]
    elif aggregate_type == AggregateType.P90:
      return sorted(vals)[int(0.9 * len(vals))]

  @classmethod
  def get_aggregated_fitness(cls, fitness_history_runs, fitness_aggregate_type = AggregateType.AVERAGE, time_to_aggregate_type = AggregateType.MEDIAN):
    num_runs = len(fitness_history_runs)
    reference = fitness_history_runs[1]
    aggregate = FitnessHistory(reference.time_to_fitness_values, reference.genome_size)

    for i in reference.history['iterations']:
      aggregated_data = FitnessData(reference.genome_size)

      fitness_vals = [r.history['iterations'][i].data['population']['fitness'] for r in fitness_history_runs.values()]
      aggregated_data.data['population']['fitness'] = FitnessHistoryAggregate.get_aggregate(fitness_vals, num_runs, fitness_aggregate_type)

      aggregated_data.data['population']['percentiles'] = {}
      for p in range(0, 101, 10):
        fitness_vals = [r.history['iterations'][i].data['population']['percentiles'][p] for r in fitness_history_runs.values()]
        aggregated_data.data['population']['percentiles'][p] = FitnessHistoryAggregate.get_aggregate(fitness_vals, num_runs, fitness_aggregate_type)

      for a in range(reference.genome_size):
        fitness_vals = [r.history['iterations'][i].data['assignment'][a]['fitness'] for r in fitness_history_runs.values()]
        aggregated_data.data['assignment'][a]['fitness'] = FitnessHistoryAggregate.get_aggregate(fitness_vals, num_runs, fitness_aggregate_type)
        
        aggregated_data.data['assignment'][a]['percentiles'] = {}
        for p in range(0, 101, 10):
          fitness_vals = [r.history['iterations'][i].data['assignment'][a]['percentiles'][p] for r in fitness_history_runs.values()]
          aggregated_data.data['assignment'][a]['percentiles'][p] = FitnessHistoryAggregate.get_aggregate(fitness_vals, num_runs, fitness_aggregate_type)

      aggregate.update_iteration(i, aggregated_data)

    for f in reference.time_to_fitness_values:
      fitness_vals = [r.history['time_to']['population'][f] for r in fitness_history_runs.values() if f in r.history['time_to']['population']]
      aggregate.history['time_to']['population'][f] = FitnessHistoryAggregate.get_aggregate(fitness_vals, num_runs, time_to_aggregate_type)

      for a in range(reference.genome_size):
        fitness_vals = [r.history['time_to']['assignment'][a][f] for r in fitness_history_runs.values() if f in r.history['time_to']['assignment'][a]]
        aggregate.history['time_to']['assignment'][a][f] = FitnessHistoryAggregate.get_aggregate(fitness_vals, num_runs, time_to_aggregate_type)

    return aggregate
