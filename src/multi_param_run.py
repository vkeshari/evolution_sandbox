import evolution_runner as evo
import data_viewer as dv
import params as par
from metrics import fitness as fit

def validate_params():
  par.LoopParams.MULTI_PARAMS = True

  par.WorldParams.NUM_RUNS = par.MultiParams.NUM_RUNS
  par.WorldParams.NUM_GENERATIONS = par.MultiParams.NUM_ITERATIONS

  par.PopulationParams.POPULATION_SIZE = par.MultiParams.POPULATION_SIZE
  par.PopulationParams.NUM_GROUPS = par.MultiParams.NUM_ASSIGNMENTS
  par.PopulationParams.NUM_ASSIGNMENTS = par.MultiParams.NUM_ASSIGNMENTS

  par.FitnessParams.TIME_TO_FITNESS_VALUES = par.MultiParams.TIME_TO_FITNESS_VALUES
  par.AggregationParams.FITNESS_AGGREGATION_TYPE = fit.AggregateType.AVERAGE
  par.AggregationParams.TIME_AGGREGATION_TYPE = fit.AggregateType.MEDIAN

  par.DebugParams.SHOW_RUN_STATUS = True
  par.DebugParams.SHOW_RUN_STATUS_DELAY = par.MultiParams.SHOW_RUN_STATUS_DELAY
  par.DebugParams.SHOW_RUN_TIME_SUMMARY = True
  par.DebugParams.SHOW_ITERATIONS = False
  par.DebugParams.NUM_CHECKPOINTS = 2
  par.DebugParams.SAVE_GENOMES_AT_CHECKPOINTS = False
  par.DebugParams.SHOW_RUN_GENOMES = False
  par.DebugParams.SHOW_RUN_FITNESS = False
  par.DebugParams.SHOW_STATS_AT_CHECKPOINTS = False
  par.DebugParams.SHOW_AGGREGATED_FITNESS = False
  par.DebugParams.WRITE_AGGREGATED_FITNESS = True

  par.DataViewerParams.POPULATION_SIZE = par.MultiParams.POPULATION_SIZE
  par.DataViewerParams.NUM_ASSIGNMENTS = par.MultiParams.NUM_ASSIGNMENTS
  par.DataViewerParams.NUM_RUNS = par.MultiParams.NUM_RUNS
  par.DataViewerParams.NUM_ITERATIONS = par.MultiParams.NUM_ITERATIONS

  par.GraphTypes.BY_EVOLUTION_STRATEGY = True
  par.GraphTypes.BY_ASSIGNMENT_RANDOMIZATION = True
  par.GraphTypes.BY_ASSIGNMENT = False

  par.GraphParams.TIME_TO_FITNESS_VALUES = par.MultiParams.TIME_TO_FITNESS_VALUES
  par.GraphParams.MAX_ITERATIONS = par.MultiParams.NUM_ITERATIONS
  par.GraphParams.FIT_CURVE = False
  par.GraphParams.SHOW_GRAPHS = False
  par.GraphParams.SAVE_GRAPHS = True
  par.GraphParams.ALL_GRAPHS = True


def multi_param_run():
  validate_params()

  datetime_string = evo.evolution_runner()
  dv.data_viewer(datetime_string = datetime_string)

if __name__ == "__main__":
  multi_param_run()
