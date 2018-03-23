import pandas as pd


def flatten_output(output):
    routes = output.routes
    flat = []
    for i in range(len(routes)):
        route = routes[i]
        orders = route.orders
        for j in range(len(orders)):
            order = orders[j]
            dictionary = {'routeId': i + 1, 'orderSequence': j + 1, 'latitude': order.location.latitude,
                          'longitude': order.location.longitude, 'arrivalTime': route.time_space_info.arrival_times[j]}
            flat.append(dictionary)

    return flat


def convert_to_data_frame(flat):
    df = pd.DataFrame(flat)
    return df


def flatten_output_1(output):
    routes = output.routes
    flat = []
    for i in range(len(routes)):
        route = routes[i]
        dictionary = {'routeId': i + 1, 'travelDistance': route.time_space_info.travel_distance,
                      'travelTime': route.time_space_info.travel_time,
                      'bestEarliestDepartureTime': route.time_space_info.best_earliest_departure_time,
                      'bestLatestDepartureTime': route.time_space_info.best_latest_departure_time,
                      'totalSpareTime': sum(route.time_space_info.spare_times),
                      'totalWaitTime': sum(route.time_space_info.waiting_times)}
        flat.append(dictionary)

    return flat

