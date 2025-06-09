import numpy as np
from matplotlib import pyplot as plt, cm
from matplotlib.patches import Rectangle
from scipy import optimize as opt

class FitnessHistoryGraph:

  LINE_ALPHA_STEP = 0.6
  LINE_ALPHA_FIT = 0.8
  LINE_WIDTH = 5
  SCATTER_ALPHA = 0.1
  SCATTER_SIZE = 50

  @staticmethod
  def exp_curve_fit_func(x, a, b, c):
    return a + b * np.exp(-x / c)

  def __init__(self, max_iterations):
    self.max_iterations = max_iterations
    self.iterations_map = {}

  def add_iterations(self, key, iterations):
    self.iterations_map[key] = iterations

  def plot(self, show = False, ax = None, by_assignment = False, fit_curve = False,
           savefile = None):
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
      if fit_curve:
        (a, b, c), _ = opt.curve_fit(self.exp_curve_fit_func, x_axis, y_axis)
        y_fit = [self.exp_curve_fit_func(x, a, b, c) for x in x_axis]
        ax.scatter(x_axis, y_axis, s = self.SCATTER_SIZE, alpha = self.SCATTER_ALPHA)
        ax.plot(x_axis, y_fit, alpha = self.LINE_ALPHA_FIT, linewidth = self.LINE_WIDTH, label = k)
      else:
        ax.step(x_axis, y_axis, alpha = self.LINE_ALPHA_STEP, linewidth = self.LINE_WIDTH,
                label = k)

    ax.set_title('Average Fitness over generations', fontsize = 16)
    ax.grid(visible = True)
    ax.legend(loc = 'lower right', fontsize = 12)
    ax.set_xlim(0, self.max_iterations)
    ax.set_ylabel('Fitness', fontsize = 16)
    ax.set_ylim(0.5, 1.0)

    if show:
      plt.tight_layout()
      plt.show()
    if savefile:
      plt.tight_layout()
      savefile.parent.mkdir(exist_ok = True, parents = True)
      plt.savefig(savefile)
      print ("Graph written to: {}".format(savefile))
      plt.close()


class FitnessTimeToGraph:

  ALPHA = 0.8

  def __init__(self, max_iterations, time_to_fitness_values):
    self.max_iterations = max_iterations
    self.time_to_fitness_values = time_to_fitness_values
    self.time_to_map = {}

  def add_time_to(self, key, time_to):
    self.time_to_map[key] = time_to

  def plot(self, show = False, ax = None, by_assignment = False, savefile = None):
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
      ax.barh(y_pos, fvals, height = y_multiplier, label = k, alpha = self.ALPHA)
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
    if savefile:
      plt.tight_layout()
      savefile.parent.mkdir(exist_ok = True, parents = True)
      plt.savefig(savefile)
      print ("Graph written to: {}".format(savefile))
      plt.close()
    

class FitnessCombinedGraph:
  def __init__(self, max_iterations, time_to_fitness_values):
    self.max_iterations = max_iterations

    self.iterations_graph = FitnessHistoryGraph(max_iterations)
    self.time_to_graph = FitnessTimeToGraph(max_iterations, time_to_fitness_values)

  def add_fitness_history(self, key, fitness_history):
    self.iterations_graph.add_iterations(key, fitness_history.history['iterations'])
    self.time_to_graph.add_time_to(key, fitness_history.history['time_to'])

  def plot(self, title = '', show = False, by_assignment = False, fit_curve = False,
           savefile = None):
    fig, (ax_fit, ax_tt) = plt.subplots(2, 1, figsize = (15, 10))
    fig.suptitle(title, fontsize = 18)
    self.iterations_graph.plot(ax = ax_fit, by_assignment = by_assignment, fit_curve = fit_curve)
    self.time_to_graph.plot(ax = ax_tt, by_assignment = by_assignment)

    if show:
      plt.tight_layout()
      plt.show()
    if savefile:
      plt.tight_layout()
      savefile.parent.mkdir(exist_ok = True, parents = True)
      plt.savefig(savefile)
      print ("Graph written to: {}".format(savefile))
      plt.close()


