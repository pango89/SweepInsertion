from Classes import TimeSpaceInfo, FeasibilityStatus


def is_capacity_honoured(orders, max_allowed_capacity):
    occupied = sum(order.physicalFeature.capacity for order in orders)
    if occupied > max_allowed_capacity:
        return False

    return True


def is_time_window_honoured(orders, depot, matrix, configuration):
    orders_arrival_time = {}
    orders_wait_time = {}
    orders_spare_time = {}

    earliest_departure_time = max(order.timeFeature.readyForDepartureTime for order in orders)

    arrival_times = []
    wait_times = []
    spare_times = []

    current_order = orders[0]
    earliest_time = current_order.timeFeature.timeWindow.startTime
    latest_time = current_order.timeFeature.timeWindow.endTime

    travel_time = (matrix[depot.location.locationId][current_order.location.locationId]).time
    travel_time_aggregate = travel_time

    service_start_time = travel_time + earliest_departure_time
    best_earliest_departure_time = earliest_departure_time
    best_late_departure_time = earliest_departure_time

    travel_distance = (matrix[depot.location.locationId][current_order.location.locationId]).distance
    travel_distance_aggregate = travel_distance

    if not (is_contained_in_time_slot(earliest_time, latest_time, service_start_time)):
        feasibility_status = FeasibilityStatus.time_window_not_honoured
        return feasibility_status, TimeSpaceInfo(travel_time_aggregate, travel_distance_aggregate, orders_arrival_time,
                                                 orders_wait_time, orders_spare_time, earliest_departure_time,
                                                 best_earliest_departure_time,
                                                 best_late_departure_time)

    if earliest_time > service_start_time:
        service_start_time = earliest_time
        best_earliest_departure_time = service_start_time - travel_time
    arrival_times.append(service_start_time)
    wait_times.append(0)
    spare_times.append(latest_time - service_start_time)
    minimum_spare_time = spare_times[0]

    for i in range(1, len(orders)):
        current_order = orders[i]
        previous_order = orders[i - 1]

        earliest_time = current_order.timeFeature.timeWindow.startTime
        latest_time = current_order.timeFeature.timeWindow.endTime

        travel_time = (matrix[previous_order.location.locationId][current_order.location.locationId]).time
        travel_time_aggregate += previous_order.timeFeature.handlingTime + travel_time

        service_start_time = service_start_time + previous_order.timeFeature.handlingTime + travel_time

        if not (is_contained_in_time_slot(earliest_time, latest_time, service_start_time)):
            feasibility_status = FeasibilityStatus.time_window_not_honoured
            return feasibility_status, TimeSpaceInfo(travel_time_aggregate, travel_distance_aggregate,
                                                     orders_arrival_time,
                                                     orders_wait_time, orders_spare_time, earliest_departure_time,
                                                     best_earliest_departure_time,
                                                     best_late_departure_time)

        if not is_total_travel_time_honoured(travel_time_aggregate, configuration.maxTotalTravelTime):
            feasibility_status = FeasibilityStatus.total_travel_time_not_honoured
            return feasibility_status, TimeSpaceInfo(travel_time_aggregate, travel_distance_aggregate,
                                                     orders_arrival_time,
                                                     orders_wait_time, orders_spare_time, earliest_departure_time,
                                                     best_earliest_departure_time,
                                                     best_late_departure_time)

        travel_distance = (matrix[previous_order.location.locationId][current_order.location.locationId]).distance
        travel_distance_aggregate += travel_distance

        if not is_total_travel_distance_honoured(travel_distance_aggregate, configuration.maxTotalTravelDistance):
            feasibility_status = FeasibilityStatus.total_travel_distance_not_honoured
            return feasibility_status, TimeSpaceInfo(travel_time_aggregate, travel_distance_aggregate,
                                                     orders_arrival_time,
                                                     orders_wait_time, orders_spare_time, earliest_departure_time,
                                                     best_earliest_departure_time,
                                                     best_late_departure_time)

        arrival_times.append(service_start_time)

        earliness = earliest_time - service_start_time

        if earliness > 0:
            wait_times.append(earliness)
            service_start_time = earliest_time
        else:
            wait_times.append(0)

        current_spare_time = latest_time - service_start_time + wait_times[-1]
        spare_times.append(current_spare_time)

        if minimum_spare_time > 0:
            if wait_times[-1] > 0:
                time_saving = min(minimum_spare_time, wait_times[-1])
                if time_saving > 0:
                    best_earliest_departure_time, service_start_time, minimum_spare_time = push_back_departure_time(
                        time_saving, arrival_times, wait_times, spare_times, best_earliest_departure_time,
                        minimum_spare_time)
                else:
                    minimum_spare_time = min(current_spare_time, minimum_spare_time)
            else:
                minimum_spare_time = min(current_spare_time, minimum_spare_time)

        is_last_stop = (i == len(orders) - 1)

        if is_last_stop:
            time_saving = min(minimum_spare_time, spare_times[-1])
            if time_saving > 0:
                best_late_departure_time = best_earliest_departure_time + time_saving
            else:
                best_late_departure_time = best_earliest_departure_time

    travel_time_aggregate = service_start_time + current_order.timeFeature.handlingTime - best_earliest_departure_time

    if not is_total_travel_time_honoured(travel_time_aggregate, configuration.maxTotalTravelTime):
        feasibility_status = FeasibilityStatus.total_travel_time_not_honoured
        return feasibility_status, TimeSpaceInfo(travel_time_aggregate, travel_distance_aggregate, orders_arrival_time,
                                                 orders_wait_time, orders_spare_time, earliest_departure_time,
                                                 best_earliest_departure_time,
                                                 best_late_departure_time)

    feasibility_status = FeasibilityStatus.feasible
    return feasibility_status, TimeSpaceInfo(travel_time_aggregate, travel_distance_aggregate, orders_arrival_time,
                                             orders_wait_time, orders_spare_time, earliest_departure_time,
                                             best_earliest_departure_time,
                                             best_late_departure_time)


