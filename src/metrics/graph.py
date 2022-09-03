import numpy as np
from matplotlib import pyplot as plt

class FitnessHistoryGraph:

  def __init__(self, max_iterations):
    self.max_iterations = max_iterations
    self.iterations_map = {}

  def add_iterations(self, key, iterations):
    self.iterations_map[key] = iterations

  def plot(self, show = False, ax = None, by_assignment = False):
    if not ax:
      ax = plt.gca()
      ax.set_xlabel('Generation No. -->', fontsize = 16)

    for kindex, k in enumerate(self.iterations_map):
      kval = self.iterations_map[k]
      x_axis = []
      y_axis = []
      for i, ival in kval.items():
        if i > self.max_iterations:
          break
        x_axis.append(int(i))
        if not by_assignment:
          y_axis.append(ival.data['population']['fitness'])
        else:
          y_axis.append(ival.data['assignment'][kindex]['fitness'])
      ax.step(x_axis, y_axis, label = k)

    ax.set_title('Average Fitness over generations', fontsize = 16)
    ax.grid(visible = True)
    ax.legend(loc = 'lower right', fontsize = 12)
    ax.set_xlim(0, self.max_iterations)
    ax.set_ylabel('Fitness', fontsize = 16)
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

  def plot(self, show = False, ax = None, by_assignment = False):
    if not ax:
      ax = plt.gca()

    y_offset = 0.0
    for kindex, k in enumerate(self.time_to_map):
      kval = self.time_to_map[k]
      y_multiplier = 0.9 / len(self.time_to_map)
      y_offset += y_multiplier

      fvals = []
      text_offset = self.max_iterations / 200
      text_y = 1 - y_offset
      for f in self.time_to_fitness_values:

        if not by_assignment:
          assert(f in kval['population'])
          fval = kval['population'][f]
        else:
          assert(f in kval['assignment'][kindex])
          fval = kval['assignment'][kindex][f]

        if np.isnan(fval):
          fvals.append(self.max_iterations)
          ax.annotate('x', (text_offset, text_y), va = 'center')
        elif fval > self.max_iterations:
          fvals.append(self.max_iterations)
          ax.annotate(str(fval), (text_offset, text_y), va = 'center')
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

    ax.set_title('Median No. of generations to reach fitness', fontsize = 16)
    ax.grid(visible = True, axis = 'x')
    ax.legend(loc = 'lower right', fontsize = 12)
    ax.set_xlabel('Generation No. -->', fontsize = 16)
    ax.set_xlim(0, self.max_iterations)
    ax.set_ylabel('Fitness', fontsize = 16)
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

  def plot(self, title = '', show = False, by_assignment = False):
    fig, (ax_fit, ax_tt) = plt.subplots(2, 1, figsize = (15, 10))
    fig.suptitle(title, fontsize = 18)
    self.iterations_graph.plot(ax = ax_fit, by_assignment = by_assignment)
    self.time_to_graph.plot(ax = ax_tt, by_assignment = by_assignment)

    if show:
      plt.tight_layout()
      plt.show()