class PopulationGraph:
  def __init__(self, population):
    self.population = population
  
  def plot(self, title_text = '', show = False, savefile = None):
    group_sizes = [len(g.individuals) for g in self.population.groups]
    actual_population = sum(group_sizes)

    genome_size = self.population.groups[0].genome_size
    graph_aspect_ratio = min(4, actual_population / genome_size)

    resolution = tuple([10.8, 10.8 / graph_aspect_ratio])
    fig, ax = plt.subplots(figsize = resolution)

    ax.set_title(title_text)
    ax.set_xlabel('<-- Individuals -->', fontsize = 'medium')
    ax.set_ylabel('Genes', fontsize = 'medium')
    
    xticks = [0]
    cum_gs = 0
    for gs in group_sizes:
      cum_gs += gs
      xticks.append(cum_gs)
    ax.set_xticks(xticks)
    xgrid = range(0, actual_population + 1)
    ax.set_xticks(xgrid, minor = True)

    yticks = [0, genome_size]
    ax.set_yticks(yticks)
    ygrid = range(0, genome_size + 1)
    ax.set_yticks(ygrid, minor = True)
    ax.grid(True, which = 'both', axis = 'both', alpha = 0.5)

    flat_individuals = []
    for g in self.population.groups:
      for i in g.individuals:
        flat_individuals.append({
            'genes': i.get_genes(),
            'assignment': i.assignment,
            'fitness': i.get_fitness()})
    
    shaped_genes = np.transpose(np.array([i['genes'] for i in flat_individuals]))
    im = ax.imshow(shaped_genes, origin = 'upper', aspect = 1, vmin = 0, vmax = 1,
                    extent = [0, actual_population, genome_size, 0])
    for xt in xticks:
      plt.axvline(x = xt, ymin = 0, ymax = 1, color = 'white', linewidth = 1, alpha = 0.8)
    
    if len(self.population.assignment_priorities) > 1:
      for i, ind in enumerate(flat_individuals):
        ass = ind['assignment']
        if ass > -1:
          ax.add_patch(Rectangle((i, ass), height = 1, width = 1, edgecolor = 'red',
                                  linewidth = 2, alpha = 1.0, fill = False))
    
    cbar = plt.colorbar(im, shrink = 0.75, ticks = np.linspace(0, 1, 6))
    cbar.set_label('Individual Fitness', size = 'medium')
    cbar.ax.tick_params(labelsize = 'medium')

    if show:
      fig.tight_layout()
      plt.show()
    if savefile:
      fig.tight_layout()
      savefile.parent.mkdir(exist_ok = True, parents = True)
      fig.savefig(savefile)
      print ("Population Graph written to: {}".format(savefile))
      plt.close()


class TuningGraph:

  FITNESS_SCALE_FACTOR = 0.7

  def __init__(self, xy_vals, type = ''):
    assert type in ['PG', 'GA']
    self.type = type

    self.xy_vals = xy_vals
    [xs, ys] = list(zip(*xy_vals))
    self.xs = sorted(list(set(xs)))
    self.ys = sorted(list(set(ys)))
    self.xstep = self.xs[-1] - self.xs[-2]
    self.ystep = self.ys[-1] - self.ys[-2]

  def plot(self, graph_vals, title_text = '', show = False, savefile = None):

    resolution = tuple([7.2, 7.2])
    fig, ax = plt.subplots(figsize = resolution)

    ax.set_title(title_text, fontsize = 'medium')
    if self.type == 'PG':
      ax.set_xlabel("Population Size")
      ax.set_ylabel("No. of Groups / Assignments")
    elif self.type == 'GA':
      ax.set_xlabel("No. of Groups")
      ax.set_ylabel("No. of Assignments")

    xticks = list(range(0, self.xs[-1] + 1, self.xstep))
    ax.set_xticks(xticks)
    yticks = list(range(0, self.ys[-1] + 1, self.ystep))
    ax.set_yticks(yticks)
    ax.grid(True, which = 'major', axis = 'both', alpha = 0.5)

    xlim = self.xs[-1] + self.xstep
    ylim = self.ys[-1] + self.ystep
    ax.set_xlim([0, xlim])
    ax.set_ylim([0, ylim])

    text_shift = int(xlim / 50)
    for [x, y], f in graph_vals['final_fitness'].items():
      scaled_fitness = (f - self.FITNESS_SCALE_FACTOR) / (1.0 - self.FITNESS_SCALE_FACTOR)
      plt.plot(x, y, marker = 'o', markersize = 10, alpha = 0.6,
                color = cm.gnuplot2_r(scaled_fitness))
      plt.text(x = x + text_shift, y = y, s = "{fit:.2f}".format(fit = f), fontsize = 'small',
                verticalalignment = 'center')

    if show:
      fig.tight_layout()
      plt.show()
    if savefile:
      fig.tight_layout()
      savefile.parent.mkdir(exist_ok = True, parents = True)
      fig.savefig(savefile)
      print ("Tuning Graph written to: {}".format(savefile))
      plt.close()
