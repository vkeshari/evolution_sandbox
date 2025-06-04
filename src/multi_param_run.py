import evolution_runner as evo
import data_viewer as dv
import params as par

def validate_params():
  assert par.LoopParams.MULTI_PARAMS and par.GraphParams.ALL_GRAPHS
  assert par.DebugParams.WRITE_AGGREGATED_FITNESS
  assert par.GraphParams.SAVE_GRAPHS

  assert par.WorldParams.NUM_RUNS == par.DataViewerParams.NUM_RUNS
  assert par.WorldParams.NUM_GENERATIONS == par.DataViewerParams.NUM_ITERATIONS
  assert par.PopulationParams.POPULATION_SIZE == par.DataViewerParams.POPULATION_SIZE
  assert par.PopulationParams.NUM_ASSIGNMENTS == par.DataViewerParams.NUM_ASSIGNMENTS


def multi_param_run():
  validate_params()

  datetime_string = evo.evolution_runner()
  dv.data_viewer(datetime_string = datetime_string)

if __name__ == "__main__":
  multi_param_run()
