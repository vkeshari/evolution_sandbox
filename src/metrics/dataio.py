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
    print (self.DATA_DIR)

  def write_fitness_history(self, filename, fitness_history):
    full_filename = self.DATA_DIR + filename
    with open(full_filename, 'wb+') as f:
      pickle.dump(fitness_history, f)
      print("Fitness History written to {}".format(full_filename))

  def read_fitness_history(self, filename, show = False):
    full_filename = self.DATA_DIR + filename
    with open(full_filename, 'rb') as f:
      fitness_history = pickle.load(f)
      print("Fitness History read from {}".format(full_filename))

    if show:
      print(json.dumps(fitness_history, cls = FitnessHistoryJSONSerializer, indent = 2, sort_keys = True))
    return fitness_history
