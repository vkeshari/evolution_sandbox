import numpy as np
from matplotlib import pyplot as plt

class FitnessHistoryGraph:

  def __init__(self, max_iterations):
    self.max_iterations = max_iterations
    self.iterations_map = {}

  def plot(self, show = False, ax = None):
    if not ax:
        ax = plt.gca()
    for k, kval in self.iterations_map.items():
      x_axis = []
      y_axis = []
      for i, ival in kval.items():
        if i > self.max_iterations:
          break
        x_axis.append(int(i))
        y_axis.append(ival.data['population']['fitness'])
      ax.step(x_axis, y_axis)
      if show:
        plt.show()

  def add_iterations(self, key, iterations):
    self.iterations_map[key] = iterations

class FitnessTimeToGraph:

  def __init__(self, max_iterations):
    self.max_iterations = max_iterations
    self.time_to_map = {}

  def add_time_to(self, key, time_to):
    self.time_to_map[key] = time_to

  def plot(self, show = False, ax = None):
    if not ax:
        ax = plt.gca()
    for k, kval in self.time_to_map.items():
      fs = []
      fvals = []
      for f, fval in kval['population'].items():
        fs.append(f)
        if fval == np.NaN or fval > self.max_iterations:
          fvals.append(0)
        else:
          fvals.append(fval)
      ax.barh(range(len(fs)), fvals)
      if show:
        plt.show()
    

class FitnessCombinedGraph:
  def __init__(self, max_iterations):
    self.max_iterations = max_iterations

    self.iterations_graph = FitnessHistoryGraph(max_iterations)
    self.time_to_graph = FitnessTimeToGraph(max_iterations)

  def add_fitness_history(self, key, fitness_history):
    self.iterations_graph.add_iterations(key, fitness_history.history['iterations'])
    self.time_to_graph.add_time_to(key, fitness_history.history['time_to'])

  def plot(self, show = False):
    fig, (ax_fit, ax_tt) = plt.subplots(2, 1, figsize = (15, 10))
    self.iterations_graph.plot(ax = ax_fit)
    self.time_to_graph.plot(ax = ax_tt)
    if show:
        plt.show()