def is_max_stops_count_honoured(orders, max_allowed_stops):
    return len(orders) <= max_allowed_stops


def is_total_travel_time_honoured(travel_time, max_travel_time):
    return travel_time <= max_travel_time


def is_total_travel_distance_honoured(travel_distance, max_travel_distance):
    return travel_distance <= max_travel_distance


def is_contained_in_time_slot(start, end, time):
    if start <= time <= end:
        return True

    return False


def push_back_departure_time(time_saving, arrival_times, wait_times, spare_times, best_earliest_departure_time,
                             minimum_spare_time):
    updated_departure_time = best_earliest_departure_time + time_saving

    for i in range(0, len(arrival_times)):
        arrival_times[i] += time_saving
        spare_times[i] -= time_saving

        minimum_spare_time = min(minimum_spare_time, spare_times[i])

        if wait_times[i] > 0:
            local_push = time_saving - wait_times[i]
            if local_push <= 0:
                wait_times[i] = -local_push
                time_saving = 0
            else:
                wait_times[i] = 0
                time_saving -= local_push

        if time_saving == 0:
            break

    service_start_time = arrival_times[-1] + wait_times[-1]
    return updated_departure_time, service_start_time, minimum_spare_time


def perform_feasibility_check(orders, depot, vehicle, matrix, configuration):
    if not is_max_stops_count_honoured(orders, configuration.maxAllowedStopsCount):
        feasibility_status = FeasibilityStatus.max_count_stops_not_honoured
        return feasibility_status, None

    if not is_capacity_honoured(orders, vehicle.capacity):
        feasibility_status = FeasibilityStatus.capacity_not_honoured
        return feasibility_status, None

    feasibility_status, time_space_info = is_time_window_honoured(orders, depot, matrix, configuration)

    return feasibility_status, time_space_info
