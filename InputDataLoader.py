import json
from pprint import pprint
from marshmallow import Schema
from Classes import *
from Schemas import *


def data_loader(data):
    '''
    :param input json data:
    :return: instantiated classes
    '''
#Process LocationMatirx

    locationMatrix = data["locationMatrix"]
    locationMatrixFinal = []
    for location in locationMatrix:
        inner_list = []
        for distance_dict in location:
                    distanceSchema = DistanceInfoSchema()
                    distance_obj = distanceSchema.load(distance_dict)
                    inner_list.append(distance_obj)
        locationMatrixFinal.append(inner_list)

    schema = JobInputSchema()
    job_input = schema.load(data)
    job_input.locationMatrix = locationMatrixFinal













if __name__ == '__main__':
    data = json.load(open('data.json'))

    data_loader(data)