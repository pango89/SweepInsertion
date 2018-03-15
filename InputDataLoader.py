import json
from Schemas import JobInputSchema


def data_loader():
    """
    This method loads the input data into Job.

    Args:

    Returns:
        This returns a Job Object.
    """
    schema = JobInputSchema()
    input_data = json.load(open('data.json'))
    job = schema.load(input_data)
    fill_distance_from_depot(job.orders, job.locationMatrix)
    return job


def fill_distance_from_depot(orders, matrix):
    for order in orders:
        order.fill_distance_from_depot(matrix)
