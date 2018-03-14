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
    calculate_distance_from_depot(job.orders, job.locationMatrix)
    return job


def calculate_distance_from_depot(orders, matrix):
    order_map = make_map_orders(matrix)
    return map(order_map, orders)


def make_map_orders(matrix):
    def map_order(order):
        order.fill_distance_from_Depot(matrix)
    return map_order
