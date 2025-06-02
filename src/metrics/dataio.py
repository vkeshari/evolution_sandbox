from pathlib import Path
import json
import pickle

class FitnessHistoryJSONSerializer(json.JSONEncoder):

  def default(self, o):
    if type(o).__name__ == 'FitnessHistory':
      return o.history
    if type(o).__name__ == 'FitnessData':
      return o.data

class FitnessHistoryIO:

  def __init__(self):
    current_dir = Path.cwd()
    if not 'evolution_sandbox' == current_dir.parts[-1]:
      print ("Not run from evolution_sandbox folder. Current directory: {}".format(current_dir))
    self.DATA_DIR = current_dir / 'data'
    print ("Data Directory: " + str(self.DATA_DIR))
    self.GRAPH_DIR = current_dir / 'out'
    print ("Graph Directory: " + str(self.GRAPH_DIR))

  def get_data_filename(self, population_size, num_assignments, num_runs, num_iterations, 
                        evolution_strategy_name, randomize_assignment_priorities,
                        randomize_assignment_sizes, datetime_string):
    return self.DATA_DIR / datetime_string / "{}_{}_{}_p{}_a{}_i{}_r{}.data".format(
        evolution_strategy_name, randomize_assignment_priorities, randomize_assignment_sizes,
        population_size, num_assignments, num_iterations, num_runs)

  def get_graph_filename(self, population_size, num_assignments, num_runs, num_iterations, 
                          evolution_strategy_name, randomize_assignment_priorities,
                          randomize_assignment_sizes, datetime_string, graph_type, fit_curve):
    return self.GRAPH_DIR / datetime_string / "{}_{}_{}_p{}_a{}_i{}_r{}_{}_{}.png".format(
        fit_curve, graph_type, evolution_strategy_name, randomize_assignment_priorities,
        randomize_assignment_sizes, population_size, num_assignments, num_iterations, num_runs)

  def write_fitness_history(self, filename, fitness_history):
    filename.parent.mkdir(exist_ok = True, parents = True)
    with open(filename, 'wb+') as f:
      pickle.dump(fitness_history, f)
      print("Fitness History written to {}".format(filename))

  def read_fitness_history(self, filename, show = False):
    with open(filename, 'rb') as f:
      fitness_history = pickle.load(f)
      print("Fitness History read from {}".format(filename))

    if show:
      print(json.dumps(fitness_history, cls = FitnessHistoryJSONSerializer, indent = 2,
                       sort_keys = True))
    return fitness_history
