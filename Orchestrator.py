import InputDataLoader as InputDataLoader
from ObjectiveFunctions import ObjectiveCoefficient
from SectorClusteringParameter import SectorClusteringParameter
import SweepInsertion
from Constants import SectorClusteringConstants, SweepObjectiveConstants
from Schemas import OutputSchema
import json
import time


if __name__ == '__main__':
    start_time = time.time()
    job = InputDataLoader.data_loader()
    print("--- %s seconds taken for reading input data.---" % (time.time() - start_time))

    clustering_parameters = SectorClusteringParameter(SectorClusteringConstants.CONST_ANGULAR_SEED_IN_RADIAN,
                                                      SectorClusteringConstants.CONST_ANGULAR_SECTOR_SIZE_IN_RADIAN,
                                                      SectorClusteringConstants.CONST_ANGULAR_STEP_SIZE_IN_RADIAN,
                                                      SectorClusteringConstants.CONST_SECTOR_CLUSTERING_METHOD)

    objective_coefficients = ObjectiveCoefficient(SweepObjectiveConstants.CONST_MU,
                                                  SweepObjectiveConstants.CONST_ALPHA,
                                                  SweepObjectiveConstants.CONST_BETA,
                                                  SweepObjectiveConstants.CONST_LAMBDA)

    start_time = time.time()
    output = SweepInsertion.generate_routes(job, clustering_parameters, objective_coefficients)
    print("--- %s seconds taken for running the engine.---" % (time.time() - start_time))

    start_time = time.time()
    output_schema = OutputSchema()
    data = output_schema.dump(output)
    output_data_serialized = json.dumps(data)
    print(output_data_serialized)
    print("--- %s seconds taken for writing output data.---" % (time.time() - start_time))
    print("Finished")
