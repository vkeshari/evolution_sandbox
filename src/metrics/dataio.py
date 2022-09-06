import json
import pickle
import os

class FitnessHistoryJSONSerializer(json.JSONEncoder):

  def default(self, o):
    if type(o).__name__ == 'FitnessHistory':
      return o.history
    if type(o).__name__ == 'FitnessData':
      return o.data

class FitnessHistoryIO:

  def __init__(self):
    current_dir = os.getcwd()
    i = current_dir.rfind('/evolution_sandbox')
    assert i >= 0, "Not run from evolution_sandbox folder. Current directory: {}".format(current_dir)
    self.DATA_DIR = current_dir[: i + 18] + "/data/"
    print ("Data Directory: " + self.DATA_DIR)
    self.GRAPH_DIR = current_dir[: i + 18] + "/out/"
    print ("Graph Directory: " + self.GRAPH_DIR)

  def get_data_filename(self, population_size, num_assignments, num_runs, num_iterations, 
                        evolution_strategy_name, randomize_assignment_priorities, randomize_assignment_sizes,
                        datetime_string):
    return self.DATA_DIR + "Run_{}_{}_{}_{}_p{}_a{}_i{}_r{}.data".format(datetime_string, 
        evolution_strategy_name, randomize_assignment_priorities, randomize_assignment_sizes,
        population_size, num_assignments, num_iterations, num_runs)

  def get_graph_filename(self, population_size, num_assignments, num_runs, num_iterations, 
                          evolution_strategy_name, randomize_assignment_priorities, randomize_assignment_sizes,
                          datetime_string, graph_type, fit_curve):
    return self.GRAPH_DIR + "Graph_{}_{}_{}_{}_p{}_a{}_i{}_r{}_{}_{}.png".format(datetime_string, 
        evolution_strategy_name, randomize_assignment_priorities, randomize_assignment_sizes,
        population_size, num_assignments, num_iterations, num_runs, graph_type, fit_curve)

  def write_fitness_history(self, filename, fitness_history):
    with open(filename, 'wb+') as f:
      pickle.dump(fitness_history, f)
      print("Fitness History written to {}".format(filename))

  def read_fitness_history(self, filename, show = False):
    with open(filename, 'rb') as f:
      fitness_history = pickle.load(f)
      print("Fitness History read from {}".format(filename))

    if show:
      print(json.dumps(fitness_history, cls = FitnessHistoryJSONSerializer, indent = 2, sort_keys = True))
    return fitness_history
