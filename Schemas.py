from marshmallow import Schema, fields, pprint, post_load
from Classes import *

class LocationSchema(Schema):
    locationId = fields.Integer()
    latitude = fields.Float()
    longitude = fields.Float()

    @post_load
    def make_location(self,data):
        return Location(**data)


class TimewindowSchema(Schema):
    startTime = fields.Time()
    endTime = fields.Time()

    @post_load
    def make_timewindow(self,data):
        return Timewindow(**data)



class TimefeatureSchema(Schema):
    timeWindow = fields.Nested(TimewindowSchema())
    handlingTime = fields.Integer()
    readyForDepartureTime = fields.Time()

    @post_load
    def make_timefeature(self,data):
        return Timefeature(**data)



class PhysicalfeatureSchema(Schema):
    capacity = fields.Integer()
    isLiftGateRequired = fields.Bool()

    @post_load
    def make_physicalfeature(self,data):
        return Physicalfeature(**data)

class ConfigurationSchema(Schema):
    averageVehicleSpeed = fields.Float()
    maxTotalTravelTime = fields.Float()
    MaxTotalTravelDistance = fields.Integer()

    @post_load
    def make_configuration(self,data):
        return Configuration(**data)

class DistanceInfoSchema(Schema):
    distance = fields.Integer()
    time = fields.Integer()
    totalCost = fields.Integer()

    @post_load
    def make_distanceInfo(self,data):
        return DistanceInfo(**data)


class DepotSchema(Schema):
    location = fields.Nested(LocationSchema())
    timeWindow = fields.Nested(TimewindowSchema())

    @post_load
    def make_depot(self,data):
        return Depot(**data)

class VehicleSchema(Schema):
    name = fields.Str()
    isResidential = fields.Bool()
    hasLiftGate = fields.Bool()
    count = fields.Integer()
    capacity = fields.Integer()

    @post_load
    def make_vehicle(self,data):
        return Vehicle(**data)


class OrderSchema(Schema):
    location = fields.Nested(LocationSchema())
    timeFeature = fields.Nested(TimefeatureSchema())
    physicalFeature = fields.Nested(PhysicalfeatureSchema())
    depot = fields.Nested(DepotSchema())

    @post_load
    def make_order(self,data):
        return Order(**data)




