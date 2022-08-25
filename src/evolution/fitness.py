class Fitness:

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
