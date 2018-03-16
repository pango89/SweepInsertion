import InputDataLoader as InputDataLoader
from ObjectiveFunctions import ObjectiveCoefficient
from SectorClusteringParameter import SectorClusteringParameter
import SweepInsertion
from Constants import SectorClusteringConstants, SweepObjectiveConstants
from Schemas import RouteSchema
from marshmallow import pprint
import json

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
    print(len(routes))
    route_schema = RouteSchema()
    data = route_schema.dump(routes,many=True)
    output = json.dumps(data)
    print(output)
   # pprint(data)


    print("Finished")
