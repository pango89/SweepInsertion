class ObjectiveCoefficient(object):

    def __init__(self, mu, alpha, beta, lambda_):
        self.mu = mu
        self.alpha = alpha
        self.beta = beta
        self.lambda_ = lambda_

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


def get_insertion_cost_1(old_time_space_info, new_time_space_info, depot, updated_orders, i, matrix, coefficient):
    """
       c_1 = alpha1 * c_11 + alpha2 * c_12;
       c_1 is used as a measure to choose the best insertion position for an un-routed customer in an existing route.

       Args:
               old_time_space_info: the time space information of the current route
               new_time_space_info:  the time space information of the new route
               depot: the depot related to the route
               updated_orders: the list of orders which includes the order to be inserted
               i: the insertion index of where the new order is inserted
               matrix: location matrix
               coefficient: Objective Coefficient parameters to be used in the construction
       Returns:

    """
    alpha1 = coefficient.alpha
    alpha2 = 1 - alpha1
    return (alpha1 * get_insertion_cost11(updated_orders, depot, i, matrix,
                                          coefficient) + alpha2 * get_insertion_cost12(
        old_time_space_info, new_time_space_info))


def get_insertion_cost11(new_orders, depot, insertion_index, matrix, coefficient):
    """
    c_11 = d_iu + d_uj - mu * d_ij, mu >= 0.
    customer u is being inserted between customers/orders i and j of an existing route.
    c_11 is a measure of savings when the above insertion is done.
    NOTE: Refer to Solomon's paper Algorithms for VRSPTW (1987).

    Args:
           new_orders: the list of orders which includes the order to insert as well
           depot: the depot related to the route
           insertion_index: the index of the order of where it is inserted
           matrix:
           coefficient:
    Returns:
    """

    if insertion_index == 0:
        prev_order_location_id = depot.location.locationId
    else:
        prev_order_location_id = new_orders[insertion_index - 1].location.locationId

    if insertion_index + 1 >= len(new_orders):
        at_order_location_id = depot.location.locationId
    else:
        at_order_location_id = new_orders[insertion_index - 1].location.locationId

    inserting_order_location_id = new_orders[insertion_index].location.locationId

    d1 = matrix[prev_order_location_id][inserting_order_location_id].distance
    d2 = matrix[inserting_order_location_id][at_order_location_id].distance
    d3 = matrix[prev_order_location_id][at_order_location_id].distance

    mu = coefficient.mu
    return d1 + d2 - mu * d3


def get_insertion_cost12(old_time_space_info, new_time_space_info):
    """
     c_12 = b_j_u - b_j;
     b_j_u: New time for service to begin at customer/order j (after insertion)
     b_j: Time for service to begin at customer/order j (before insertion)

     Args:
            old_time_space_info: the current time  space information of the route
            new_time_space_info: the time space information of the route after inserting the new order

    Returns:
            Returns the difference in time, after insertion, at j.
    """
    return new_time_space_info.travel_time - old_time_space_info.travel_time


def get_insertion_profit(old_time_space_info, new_time_space_info, depot, updated_orders, order_to_insert,
                         position_to_insert,
                         matrix, coefficient):
    """
       The get insertion cost 2
       Args:
             old_time_space_info: the current time space information of the route
             new_time_space_info: the time space information after inserting the order
             depot:
             updated_orders: the list of orders which also includes the order to insert
             order_to_insert: the order which is to be inserted
             position_to_insert:
             matrix:
             coefficient:
       Returns:
    """
    lambda_ = coefficient.lambda_
    return lambda_ * order_to_insert.distance_from_depot - get_insertion_cost_1(old_time_space_info,
                                                                                new_time_space_info, depot,
                                                                                updated_orders, position_to_insert,
                                                                                matrix, coefficient)
