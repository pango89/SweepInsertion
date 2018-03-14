import InputDataLoader as InputDataLoader
from ObjectiveFunctions import ObjectiveCoefficient
from SectorClusteringParameter import SectorClusteringParameter
import SweepInsertion
from Constants import SectorClusteringConstants, SweepObjectiveConstants

if __name__ == '__main__':
    job = InputDataLoader.data_loader()

    clustering_parameters = SectorClusteringParameter(SectorClusteringConstants.CONST_ANGULAR_SEED_IN_RADIAN,
                                                      SectorClusteringConstants.CONST_ANGULAR_SECTOR_SIZE_IN_RADIAN,
                                                      SectorClusteringConstants.CONST_ANGULAR_STEP_SIZE_IN_RADIAN,
                                                      SectorClusteringConstants.CONST_SECTOR_CLUSTERING_METHOD)

    objective_coefficients = ObjectiveCoefficient(SweepObjectiveConstants.CONST_MU,
                                                  SweepObjectiveConstants.CONST_ALPHA,
                                                  SweepObjectiveConstants.CONST_BETA,
                                                  SweepObjectiveConstants.CONST_LAMBDA)

    routes = SweepInsertion.generate_routes(job, clustering_parameters, objective_coefficients)
    print("Finished")
