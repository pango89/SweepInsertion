from marshmallow import Schema, fields, post_load, pre_dump
from marshmallow_enum import EnumField
import json

from Classes import *


class LocationSchema(Schema):
    locationId = fields.Integer()
    latitude = fields.Float()
    longitude = fields.Float()

    @post_load
    def make_location(self, data):
        return Location(**data)


class TimeWindowSchema(Schema):
    startTime = fields.Str()  # Time('%H:%M %p')
    endTime = fields.Str()  # Time('%H:%M %p')

    @post_load
    def make_timeWindow(self, data):
        return TimeWindow(**data)


class TimeFeatureSchema(Schema):
    timeWindow = fields.Nested(TimeWindowSchema())
    handlingTime = fields.Integer()
    readyForDepartureTime = fields.Str()  # Time('%H:%M %p')

    @post_load
    def make_timeFeature(self, data):
        return TimeFeature(**data)


class PhysicalFeatureSchema(Schema):
    capacity = fields.Integer()
    isLiftGateRequired = fields.Bool()

    @post_load
    def make_physicalFeature(self, data):
        return PhysicalFeature(**data)


class ConfigurationSchema(Schema):
    averageVehicleSpeed = fields.Float()
    maxTotalTravelTime = fields.Float()
    maxTotalTravelDistance = fields.Integer()
    maxAllowedStopsCount = fields.Integer()

    @post_load
    def make_configuration(self, data):
        return Configuration(**data)


class DistanceInfoSchema(Schema):
    distance = fields.Float()
    time = fields.Float()
    totalCost = fields.Float()

    @post_load
    def make_distanceInfo(self, data):
        return DistanceInfo(**data)


class DepotSchema(Schema):
    location = fields.Nested(LocationSchema())
    timeWindow = fields.Nested(TimeWindowSchema())

    @post_load
    def make_depot(self, data):
        return Depot(**data)


class VehicleSchema(Schema):
    name = fields.Str()
    isResidential = fields.Bool()
    hasLiftGate = fields.Bool()
    count = fields.Integer()
    capacity = fields.Integer()

    @post_load
    def make_vehicle(self, data):
        return Vehicle(**data)


class OrderSchema(Schema):
    location = fields.Nested(LocationSchema())
    timeFeature = fields.Nested(TimeFeatureSchema())
    physicalFeature = fields.Nested(PhysicalFeatureSchema())
    depot = fields.Nested(DepotSchema())

    @post_load
    def make_order(self, data):
        return Order(**data)


class TimeSpaceInfoSchema(Schema):
    travel_time = fields.Int()
    travel_distance = fields.Float()
    arrival_times = fields.List(fields.Time('%I:%M %p'))
    waiting_times = fields.List(fields.Float())
    spare_times = fields.List(fields.Float())
    earliest_departure_time = fields.Time()
    best_earliest_departure_time = fields.Time()
    best_latest_departure_time = fields.Time()


class JobInputSchema(Schema):
    orders = fields.List(fields.Nested(OrderSchema))
    vehicles = fields.List(fields.Nested(VehicleSchema))
    depot = fields.Nested(DepotSchema)
    configuration = fields.Nested(ConfigurationSchema)
    locationMatrix = fields.List(fields.List(fields.Nested(DistanceInfoSchema)))

    @post_load
    def make_jobInput(self, data):
        return JobInput(**data)


class RouteSchema(Schema):
    status = EnumField(FeasibilityStatus)
    orders = fields.List(fields.Nested(OrderSchema))
    depot = fields.Nested(DepotSchema)
    vehicle = fields.Nested(VehicleSchema)
    time_space_info = fields.Nested(TimeSpaceInfoSchema)

    @post_load
    def make_route(self, data):
        return Route(**data)
