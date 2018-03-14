from enum import Enum
from Utilities import PolarCoordinate

class Order(object):
    def __init__(self, location={}, timeFeature={}, physicalFeature={}, depot={}):
        self.location = location
        self.timeFeature = timeFeature
        self.physicalFeature = physicalFeature
        self.depot = depot
        self.distance_from_depot = 0
        self.PolarCoordinate = PolarCoordinate(self.location,self.depot.location)


    def fill_distance_from_depot(self, matrix):
        self.distance_from_depot = matrix[self.depot.location.locationId][self.location.locationId].distance


class Vehicle(object):
    def __init__(self, name='', isResidential=False, hasLiftGate=False, count=0, capacity=0):
        self.name = name
        self.isResidential = True if isResidential == 'true' else False
        self.hasLiftGate = True if hasLiftGate == 'true' else False
        self.count = count
        self.capacity = capacity


class Depot(object):
    def __init__(self, location={}, timeWindow={}):
        self.location = location
        self.timeWindow = timeWindow


class Configuration(object):
    def __init__(self, averageVehicleSpeed=0, maxTotalTravelTime=0, maxTotalTravelDistance=0):
        self.averageVehicleSpeed = averageVehicleSpeed
        self.maxTotalTravelTime = maxTotalTravelTime
        self.maxTotalTravelDistance = maxTotalTravelDistance


class DistanceInfo(object):
    def __init__(self, distance=0, time=0, totalCost=0):
        self.distance = distance
        self.time = time
        self.totalCost = totalCost


class TimeFeature(object):
    def __init__(self, timeWindow={}, handlingTime=0, readyForDepartureTime=0):
        self.timeWindow = timeWindow
        self.handlingTime = handlingTime
        self.readyForDepartureTime = readyForDepartureTime


class TimeWindow(object):
    def __init__(self, startTime=0, endTime=0):
        self.startTime = startTime
        self.endTime = endTime


class Location(object):
    def __init__(self, locationId=0, latitude=0, longitude=0):
        self.locationId = locationId
        self.latitude = latitude
        self.longitude = longitude


class PhysicalFeature(object):
    def __init__(self, capacity=0, isLiftGateRequired=False):
        self.capacity = capacity
        self.isLiftGateRequired = True if isLiftGateRequired == 'true' else False


class JobInput(object):
    def __init__(self, orders, vehicles, depot, configuration, locationMatrix=[]):
        self.orders = orders
        self.vehicles = vehicles
        self.depot = depot
        self.configuration = configuration
        self.locationMatrix = locationMatrix


class TimeSpaceInfo(object):
    def __init__(self, travel_time, travel_distance, arrival_times, waiting_times, spare_times, earliest_departure_time,
                 best_earliest_departure_time,
                 best_latest_departure_time):
        self.travel_time = travel_time
        self.travel_distance = travel_distance
        self.arrival_times = arrival_times
        self.waiting_times = waiting_times
        self.spare_times = spare_times
        self.earliest_departure_time = earliest_departure_time
        self.best_earliest_departure_time = best_earliest_departure_time
        self.best_latest_departure_time = best_latest_departure_time


class Route(object):
    def __init__(self, status, orders, depot, vehicle, time_space_info):
        self.status = status
        self.orders = orders
        self.depot = depot
        self.vehicle = vehicle
        self.time_space_info = time_space_info

    def update(self, orders, time_space_info):
        self.orders = orders
        self.time_space_info = time_space_info


class FeasibilityStatus(Enum):
    none = 0
    feasible = 1
    capacity_not_honoured = 2
    time_window_not_honoured = 3
    total_travel_time_not_honoured = 4
    total_travel_distance_not_honoured = 5
    max_count_stops_not_honoured = 6
