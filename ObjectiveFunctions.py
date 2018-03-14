import math
from Constants import SweepConstants


class ObjectiveCoefficient(object):

    def __init__(self):
        self.mu = SweepConstants.CONST_MU
        self.alpha = SweepConstants.CONST_ALPHA
        self.beta = SweepConstants.CONST_BETA
        self.lambda_ = SweepConstants.CONST_LAMBDA

    @classmethod
    def from_parameters(cls, mu, alpha, beta, lambda_):
        obj = cls()
        obj.mu = mu
        obj.alpha = alpha
        obj.beta = beta
        obj.lambda_ = lambda_
        return obj

    def __str__(self):
        return "Mu:{}_Al:{}_Be:{}_La:{}".format(self.mu, self.alpha, self.beta, self.lambda_)


def get_total_paired_distance_cost(location_matrix, locationId1, locationId2):
    """
        Distance between two stops which also includes toll cost

        Args:
            locationId1: The Location Id
            locationId2: The Location Id

        Returns:
            This returns distance
        """
    try:
        if locationId1 == locationId2:
            return 0
        return round(location_matrix[locationId1][locationId2].distance, 2)
    except Exception as ex:
        raise ex


def get_insertion_cost_1(old_time_space_info, new_time_space_info, depot, updated_orders, i, sw_job, obj_coeff):
    '''
       c_1 = alpha1 * c_11 + alpha2 * c_12;
       c_1 is used as a measure to choose the best insertion position for an unrouted customer in an exisiting route.

       Args:
               old_time_space_info: the timespace information of the current route
               new_time_space_info:  the timespace information of the new route
               depot: the depot related to the route
               updated_orders: the list of orders which includes the order to be inserted
               i: the insertion index of where the new order is inserted
               sw_job: the sweep job
               obj_coeff: Objective Coefficient parameters to be used in the construction
       Returns:

    '''
    alpha1 = obj_coeff.alpha
    alpha2 = 1 - alpha1
    return alpha1 * get_insertion_cost11(updated_orders, depot, i, sw_job, obj_coeff) + alpha2 * get_insertion_cost12(
        old_time_space_info, new_time_space_info, obj_coeff,
        sw_job.configuration.averageVehicleSpeed)


def get_insertion_cost11(new_orders, depot, insertion_index, sw_job, obj_coeff):
    '''
    c_11 = d_iu + d_uj - mu * d_ij, mu >= 0.Ye use ho rha
    customer u is being inserted between customers/orders i and j of an exisitng route.
    c_11 is a measure of savings when the above insertion is done.
    NOTE: Refer to Solomon's paper Algos for VRSPTW (1987).

    Args:
           new_orders: the list of orders which includes the order to insert as well
           depot: the depot related to the route
           insertion_index: the index of the order of where it is inserted
           sw_job:
           obj_coeff:
    Returns:
    '''

    prev_order = None
    at_order = None

    if insertion_index == 0:
        prev_order = depot.location
    else:
        prev_order = new_orders[insertion_index - 1].location.locationId

    if insertion_index + 1 >= len(new_orders):
        at_order = depot.location
    else:
        at_order = new_orders[insertion_index - 1].location.locationId

    inserting_order = new_orders[insertion_index].location.locationId

    d1 = get_total_paired_distance_cost(sw_job.locationMatrix, prev_order, inserting_order)
    d2 = get_total_paired_distance_cost(sw_job.locationMatrix, inserting_order, at_order)
    d3 = get_total_paired_distance_cost(sw_job.locationMatrix, prev_order, at_order)

    mu = obj_coeff.mu
    return d1 + d2 - mu * d3


def get_insertion_cost12(old_time_Space_info, new_time_space_info, obj_coeff, avg_vehicle_speed):
    '''

     c_12 = b_j_u - b_j;
     b_j_u: New time for service to begin at customer/order j (after insertion)
     b_j: Time for service to begin at customer/order j (before insertion)

     Args:
            old_time_Space_info: the current timespace information of the route
            new_time_space_info: the timespace information of the route after inserting the new order
            obj_coeff:
            avg_vehicle_speed:
    Returns:
            Returns the difference in time, after insertion, at j.
    '''
    return new_time_space_info.travel_time - old_time_Space_info.travel_time


def get_insertion_profit(old_time_info, new_time_info, depot, updated_orders, order_to_insert, position_to_insert,
                         sw_job, obj_coeff, vehicle):
    '''
       The get insertion cost 2
       Args:
             old_time_info: the current timespace information of the route
             new_time_info: the timespace information after inserting the order
             depot:
             updated_orders: the list of orders which also includes the order to insert
             order_to_insert: the order which is to be inserted
             position_to_insert:
             sw_job:
             obj_coeff:
             vehicle:
       Returns:
    '''
    lambda_ = obj_coeff.lambda_

    return lambda_ * order_to_insert.distance_from_depot - get_insertion_cost_1(old_time_info, new_time_info, depot,
                                                                                updated_orders, position_to_insert,
                                                                                sw_job, obj_coeff)
