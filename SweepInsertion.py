import SectorClustering as SectorClustering
import FeasibilityUtility
import ObjectiveFunctions
import sys
from Classes import Route, FeasibilityStatus


def generate_routes(job, clustering_parameters, objective_coefficients):
    output_routes = []
    un_routed_orders = job.orders[0:]

    while True:
        clustered_orders = SectorClustering.get_next_cluster(un_routed_orders, clustering_parameters)
        if len(clustered_orders) == 0:
            continue

        route = initiate_new_route(clustered_orders, job.depot, job.vehicles[0], job.locationMatrix, job.configuration)

        if route is None:
            break

        if len(clustered_orders) > 0:
            apply_best_feasible_insertion(route, clustered_orders, job.depot, job.locationMatrix, job.configuration,
                                          objective_coefficients)

        if len(route.orders) > 0:
            output_routes.append(route)
            un_routed_orders = [order for order in un_routed_orders if order not in route]
        else:
            break

        if len(un_routed_orders) <= 0:
            break


def initiate_new_route(orders, depot, vehicle, matrix, configuration):
    route = None
    for i in range(0, len(orders)):
        order = orders[i]
        route = Route(FeasibilityStatus.none, [order], depot, vehicle, {})

        route.status, route.time_space_info = FeasibilityUtility.perform_feasibility_check(route.orders, depot,
                                                                                           matrix, configuration)

        if route.status == FeasibilityStatus.Feasible:
            del orders[i]
            break
        else:
            route = None

    return route


def apply_best_feasible_insertion(route, clustered_orders, depot, matrix, configuration, coefficients):
    while True:
        best_route_timing = None
        best_order_to_insert = None
        best_position_to_insert = 0
        best_insertion_profit = sys.float_info.min

        for index, order in enumerate(clustered_orders):
            best_route_timing_so_far = None
            best_insertion_cost = sys.float_info.max
            order_to_insert = None
            position_to_insert = 0

            best_order_sequence = None

            for i in range(0, len(route.orders) + 1):
                updated_orders = route.orders[:i] + [order] + route.orders[i:]
                status, new_time_space_info = FeasibilityUtility.perform_feasibility_check(updated_orders, depot,
                                                                                           matrix,
                                                                                           configuration)
                if status == FeasibilityStatus.feasible:
                    insertion_cost = ObjectiveFunctions.get_insertion_cost_1(route.time_space_info, new_time_space_info,
                                                                             depot, updated_orders, i, matrix,
                                                                             coefficients)

                    if insertion_cost >= best_insertion_cost:
                        continue

                    best_insertion_cost = insertion_cost
                    order_to_insert = order
                    best_route_timing_so_far = new_time_space_info
                    position_to_insert = i
                    best_order_sequence = updated_orders

            if order_to_insert is None:
                continue

            profit = ObjectiveFunctions.get_insertion_profit(route.time_space_info, best_route_timing_so_far, depot,
                                                             best_order_sequence, order_to_insert, position_to_insert,
                                                             matrix, coefficients)

            if profit <= best_insertion_profit:
                continue

            best_insertion_profit = profit
            best_order_to_insert = order_to_insert
            best_route_timing = best_route_timing_so_far
            best_position_to_insert = position_to_insert

        if best_order_to_insert is not None:
            route_orders = route.orders[:best_position_to_insert] + [best_order_to_insert] + route.orders[
                                                                                             best_position_to_insert:]
            route.update(route_orders, best_route_timing)
            clustered_orders.remove(best_order_to_insert)
        else:
            break
