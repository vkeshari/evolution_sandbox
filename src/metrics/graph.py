import numpy as np
from matplotlib import pyplot as plt

class FitnessHistoryGraph:

  def __init__(self, max_iterations):
    self.max_iterations = max_iterations
    self.iterations_map = {}

  def add_iterations(self, key, iterations):
    self.iterations_map[key] = iterations

  def plot(self, show = False, ax = None):
    if not ax:
      ax = plt.gca()
      ax.set_xlabel('Generation No. -->')

    for k, kval in self.iterations_map.items():
      x_axis = []
      y_axis = []
      for i, ival in kval.items():
        if i > self.max_iterations:
          break
        x_axis.append(int(i))
        y_axis.append(ival.data['population']['fitness'])
      ax.step(x_axis, y_axis, label = k)

    ax.set_title('Average Fitness over generations')
    ax.grid(visible = True)
    ax.legend(loc = 'lower right')
    ax.set_xlim(0, self.max_iterations)
    ax.set_ylabel('Fitness')
    ax.set_ylim(0.5, 1.0)

    if show:
      plt.tight_layout()
      plt.show()

class FitnessTimeToGraph:

  def __init__(self, max_iterations, time_to_fitness_values):
    self.max_iterations = max_iterations
    self.time_to_fitness_values = time_to_fitness_values
    self.time_to_map = {}

  def add_time_to(self, key, time_to):
    self.time_to_map[key] = time_to

  def plot(self, show = False, ax = None):
    if not ax:
      ax = plt.gca()

    y_offset = 0.0
    for k, kval in self.time_to_map.items():
      y_multiplier = 0.9 / len(self.time_to_map)
      y_offset += y_multiplier

      fvals = []
      text_offset = self.max_iterations / 200
      text_y = 1 - y_offset
      for f in self.time_to_fitness_values:
        assert(f in kval['population'])

        fval = kval['population'][f]
        if np.isnan(fval) or fval > self.max_iterations:
          fvals.append(0.5)
        else:
          fvals.append(fval)
          ax.annotate(str(fval), (fval + text_offset, text_y), va = 'center')
        text_y += 1

      y_pos = [y + 1 - y_offset for y in range(len(self.time_to_fitness_values))]
      ax.barh(y_pos, fvals, height = y_multiplier, label = k)
      for v in fvals:
        if v == 0:
          l = 'N/A'
        else:
          l = str(v)

    ax.set_title('Median No. of generations to reach fitness')
    ax.grid(visible = True, axis = 'x')
    ax.legend(loc = 'lower right')
    ax.set_xlabel('Generation No. -->')
    ax.set_xlim(0, self.max_iterations)
    ax.set_ylabel('Fitness')
    ax.set_ylim(0, len(self.time_to_fitness_values))
    ax.set_yticks(range(len(self.time_to_fitness_values)), labels = self.time_to_fitness_values)

    if show:
      plt.tight_layout()
      plt.show()
    

class FitnessCombinedGraph:
  def __init__(self, max_iterations, time_to_fitness_values):
    self.max_iterations = max_iterations

    self.iterations_graph = FitnessHistoryGraph(max_iterations)
    self.time_to_graph = FitnessTimeToGraph(max_iterations, time_to_fitness_values)

  def add_fitness_history(self, key, fitness_history):
    self.iterations_graph.add_iterations(key, fitness_history.history['iterations'])
    self.time_to_graph.add_time_to(key, fitness_history.history['time_to'])

  def plot(self, show = False):
    fig, (ax_fit, ax_tt) = plt.subplots(2, 1, figsize = (15, 10))
    self.iterations_graph.plot(ax = ax_fit)
    self.time_to_graph.plot(ax = ax_tt)

    if show:
      plt.tight_layout()
      plt.show()
