import json
import pickle
from pathlib import Path

class FitnessHistoryJSONSerializer(json.JSONEncoder):

  def default(self, o):
    if type(o).__name__ == 'FitnessHistory':
      return o.history
    if type(o).__name__ == 'FitnessData':
      return o.data


class DirectoryValidation:

  @staticmethod
  def get_directory():
    current_dir = Path.cwd()
    assert 'evolution_sandbox' == current_dir.parts[-1], \
        print ("Not run from evolution_sandbox folder. Current directory: {}".format(current_dir))
    
    return current_dir


class FitnessHistoryIO:

  def __init__(self, datetime_string):
    assert datetime_string.isdigit() and  len(datetime_string) == 14

    current_dir = DirectoryValidation.get_directory()
    self.DATA_DIR = current_dir / 'data' / datetime_string
    self.GRAPH_DIR = current_dir / 'out' / datetime_string

  def get_data_filename(self, population_size, num_assignments, num_groups, num_runs,
                        num_iterations, evolution_strategy_name, randomize_assignment_priorities,
                        randomize_assignment_sizes):
    return self.DATA_DIR / "{}_{}_{}_p{}_a{}_g{}_i{}_r{}.data".format(
        evolution_strategy_name, randomize_assignment_priorities, randomize_assignment_sizes,
        population_size, num_assignments, num_groups, num_iterations, num_runs)

  def get_graph_filename(self, population_size, num_assignments, num_groups, num_runs,
                          num_iterations, evolution_strategy_name, randomize_assignment_priorities,
                          randomize_assignment_sizes, graph_type, fit_curve):
    return self.GRAPH_DIR / "{}_{}_{}_{}_{}_p{}_a{}_g{}_i{}_r{}.png".format(
        fit_curve, graph_type, evolution_strategy_name, randomize_assignment_priorities,
        randomize_assignment_sizes, population_size, num_assignments, num_groups, num_iterations,
        num_runs)

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


class PopulationIO:

  def __init__(self, population_size, num_groups, num_assignments, evolution_strategy_name,
                randomize_assignment_priorities, randomize_assignment_sizes, datetime_string):
    self.population_size = population_size
    self.num_assignments = num_assignments
    self.num_groups = num_groups
    self.evolution_strategy_name = evolution_strategy_name
    self.randomize_assignment_priorities = randomize_assignment_priorities
    self.randomize_assignment_sizes = randomize_assignment_sizes

    current_dir = DirectoryValidation.get_directory()
    self.POPULATION_DIR = current_dir / 'population' / datetime_string
  
  def get_population_filename(self, iteration_no):
    return self.POPULATION_DIR / "{}_{}_{}_p{}_a{}_g{}_i{}.png".format(
              self.evolution_strategy_name, self.randomize_assignment_priorities,
              self.randomize_assignment_sizes, self.population_size, self.num_assignments,
              self.num_groups, iteration_no)
  

class TuningIO:

  def __init__(self, datetime_string):

    current_dir = DirectoryValidation.get_directory()
    self.TUNING_DIR = current_dir / 'tuning' / datetime_string
  
  def get_tuning_filename(self, num_runs, num_iterations, evolution_strategy_name,
                          randomize_assignment_priorities, randomize_assignment_sizes):
    return self.TUNING_DIR / "{}_{}_{}_i{}_r{}.png".format(
              evolution_strategy_name, randomize_assignment_priorities,
              randomize_assignment_sizes, num_iterations, num_runs)

